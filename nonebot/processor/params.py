import abc
import inspect
from enum import Enum
from typing import Any, Dict, Optional

from pydantic.fields import FieldInfo

from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .utils import generic_check_issubclass


class Param(FieldInfo, abc.ABC):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    @abc.abstractmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _solve(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class BotParam(Param):

    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Bot)

    def _solve(self, bot: Bot, **kwargs: Any) -> Any:
        return bot


class EventParam(Param):

    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Event)

    def _solve(self, event: Event, **kwargs: Any) -> Any:
        return event


class StateParam(Param):

    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Dict)

    def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class MatcherParam(Param):

    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Matcher)

    def _solve(self, matcher: Optional["Matcher"] = None, **kwargs: Any) -> Any:
        return matcher


class ExceptionParam(Param):

    @classmethod
    def _check(cls, name: str, param: inspect.Parameter) -> bool:
        return generic_check_issubclass(param.annotation, Exception)

    def _solve(self,
               exception: Optional[Exception] = None,
               **kwargs: Any) -> Any:
        return exception


class ParamTypes(Enum):
    BOT = BotParam
    EVENT = EventParam
    STATE = StateParam
    MATCHER = MatcherParam
    EXCEPTION = ExceptionParam


from .matcher import Matcher
