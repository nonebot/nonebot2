#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.log import logger
import typing
import inspect
from functools import wraps
from datetime import datetime
from contextvars import ContextVar
from collections import defaultdict

from nonebot.rule import Rule
from nonebot.permission import Permission, USER
from nonebot.typing import Type, List, Dict, Union, Callable, Optional, NoReturn
from nonebot.typing import Bot, Event, Handler, Message, ArgsParser, MessageSegment
from nonebot.exception import PausedException, RejectedException, FinishedException

matchers: Dict[int, List[Type["Matcher"]]] = defaultdict(list)
current_bot: ContextVar = ContextVar("current_bot")
current_event: ContextVar = ContextVar("current_event")


class MatcherMeta(type):

    def __repr__(self) -> str:
        return (f"<Matcher from {self.module or 'unknow'}, "  # type: ignore
                f"type={self.type}, priority={self.priority}, "  # type: ignore
                f"temp={self.temp}>")  # type: ignore

    def __str__(self) -> str:
        return repr(self)


class Matcher(metaclass=MatcherMeta):
    """`Matcher`类
    """
    module: Optional[str] = None

    type: str = ""
    rule: Rule = Rule()
    permission: Permission = Permission()
    handlers: List[Handler] = []
    temp: bool = False
    expire_time: Optional[datetime] = None
    priority: int = 1
    block: bool = False

    _default_state: dict = {}

    _default_parser: Optional[ArgsParser] = None

    def __init__(self):
        """实例化 Matcher 以便运行
        """
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()

    def __repr__(self) -> str:
        return (f"<Matcher from {self.module or 'unknow'}, type={self.type}, "
                f"priority={self.priority}, temp={self.temp}>")

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def new(cls,
            type_: str = "",
            rule: Rule = Rule(),
            permission: Permission = Permission(),
            handlers: Optional[list] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            *,
            module: Optional[str] = None,
            default_state: Optional[dict] = None,
            expire_time: Optional[datetime] = None) -> Type["Matcher"]:
        """创建新的 Matcher

        Returns:
            Type["Matcher"]: 新的 Matcher 类
        """

        NewMatcher = type(
            "Matcher", (Matcher,), {
                "module": module,
                "type": type_,
                "rule": rule,
                "permission": permission,
                "handlers": handlers or [],
                "temp": temp,
                "expire_time": expire_time,
                "priority": priority,
                "block": block,
                "_default_state": default_state or {}
            })

        matchers[priority].append(NewMatcher)

        return NewMatcher

    @classmethod
    async def check_perm(cls, bot: Bot, event: Event) -> bool:
        return await cls.permission(bot, event)

    @classmethod
    async def check_rule(cls, bot: Bot, event: Event, state: dict) -> bool:
        """检查 Matcher 的 Rule 是否成立

        Args:
            event (Event): 消息事件

        Returns:
            bool: 条件成立与否
        """
        return (event.type == (cls.type or event.type) and
                await cls.rule(bot, event, state))

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

        async def _receive(bot: Bot, event: Event, state: dict) -> NoReturn:
            raise PausedException

        if cls.handlers:
            # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
            cls.handlers.append(_receive)

        def _decorator(func: Handler) -> Handler:
            if not cls.handlers or cls.handlers[-1] is not func:
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

        async def _key_getter(bot: Bot, event: Event, state: dict):
            state["_current_key"] = key
            if key not in state:
                if prompt:
                    await bot.send(event=event, message=prompt)
                raise PausedException
            else:
                state["_skip_key"] = True

        async def _key_parser(bot: Bot, event: Event, state: dict):
            if key in state and state.get("_skip_key"):
                del state["_skip_key"]
                return
            parser = args_parser or cls._default_parser
            if parser:
                await parser(bot, event, state)
            else:
                state[state["_current_key"]] = str(event.message)

        cls.handlers.append(_key_getter)
        cls.handlers.append(_key_parser)

        def _decorator(func: Handler) -> Handler:
            if not hasattr(cls.handlers[-1], "__wrapped__"):
                parser = cls.handlers.pop()

                @wraps(func)
                async def wrapper(bot: Bot, event: Event, state: dict):
                    await parser(bot, event, state)
                    await func(bot, event, state)
                    if "_current_key" in state:
                        del state["_current_key"]

                cls.handlers.append(wrapper)

            return func

        return _decorator

    @classmethod
    async def finish(
        cls,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise FinishedException

    @classmethod
    async def pause(
        cls,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise PausedException

    @classmethod
    async def reject(
        cls,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise RejectedException

    # 运行handlers
    async def run(self, bot: Bot, event: Event, state: dict):
        b_t = current_bot.set(bot)
        e_t = current_event.set(event)
        try:
            # Refresh preprocess state
            self.state.update(state)

            for _ in range(len(self.handlers)):
                handler = self.handlers.pop(0)
                annotation = typing.get_type_hints(handler)
                BotType = annotation.get("bot")
                if BotType and inspect.isclass(BotType) and not isinstance(
                        bot, BotType):
                    continue
                await handler(bot, event, self.state)

        except RejectedException:
            self.handlers.insert(0, handler)  # type: ignore
            Matcher.new(
                self.type,
                Rule(),
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
        except PausedException:
            Matcher.new(
                self.type,
                Rule(),
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
        except FinishedException:
            pass
        finally:
            logger.info(f"Matcher {self} running complete")
            current_bot.reset(b_t)
            current_event.reset(e_t)


class MatcherGroup:

    def __init__(self,
                 type_: str = "",
                 rule: Rule = Rule(),
                 permission: Permission = Permission(),
                 handlers: Optional[list] = None,
                 temp: bool = False,
                 priority: int = 1,
                 block: bool = False,
                 *,
                 module: Optional[str] = None,
                 default_state: Optional[dict] = None,
                 expire_time: Optional[datetime] = None):
        self.matchers: List[Type[Matcher]] = []

        self.type = type_
        self.rule = rule
        self.permission = permission
        self.handlers = handlers
        self.temp = temp
        self.priority = priority
        self.block = block
        self.module = module
        self.expire_time = expire_time

        self._default_state = default_state

        self._default_parser: Optional[ArgsParser] = None

    def __repr__(self) -> str:
        return (
            f"<MatcherGroup from {self.module or 'unknow'}, type={self.type}, "
            f"priority={self.priority}, temp={self.temp}>")

    def __str__(self) -> str:
        return self.__repr__()

    def new(self,
            type_: str = "",
            rule: Rule = Rule(),
            permission: Permission = Permission(),
            handlers: Optional[list] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            *,
            module: Optional[str] = None,
            default_state: Optional[dict] = None,
            expire_time: Optional[datetime] = None) -> Type[Matcher]:
        matcher = Matcher.new(type_=type_ or self.type,
                              rule=self.rule & rule,
                              permission=permission or self.permission,
                              handlers=handlers or self.handlers,
                              temp=temp or self.temp,
                              priority=priority or self.priority,
                              block=block or self.block,
                              module=module or self.module,
                              default_state=default_state or
                              self._default_state,
                              expire_time=expire_time or self.expire_time)
        self.matchers.append(matcher)
        return matcher

    def args_parser(self, func: ArgsParser) -> ArgsParser:
        for matcher in self.matchers:
            matcher.args_parser(func)
        return func

    def handle(self) -> Callable[[Handler], Handler]:
        """直接处理消息事件"""

        def _decorator(func: Handler) -> Handler:
            self.handlers.append(func)
            return func

        return _decorator

    def receive(self) -> Callable[[Handler], Handler]:
        """接收一条新消息并处理"""

        async def _receive(bot: Bot, event: Event, state: dict) -> NoReturn:
            raise PausedException

        if self.handlers:
            # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
            self.handlers.append(_receive)

        def _decorator(func: Handler) -> Handler:
            if not self.handlers or self.handlers[-1] is not func:
                self.handlers.append(func)

            return func

        return _decorator

    def got(
        self,
        key: str,
        prompt: Optional[str] = None,
        args_parser: Optional[ArgsParser] = None
    ) -> Callable[[Handler], Handler]:

        async def _key_getter(bot: Bot, event: Event, state: dict):
            state["_current_key"] = key
            if key not in state:
                if prompt:
                    await bot.send(event=event, message=prompt)
                raise PausedException
            else:
                state["_skip_key"] = True

        async def _key_parser(bot: Bot, event: Event, state: dict):
            if key in state and state.get("_skip_key"):
                del state["_skip_key"]
                return
            parser = args_parser or self._default_parser
            if parser:
                await parser(bot, event, state)
            else:
                state[state["_current_key"]] = str(event.message)

        self.handlers.append(_key_getter)
        self.handlers.append(_key_parser)

        def _decorator(func: Handler) -> Handler:
            if not hasattr(self.handlers[-1], "__wrapped__"):
                parser = self.handlers.pop()

                @wraps(func)
                async def wrapper(bot: Bot, event: Event, state: dict):
                    await parser(bot, event, state)
                    await func(bot, event, state)
                    if "_current_key" in state:
                        del state["_current_key"]

                self.handlers.append(wrapper)

            return func

        return _decorator

    async def finish(
        self,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise FinishedException

    async def pause(
        self,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise PausedException

    async def reject(
        self,
        prompt: Optional[Union[str, Message,
                               MessageSegment]] = None) -> NoReturn:
        bot: Bot = current_bot.get()
        event: Event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt)
        raise RejectedException
