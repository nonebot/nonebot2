import abc
import inspect
from typing import Any, List, Type, Optional

from pydantic.fields import FieldInfo, ModelField

from nonebot.utils import get_name
from nonebot.typing import T_Handler


class Param(abc.ABC, FieldInfo):

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


class DependsWrapper:

    def __init__(self,
                 dependency: Optional[T_Handler] = None,
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
                 func: Optional[T_Handler] = None,
                 name: Optional[str] = None,
                 params: Optional[List[ModelField]] = None,
                 allow_types: Optional[List[Type[Param]]] = None,
                 dependencies: Optional[List["Dependent"]] = None,
                 use_cache: bool = True) -> None:
        self.func = func
        self.name = name
        self.params = params or []
        self.allow_types = allow_types or []
        self.dependencies = dependencies or []
        self.use_cache = use_cache
        self.cache_key = self.func
