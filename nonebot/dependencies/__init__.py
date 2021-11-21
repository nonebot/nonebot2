"""
依赖注入处理模块
===============

该模块实现了依赖注入的定义与处理。
"""

import inspect
from itertools import chain
from typing import Any, Dict, List, Type, Tuple, Callable, Optional, cast
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager

from pydantic import BaseConfig
from pydantic.fields import Required, ModelField
from pydantic.schema import get_annotation_from_field_info

from nonebot.log import logger
from .models import Param as Param
from .utils import get_typed_signature
from .models import Dependent as Dependent
from nonebot.exception import SkippedException
from .models import DependsWrapper as DependsWrapper
from nonebot.typing import T_Handler, T_DependencyCache
from nonebot.utils import (CacheLock, run_sync, is_gen_callable,
                           run_sync_ctx_manager, is_async_gen_callable,
                           is_coroutine_callable)

cache_lock = CacheLock()


class CustomConfig(BaseConfig):
    arbitrary_types_allowed = True


def get_param_sub_dependent(
        *,
        param: inspect.Parameter,
        allow_types: Optional[List[Type[Param]]] = None) -> Dependent:
    depends: DependsWrapper = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    return get_sub_dependant(depends=depends,
                             dependency=dependency,
                             name=param.name,
                             allow_types=allow_types)


def get_parameterless_sub_dependant(
        *,
        depends: DependsWrapper,
        allow_types: Optional[List[Type[Param]]] = None) -> Dependent:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends,
                             dependency=depends.dependency,
                             allow_types=allow_types)


def get_sub_dependant(
        *,
        depends: DependsWrapper,
        dependency: T_Handler,
        name: Optional[str] = None,
        allow_types: Optional[List[Type[Param]]] = None) -> Dependent:
    sub_dependant = get_dependent(func=dependency,
                                  name=name,
                                  use_cache=depends.use_cache,
                                  allow_types=allow_types)
    return sub_dependant


def get_dependent(*,
                  func: T_Handler,
                  name: Optional[str] = None,
                  use_cache: bool = True,
                  allow_types: Optional[List[Type[Param]]] = None) -> Dependent:
    signature = get_typed_signature(func)
    params = signature.parameters
    dependent = Dependent(func=func,
                          name=name,
                          allow_types=allow_types,
                          use_cache=use_cache)
    for param_name, param in params.items():
        if isinstance(param.default, DependsWrapper):
            sub_dependent = get_param_sub_dependent(param=param,
                                                    allow_types=allow_types)
            dependent.dependencies.append(sub_dependent)
            continue

        for allow_type in dependent.allow_types:
            if allow_type._check(param_name, param):
                field_info = allow_type(param.default)
                break
        else:
            raise ValueError(
                f"Unknown parameter {param_name} for function {func} with type {param.annotation}"
            )

        annotation: Any = Any
        if param.annotation != param.empty:
            annotation = param.annotation
        annotation = get_annotation_from_field_info(annotation, field_info,
                                                    param_name)
        dependent.params.append(
            ModelField(name=param_name,
                       type_=annotation,
                       class_validators=None,
                       model_config=CustomConfig,
                       default=Required,
                       required=True,
                       field_info=field_info))

    return dependent


async def solve_dependencies(
        *,
        _dependent: Dependent,
        _stack: Optional[AsyncExitStack] = None,
        _sub_dependents: Optional[List[Dependent]] = None,
        _dependency_overrides_provider: Optional[Any] = None,
        _dependency_cache: Optional[T_DependencyCache] = None,
        **params: Any) -> Tuple[Dict[str, Any], T_DependencyCache]:
    values: Dict[str, Any] = {}
    dependency_cache = {} if _dependency_cache is None else _dependency_cache

    # solve sub dependencies
    sub_dependent: Dependent
    for sub_dependent in chain(_sub_dependents or tuple(),
                               _dependent.dependencies):
        sub_dependent.func = cast(Callable[..., Any], sub_dependent.func)
        sub_dependent.cache_key = cast(Callable[..., Any],
                                       sub_dependent.cache_key)
        func = sub_dependent.func

        # dependency overrides
        use_sub_dependant = sub_dependent
        if (_dependency_overrides_provider and hasattr(
                _dependency_overrides_provider, "dependency_overrides")):
            original_call = sub_dependent.func
            func = getattr(_dependency_overrides_provider,
                           "dependency_overrides",
                           {}).get(original_call, original_call)
            use_sub_dependant = get_dependent(
                func=func,
                name=sub_dependent.name,
                allow_types=sub_dependent.allow_types,
            )

        # solve sub dependency with current cache
        solved_result = await solve_dependencies(
            _dependent=use_sub_dependant,
            _dependency_overrides_provider=_dependency_overrides_provider,
            _dependency_cache=dependency_cache,
            **params)
        sub_values, sub_dependency_cache = solved_result
        # update cache?
        # dependency_cache.update(sub_dependency_cache)

        # run dependency function
        async with cache_lock:
            if sub_dependent.use_cache and sub_dependent.cache_key in dependency_cache:
                solved = dependency_cache[sub_dependent.cache_key]
            elif is_gen_callable(func) or is_async_gen_callable(func):
                assert isinstance(
                    _stack, AsyncExitStack
                ), "Generator dependency should be called in context"
                if is_gen_callable(func):
                    cm = run_sync_ctx_manager(
                        contextmanager(func)(**sub_values))
                else:
                    cm = asynccontextmanager(func)(**sub_values)
                solved = await _stack.enter_async_context(cm)
            elif is_coroutine_callable(func):
                solved = await func(**sub_values)
            else:
                solved = await run_sync(func)(**sub_values)

            # parameter dependency
            if sub_dependent.name is not None:
                values[sub_dependent.name] = solved
            # save current dependency to cache
            if sub_dependent.cache_key not in dependency_cache:
                dependency_cache[sub_dependent.cache_key] = solved

    # usual dependency
    for field in _dependent.params:
        field_info = field.field_info
        assert isinstance(field_info,
                          Param), "Params must be subclasses of Param"
        value = field_info._solve(**params)
        _, errs_ = field.validate(value,
                                  values,
                                  loc=(str(field_info), field.alias))
        if errs_:
            logger.debug(
                f"{field_info} "
                f"type {type(value)} not match depends {_dependent.func} "
                f"annotation {field._type_display()}, ignored")
            raise SkippedException
        else:
            values[field.name] = value

    return values, dependency_cache


def Depends(dependency: Optional[T_Handler] = None,
            *,
            use_cache: bool = True) -> Any:
    """
    :说明:

      参数依赖注入装饰器

    :参数:

      * ``dependency: Optional[Callable[..., Any]] = None``: 依赖函数。默认为参数的类型注释。
      * ``use_cache: bool = True``: 是否使用缓存。默认为 ``True``。
    """
    return DependsWrapper(dependency=dependency, use_cache=use_cache)
