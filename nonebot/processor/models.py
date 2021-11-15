from typing import Any, List, Callable, Optional

from pydantic.fields import ModelField

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
                 params: Optional[List[ModelField]] = None,
                 dependencies: Optional[List["Dependent"]] = None,
                 use_cache: bool = True) -> None:
        self.func = func
        self.name = name
        self.params = params or []
        self.dependencies = dependencies or []
        self.use_cache = use_cache
        self.cache_key = self.func
