#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
from functools import wraps
from datetime import datetime
from collections import defaultdict

from nonebot.rule import Rule
from nonebot.permission import Permission, USER
from nonebot.typing import Bot, Event, Handler, ArgsParser
from nonebot.typing import Type, List, Dict, Callable, Optional, NoReturn
from nonebot.exception import PausedException, RejectedException, FinishedException

matchers: Dict[int, List[Type["Matcher"]]] = defaultdict(list)


class Matcher:
    """`Matcher`类
    """

    type: str = ""
    rule: Rule = Rule()
    permission: Permission = Permission()
    handlers: List[Handler] = []
    temp: bool = False
    expire_time: Optional[datetime] = None
    priority: int = 1

    _default_state: dict = {}

    _default_parser: Optional[ArgsParser] = None

    def __init__(self):
        """实例化 Matcher 以便运行
        """
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()

    @classmethod
    def new(cls,
            type_: str = "",
            rule: Rule = Rule(),
            permission: Permission = Permission(),
            handlers: list = [],
            temp: bool = False,
            priority: int = 1,
            *,
            default_state: dict = {},
            expire_time: Optional[datetime] = None) -> Type["Matcher"]:
        """创建新的 Matcher

        Returns:
            Type["Matcher"]: 新的 Matcher 类
        """

        NewMatcher = type(
            "Matcher", (Matcher,), {
                "type": type_,
                "rule": rule,
                "permission": permission,
                "handlers": handlers,
                "temp": temp,
                "expire_time": expire_time,
                "priority": priority,
                "_default_state": default_state
            })

        matchers[priority].append(NewMatcher)

        return NewMatcher

    @classmethod
    async def check_perm(cls, bot: Bot, event: Event) -> bool:
        return (event.type == (cls.type or event.type) and
                await cls.permission(bot, event))

    @classmethod
    async def check_rule(cls, bot: Bot, event: Event, state: dict) -> bool:
        """检查 Matcher 的 Rule 是否成立

        Args:
            event (Event): 消息事件

        Returns:
            bool: 条件成立与否
        """
        return await cls.rule(bot, event, state)

    @classmethod
    def args_parser(cls, func: ArgsParser) -> ArgsParser:
        cls._default_parser = func
        return func

    @classmethod
    def handle(cls) -> Callable[[Handler], Handler]:
        """直接处理消息事件"""

        def _decorator(func: Handler) -> Handler:
            cls.handlers.append(func)
            return func

        return _decorator

    @classmethod
    def receive(cls) -> Callable[[Handler], Handler]:
        """接收一条新消息并处理"""

        def _decorator(func: Handler) -> Handler:

            async def _handler(bot: Bot, event: Event, state: dict) -> NoReturn:
                raise PausedException

            if cls.handlers:
                # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
                cls.handlers.append(_handler)
            cls.handlers.append(func)

            return func

        return _decorator

    @classmethod
    def got(
        cls,
        key: str,
        prompt: Optional[str] = None,
        args_parser: Optional[ArgsParser] = None
    ) -> Callable[[Handler], Handler]:

        def _decorator(func: Handler) -> Handler:

            async def _key_getter(bot: Bot, event: Event, state: dict):
                if key not in state:
                    state["_current_key"] = key
                    if prompt:
                        await bot.send_private_msg(user_id=event.user_id,
                                                   message=prompt)
                    raise PausedException

            async def _key_parser(bot: Bot, event: Event, state: dict):
                parser = args_parser or cls._default_parser
                if parser:
                    await parser(bot, event, state)
                else:
                    state[state["_current_key"]] = str(event.message)

            if cls.handlers:
                # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
                cls.handlers.append(_key_getter)
            cls.handlers.append(_key_parser)
            cls.handlers.append(func)

            return func

        return _decorator

    @classmethod
    def finish(cls) -> NoReturn:
        raise FinishedException

    @classmethod
    def pause(cls) -> NoReturn:
        raise PausedException

    @classmethod
    def reject(cls) -> NoReturn:
        raise RejectedException

    # 运行handlers
    async def run(self, bot: Bot, event: Event, state: dict):
        try:
            # Refresh preprocess state
            self.state.update(state)

            for _ in range(len(self.handlers)):
                handler = self.handlers.pop(0)
                annotation = typing.get_type_hints(handler)
                BotType = annotation.get("bot")
                if BotType and not isinstance(bot, BotType):
                    continue
                await handler(bot, event, self.state)

        except RejectedException:
            self.handlers.insert(0, handler)  # type: ignore
            matcher = Matcher.new(
                self.type,
                self.rule,
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
            matchers[0].append(matcher)
            return
        except PausedException:
            matcher = Matcher.new(
                self.type,
                self.rule,
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
            matchers[0].append(matcher)
            return
        except FinishedException:
            return
