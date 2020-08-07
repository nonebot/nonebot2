#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from nonebot.event import Event
from nonebot.typing import Union, Callable, Optional


class Rule:

    def __init__(
        self,
        checker: Optional[Callable[["BaseBot", Event],  # type: ignore
                                   bool]] = None):
        self.checker = checker or (lambda bot, event: True)

    def __call__(self, bot, event: Event) -> bool:
        return self.checker(bot, event)

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(lambda bot, event: self.checker(bot, event) and other.
                    checker(bot, event))

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(lambda bot, event: self.checker(bot, event) or other.
                    checker(bot, event))

    def __neg__(self) -> "Rule":
        return Rule(lambda bot, event: not self.checker(bot, event))


def message() -> Rule:
    return Rule(lambda bot, event: event.type == "message")


def notice() -> Rule:
    return Rule(lambda bot, event: event.type == "notice")


def request() -> Rule:
    return Rule(lambda bot, event: event.type == "request")


def metaevent() -> Rule:
    return Rule(lambda bot, event: event.type == "meta_event")


def user(*qq: int) -> Rule:
    return Rule(lambda bot, event: event.user_id in qq)


def private() -> Rule:
    return Rule(lambda bot, event: event.detail_type == "private")


def group(*group: int) -> Rule:
    return Rule(lambda bot, event: event.detail_type == "group" and event.
                group_id in group)


def discuss(*discuss: int) -> Rule:
    return Rule(lambda bot, event: event.detail_type == "discuss" and event.
                discuss_id in discuss)


def startswith(msg, start: int = None, end: int = None) -> Rule:
    return Rule(lambda bot, event: event.message.startswith(msg, start, end))


def endswith(msg, start: int = None, end: int = None) -> Rule:
    return Rule(
        lambda bot, event: event.message.endswith(msg, start=None, end=None))


def has(msg: str) -> Rule:
    return Rule(lambda bot, event: msg in event.message)


def regex(regex, flags: Union[int, re.RegexFlag] = 0) -> Rule:
    pattern = re.compile(regex, flags)
    return Rule(lambda bot, event: bool(pattern.search(str(event.message))))
