import inspect
from typing import Any, Dict, Optional

from pydantic.fields import Undefined

from nonebot.typing import T_State
from nonebot.dependencies import Param
from nonebot.adapters import Bot, Event
from nonebot.utils import generic_check_issubclass


class BotParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Bot) or (
            param.annotation == param.empty and name == "bot"
        )

    def _solve(self, bot: Bot, **kwargs: Any) -> Any:
        return bot


class EventParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Event) or (
            param.annotation == param.empty and name == "event"
        )

    def _solve(self, event: Event, **kwargs: Any) -> Any:
        return event


class StateParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Dict) or (
            param.annotation == param.empty and name == "state"
        )

    def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class MatcherParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Matcher) or (
            param.annotation == param.empty and name == "matcher"
        )

    def _solve(self, matcher: Optional["Matcher"] = None, **kwargs: Any) -> Any:
        return matcher


class ExceptionParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Exception) or (
            param.annotation == param.empty and name == "exception"
        )

    def _solve(self, exception: Optional[Exception] = None, **kwargs: Any) -> Any:
        return exception


class DefaultParam(Param):
    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return param.default != param.empty

    def _solve(self, **kwargs: Any) -> Any:
        return Undefined


from nonebot.matcher import Matcher
