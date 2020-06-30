#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from collections import defaultdict
from typing import Type, List, Dict, Optional, Callable

from .event import Event
from .typing import Handler
from .rule import Rule, user
from .exception import PausedException, RejectedException, FinishedException

matchers: Dict[int, List[Type["Matcher"]]] = defaultdict(list)


class Matcher:

    rule: Rule = Rule()
    handlers: List[Handler] = []
    temp: bool = False
    priority: int = 1

    _default_state: dict = {}

    # _default_parser: Optional[Callable[[Event, dict], None]] = None
    # _args_parser: Optional[Callable[[Event, dict], None]] = None

    def __init__(self):
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()
        # self.parser = self._args_parser or self._default_parser

    @classmethod
    def new(cls,
            rule: Rule = Rule(),
            handlers: list = [],
            temp: bool = False,
            priority: int = 1,
            *,
            default_state: dict = {}) -> Type["Matcher"]:

        NewMatcher = type(
            "Matcher", (Matcher,), {
                "rule": rule,
                "handlers": handlers,
                "temp": temp,
                "priority": priority,
                "_default_state": default_state
            })

        matchers[priority].append(NewMatcher)

        return NewMatcher

    # @classmethod
    # def args_parser(cls, func: Callable[[Event, dict], None]):
    #     cls._default_parser = func
    #     return func

    @classmethod
    def handle(cls):

        def _decorator(func: Handler) -> Handler:
            cls.handlers.append(func)
            return func

        return _decorator

    @classmethod
    def receive(cls):

        def _decorator(func: Handler) -> Handler:

            @wraps(func)
            async def _handler(bot, event: Event, state: dict):
                raise PausedException

            cls.handlers.append(_handler)
            cls.handlers.append(func)

            return func

        return _decorator

    # @classmethod
    # def got(cls,
    #         key: str,
    #         prompt: Optional[str] = None,
    #         args_parser: Optional[Callable[[Event, dict], None]] = None):

    #     def _decorator(func: Handler) -> Handler:

    #         @wraps(func)
    #         def _handler(event: Event, state: dict):
    #             if key not in state:
    #                 if state.get("__current_arg__", None) == key:
    #                     state[key] = event.message
    #                     del state["__current_arg__"]
    #                     return func(event, state)
    #                 state["__current_arg__"] = key
    #                 cls._args_parser = args_parser
    #                 raise RejectedException

    #             return func(event, state)

    #         cls.handlers.append(_handler)

    #         return func

    #     return _decorator

    # @classmethod
    # def finish(cls, prompt: Optional[str] = None):
    #     raise FinishedException

    # @classmethod
    # def reject(cls, prompt: Optional[str] = None):
    #     raise RejectedException

    async def run(self, bot, event):
        if not self.rule(event):
            return

        try:
            # if self.parser:
            #     await self.parser(event, state)  # type: ignore

            for _ in range(len(self.handlers)):
                handler = self.handlers.pop(0)
                await handler(bot, event, self.state)
        except RejectedException:
            self.handlers.insert(0, handler)  # type: ignore
            matcher = Matcher.new(user(event.user_id) & self.rule,
                                  self.handlers,
                                  temp=True,
                                  priority=0,
                                  default_state=self.state)
            matchers[0].append(matcher)
            return
        except PausedException:
            matcher = Matcher.new(user(event.user_id) & self.rule,
                                  self.handlers,
                                  temp=True,
                                  priority=0,
                                  default_state=self.state)
            matchers[0].append(matcher)
            return
        except FinishedException:
            return
