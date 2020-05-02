import re
import copy
from functools import wraps
from typing import Union, Optional

from .rule import Rule, startswith, regex, user
from .typing import Scope, Handler
from .exception import BlockedException, RejectedException


class Matcher:

    def __init__(self,
                 rule: Rule,
                 scope: Scope = "ALL",
                 permission: str = "ALL",
                 block: bool = True,
                 *,
                 handlers: list = [],
                 state: dict = {},
                 temp: bool = False):
        self.rule = rule
        self.scope = scope
        self.permission = permission
        self.block = block
        self.handlers = handlers
        self.state = state
        self.temp = temp

        def _default_parser(event: "Event", state: dict):
            state[state.pop("_current_arg")] = event.message

        self._args_parser = _default_parser

    def __call__(self, func: Handler) -> Handler:
        self.handlers.append(func)

        # TODO: export some functions
        func.args_parser = self.args_parser
        func.receive = self.receive
        func.got = self.got

        return func

    def args_parser(self, func):
        self._args_parser = func
        return func

    def receive(self):

        def _decorator(func: Handler) -> Handler:

            @wraps(func)
            def _handler(event: "Event", state: dict):
                # TODO: add tmp matcher to matcher tree
                matcher = Matcher(user(event.user_id) & self.rule,
                                  scope=self.scope,
                                  permission=self.permission,
                                  block=self.block,
                                  handlers=self.handlers,
                                  state=state,
                                  temp=True)
                matcher.args_parser(self._args_parser)
                raise BlockedException

            self.handlers.append(_handler)

            return func

        return _decorator

    def got(self, key, args_parser=None):

        def _decorator(func: Handler) -> Handler:

            @wraps(func)
            def _handler(event: "Event", state: dict):
                if key not in state:
                    state["_current_arg"] = key

                    # TODO: add tmp matcher to matcher tree
                    matcher = copy.copy(self)
                    raise RejectedException
                return func(event, state)

            self.handlers.append(_handler)

            return func

        return _decorator

    def finish(self):
        # BlockedException用于阻止后续handler继续执行
        raise BlockedException

    def reject(self):
        # RejectedException用于阻止后续handler继续执行并将当前handler放回队列
        raise RejectedException


def on_message(rule: Rule,
               scope="ALL",
               permission="ALL",
               block=True,
               *,
               handlers=[],
               state={},
               temp=False) -> Matcher:
    # TODO: add matcher to matcher tree
    return Matcher(rule,
                   scope,
                   permission,
                   block,
                   handlers=handlers,
                   state=state,
                   temp=temp)


def on_startswith(msg,
                  start: int = None,
                  end: int = None,
                  rule: Optional[Rule] = None,
                  **kwargs) -> Matcher:
    return on_message(startswith(msg, start, end) &
                      rule, **kwargs) if rule else on_message(
                          startswith(msg, start, end), **kwargs)


def on_regex(pattern,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = None,
             **kwargs) -> Matcher:
    return on_message(regex(pattern, flags) &
                      rule, **kwargs) if rule else on_message(
                          regex(pattern, flags), **kwargs)
