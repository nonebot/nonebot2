import re
import copy
from functools import wraps
from typing import Type, Union, Optional, Callable

from .event import Event
from .typing import Scope, Handler
from .rule import Rule, startswith, regex, user
from .exception import PausedException, RejectedException, FinishedException


class Matcher:

    rule: Rule = Rule()
    scope: Scope = "ALL"
    permission: str = "ALL"
    block: bool = True
    handlers: list = []
    temp: bool = False

    _default_state: dict = {}
    _default_parser: Optional[Callable[[Event, dict], None]] = None
    _args_parser: Optional[Callable[[Event, dict], None]] = None

    def __init__(self):
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()
        self.parser = self._args_parser or self._default_parser

    @classmethod
    def new(cls,
            rule: Rule = Rule(),
            scope: Scope = "ALL",
            permission: str = "ALL",
            block: bool = True,
            handlers: list = [],
            temp: bool = False,
            *,
            default_state: dict = {},
            default_parser: Optional[Callable[[Event, dict], None]] = None,
            args_parser: Optional[Callable[[Event, dict], None]] = None):

        # class NewMatcher(cls):
        #     rule: Rule = rule
        #     scope: Scope = scope
        #     permission: str = permission
        #     block: bool = block
        #     handlers: list = handlers
        #     temp: bool = temp

        #     _default_state = default_state

        NewMatcher = type(
            "Matcher", (cls,), {
                "rule": rule,
                "scope": scope,
                "permission": permission,
                "block": block,
                "handlers": handlers,
                "temp": temp,
                "_default_state": default_state,
                "_default_parser": default_parser,
                "_args_parser": args_parser,
            })

        return NewMatcher

    @classmethod
    def args_parser(cls, func: Callable[[Event, dict], None]):
        cls._default_parser = func
        return func

    @classmethod
    def receive(cls):

        def _decorator(func: Handler) -> Handler:

            @wraps(func)
            def _handler(event: Event, state: dict):
                raise PausedException

            cls.handlers.append(_handler)

            return func

        return _decorator

    @classmethod
    def got(cls,
            key: str,
            prompt: Optional[str] = None,
            args_parser: Optional[Callable[[Event, dict], None]] = None):

        def _decorator(func: Handler) -> Handler:

            @wraps(func)
            def _handler(event: Event, state: dict):
                if key not in state:
                    if state.get("__current_arg__", None) == key:
                        state[key] = event.message
                        del state["__current_arg__"]
                        return func(event, state)
                    state["__current_arg__"] = key
                    cls._args_parser = args_parser
                    raise RejectedException

                return func(event, state)

            cls.handlers.append(_handler)

            return func

        return _decorator

    @classmethod
    def finish(cls, prompt: Optional[str] = None):
        raise FinishedException

    @classmethod
    def reject(cls, prompt: Optional[str] = None):
        raise RejectedException

    async def run(self, event):
        if not self.rule(event):
            return

        try:
            if self.parser:
                await self.parser(event, state)  # type: ignore

            for _ in range(len(self.handlers)):
                handler = self.handlers.pop(0)
                await handler(event, self.state)
        except RejectedException:
            # TODO: add tmp matcher to matcher tree
            self.handlers.insert(handler, 0)
            matcher = Matcher.new(self.rule,
                                  self.scope,
                                  self.permission,
                                  self.block,
                                  self.handlers,
                                  temp=True,
                                  default_state=self.state,
                                  default_parser=self._default_parser,
                                  args_parser=self._args_parser)
            return
        except PausedException:
            # TODO: add tmp matcher to matcher tree
            matcher = Matcher.new(self.rule,
                                  self.scope,
                                  self.permission,
                                  self.block,
                                  self.handlers,
                                  temp=True,
                                  default_state=self.state,
                                  default_parser=self._default_parser,
                                  args_parser=self._args_parser)
            return
        except FinishedException:
            return


def on_message(rule: Rule,
               scope="ALL",
               permission="ALL",
               block=True,
               *,
               handlers=[],
               temp=False,
               state={}) -> Type[Matcher]:
    # TODO: add matcher to matcher tree
    return Matcher.new(rule,
                       scope,
                       permission,
                       block,
                       handlers=handlers,
                       temp=temp,
                       default_state=state)


def on_startswith(msg,
                  start: int = None,
                  end: int = None,
                  rule: Optional[Rule] = None,
                  **kwargs) -> Type[Matcher]:
    return on_message(startswith(msg, start, end) &
                      rule, **kwargs) if rule else on_message(
                          startswith(msg, start, end), **kwargs)


def on_regex(pattern,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = None,
             **kwargs) -> Type[Matcher]:
    return on_message(regex(pattern, flags) &
                      rule, **kwargs) if rule else on_message(
                          regex(pattern, flags), **kwargs)
