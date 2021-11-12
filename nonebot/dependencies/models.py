from enum import Enum
from typing import Any, List, Callable, Optional

from pydantic.fields import Required, FieldInfo, ModelField

from nonebot.utils import get_name


class Depends:

    def __init__(self,
                 dependency: Optional[Callable[..., Any]] = None,
                 *,
                 use_cache: bool = True) -> None:
        self.dependency = dependency
        self.use_cache = use_cache

    def __repr__(self) -> str:
        dep = get_name(self.dependency)
        cache = "" if self.use_cache else ", use_cache=False"
        return f"{self.__class__.__name__}({dep}{cache})"


class Dependent:

    def __init__(self,
                 *,
                 func: Optional[Callable[..., Any]] = None,
                 name: Optional[str] = None,
                 bot_param: Optional[ModelField] = None,
                 event_param: Optional[ModelField] = None,
                 state_param: Optional[ModelField] = None,
                 matcher_param: Optional[ModelField] = None,
                 simple_params: Optional[List[ModelField]] = None,
                 dependencies: Optional[List["Dependent"]] = None,
                 use_cache: bool = True) -> None:
        self.func = func
        self.name = name
        self.bot_param = bot_param
        self.event_param = event_param
        self.state_param = state_param
        self.matcher_param = matcher_param
        self.simple_params = simple_params or []
        self.dependencies = dependencies or []
        self.use_cache = use_cache
        self.cache_key = (self.func,)


class ParamTypes(Enum):
    BOT = "bot"
    EVENT = "event"
    STATE = "state"
    MATCHER = "matcher"
    SIMPLE = "simple"


class Param(FieldInfo):
    in_: ParamTypes

    def __init__(self, default: Any):
        super().__init__(default=default)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class BotParam(Param):
    in_ = ParamTypes.BOT


class EventParam(Param):
    in_ = ParamTypes.EVENT


class StateParam(Param):
    in_ = ParamTypes.STATE


class MatcherParam(Param):
    in_ = ParamTypes.MATCHER


class SimpleParam(Param):
    in_ = ParamTypes.SIMPLE

    def __init__(self, default: Any):
        if default is Required:
            raise ValueError("SimpleParam should be given a default value")
        super().__init__(default)
