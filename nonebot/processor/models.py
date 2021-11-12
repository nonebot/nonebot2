from typing import Any, List, Callable, Optional

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
                 bot_param_name: Optional[str] = None,
                 event_param_name: Optional[str] = None,
                 state_param_name: Optional[str] = None,
                 matcher_param_name: Optional[str] = None,
                 dependencies: Optional[List["Dependent"]] = None,
                 use_cache: bool = True) -> None:
        self.func = func
        self.name = name
        self.bot_param_name = bot_param_name
        self.event_param_name = event_param_name
        self.state_param_name = state_param_name
        self.matcher_param_name = matcher_param_name
        self.dependencies = dependencies or []
        self.use_cache = use_cache
        self.cache_key = (self.func,)
