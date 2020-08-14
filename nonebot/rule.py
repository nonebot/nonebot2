#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import abc
import asyncio
from typing import cast

from nonebot.utils import run_sync
from nonebot.typing import Bot, Event, Union, Optional, Awaitable
from nonebot.typing import RuleChecker, SyncRuleChecker, AsyncRuleChecker


class BaseRule(abc.ABC):

    def __init__(self, checker: RuleChecker):
        self.checker: RuleChecker = checker

    @abc.abstractmethod
    def __call__(self, bot: Bot, event: Event) -> Awaitable[bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def __and__(self, other: Union["BaseRule", RuleChecker]) -> "BaseRule":
        raise NotImplementedError

    @abc.abstractmethod
    def __or__(self, other: Union["BaseRule", RuleChecker]) -> "BaseRule":
        raise NotImplementedError

    @abc.abstractmethod
    def __neg__(self) -> "BaseRule":
        raise NotImplementedError


class AsyncRule(BaseRule):

    def __init__(self, checker: Optional[AsyncRuleChecker] = None):

        async def always_true(bot: Bot, event: Event) -> bool:
            return True

        self.checker: AsyncRuleChecker = checker or always_true

    def __call__(self, bot: Bot, event: Event) -> Awaitable[bool]:
        return self.checker(bot, event)

    def __and__(self, other: Union[BaseRule, RuleChecker]) -> "AsyncRule":
        func = other
        if isinstance(other, BaseRule):
            func = other.checker

        if not asyncio.iscoroutinefunction(func):
            func = run_sync(func)

        async def tmp(bot: Bot, event: Event) -> bool:
            a, b = await asyncio.gather(self.checker(bot, event),
                                        func(bot, event))
            return a and b

        return AsyncRule(tmp)

    def __or__(self, other: Union[BaseRule, RuleChecker]) -> "AsyncRule":
        func = other
        if isinstance(other, BaseRule):
            func = other.checker

        if not asyncio.iscoroutinefunction(func):
            func = run_sync(func)

        async def tmp(bot: Bot, event: Event) -> bool:
            a, b = await asyncio.gather(self.checker(bot, event),
                                        func(bot, event))
            return a or b

        return AsyncRule(tmp)

    def __neg__(self) -> "AsyncRule":

        async def neg(bot: Bot, event: Event) -> bool:
            result = await self.checker(bot, event)
            return not result

        return AsyncRule(neg)


class SyncRule(BaseRule):

    def __init__(self, checker: Optional[SyncRuleChecker] = None):

        def always_true(bot: Bot, event: Event) -> bool:
            return True

        self.checker: SyncRuleChecker = checker or always_true

    def __call__(self, bot: Bot, event: Event) -> Awaitable[bool]:
        return run_sync(self.checker)(bot, event)

    def __and__(self, other: Union[BaseRule, RuleChecker]) -> BaseRule:
        func = other
        if isinstance(other, BaseRule):
            func = other.checker

        if not asyncio.iscoroutinefunction(func):
            # func: SyncRuleChecker
            syncfunc = cast(SyncRuleChecker, func)

            def tmp(bot: Bot, event: Event) -> bool:
                return self.checker(bot, event) and syncfunc(bot, event)

            return SyncRule(tmp)
        else:
            # func: AsyncRuleChecker
            asyncfunc = cast(AsyncRuleChecker, func)

            async def tmp(bot: Bot, event: Event) -> bool:
                a, b = await asyncio.gather(
                    run_sync(self.checker)(bot, event), asyncfunc(bot, event))
                return a and b

            return AsyncRule(tmp)

    def __or__(self, other: Union[BaseRule, RuleChecker]) -> BaseRule:
        func = other
        if isinstance(other, BaseRule):
            func = other.checker

        if not asyncio.iscoroutinefunction(func):
            # func: SyncRuleChecker
            syncfunc = cast(SyncRuleChecker, func)

            def tmp(bot: Bot, event: Event) -> bool:
                return self.checker(bot, event) or syncfunc(bot, event)

            return SyncRule(tmp)
        else:
            # func: AsyncRuleChecker
            asyncfunc = cast(AsyncRuleChecker, func)

            async def tmp(bot: Bot, event: Event) -> bool:
                a, b = await asyncio.gather(
                    run_sync(self.checker)(bot, event), asyncfunc(bot, event))
                return a or b

            return AsyncRule(tmp)

    def __neg__(self) -> "SyncRule":

        def neg(bot: Bot, event: Event) -> bool:
            return not self.checker(bot, event)

        return SyncRule(neg)


def Rule(func: Optional[RuleChecker] = None) -> BaseRule:
    if func and asyncio.iscoroutinefunction(func):
        asyncfunc = cast(AsyncRuleChecker, func)
        return AsyncRule(asyncfunc)
    else:
        syncfunc = cast(Optional[SyncRuleChecker], func)
        return SyncRule(syncfunc)


def message() -> BaseRule:
    return Rule(lambda bot, event: event.type == "message")


def notice() -> BaseRule:
    return Rule(lambda bot, event: event.type == "notice")


def request() -> BaseRule:
    return Rule(lambda bot, event: event.type == "request")


def metaevent() -> BaseRule:
    return Rule(lambda bot, event: event.type == "meta_event")


def user(*qq: int) -> BaseRule:
    return Rule(lambda bot, event: event.user_id in qq)


def private() -> BaseRule:
    return Rule(lambda bot, event: event.detail_type == "private")


def group(*group: int) -> BaseRule:
    return Rule(lambda bot, event: event.detail_type == "group" and event.
                group_id in group)


def startswith(msg, start: int = None, end: int = None) -> BaseRule:
    return Rule(lambda bot, event: event.message.startswith(msg, start, end))


def endswith(msg, start: int = None, end: int = None) -> BaseRule:
    return Rule(
        lambda bot, event: event.message.endswith(msg, start=None, end=None))


def has(msg: str) -> BaseRule:
    return Rule(lambda bot, event: msg in event.message)


def regex(regex, flags: Union[int, re.RegexFlag] = 0) -> BaseRule:
    pattern = re.compile(regex, flags)
    return Rule(lambda bot, event: bool(pattern.search(str(event.message))))
