import inspect
from itertools import chain
from typing import Any, Dict, List, Type, Tuple, Callable, Optional, cast
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager

from pydantic import BaseConfig
from pydantic.fields import Required, ModelField
from pydantic.schema import get_annotation_from_field_info

from .models import Dependent
from nonebot.log import logger
from nonebot.typing import T_State
from .utils import get_typed_signature
from nonebot.adapters import Bot, Event
from .models import Depends as DependsClass
from nonebot.utils import (run_sync, is_gen_callable, run_sync_ctx_manager,
                           is_async_gen_callable, is_coroutine_callable)


def get_param_sub_dependent(*, param: inspect.Parameter) -> Dependent:
    depends: DependsClass = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    return get_sub_dependant(
        depends=depends,
        dependency=dependency,
        name=param.name,
    )


def get_parameterless_sub_dependant(
        *,
        depends: DependsClass,
        allow_types: Optional[List["ParamTypes"]] = None) -> Dependent:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends,
                             dependency=depends.dependency,
                             allow_types=allow_types)


def get_sub_dependant(
        *,
        depends: DependsClass,
        dependency: Callable[..., Any],
        name: Optional[str] = None,
        allow_types: Optional[List["ParamTypes"]] = None) -> Dependent:
    sub_dependant = get_dependent(func=dependency,
                                  name=name,
                                  use_cache=depends.use_cache,
                                  allow_types=allow_types)
    return sub_dependant


def get_dependent(
        *,
        func: Callable[..., Any],
        name: Optional[str] = None,
        use_cache: bool = True,
        allow_types: Optional[List["ParamTypes"]] = None) -> Dependent:
    signature = get_typed_signature(func)
    params = signature.parameters
    allow_types = allow_types or [
        ParamTypes.BOT, ParamTypes.EVENT, ParamTypes.STATE
    ]
    dependent = Dependent(func=func, name=name, use_cache=use_cache)
    for param_name, param in params.items():
        if isinstance(param.default, DependsClass):
            sub_dependent = get_param_sub_dependent(param=param)
            dependent.dependencies.append(sub_dependent)
            continue

        for allow_type in allow_types:
            field_info_class: Type[Param] = allow_type.value
            if field_info_class._check(param_name, param):
                field_info = field_info_class(param.default)
                break
        else:
            raise ValueError(
                f"Unknown parameter {param_name} with type {param.annotation}")

        annotation: Any = Any
        if param.annotation != param.empty:
            annotation = param.annotation
        annotation = get_annotation_from_field_info(annotation, field_info,
                                                    param_name)
        dependent.params.append(
            ModelField(name=param_name,
                       type_=annotation,
                       class_validators=None,
                       model_config=BaseConfig,
                       default=Required,
                       required=True,
                       field_info=field_info))

    return dependent


async def solve_dependencies(
    *,
    dependent: Dependent,
    bot: Bot,
    event: Event,
    state: T_State,
    matcher: Optional["Matcher"] = None,
    exception: Optional[Exception] = None,
    stack: Optional[AsyncExitStack] = None,
    sub_dependents: Optional[List[Dependent]] = None,
    dependency_overrides_provider: Optional[Any] = None,
    dependency_cache: Optional[Dict[Callable[..., Any], Any]] = None,
) -> Tuple[Dict[str, Any], Dict[Callable[..., Any], Any], bool]:
    values: Dict[str, Any] = {}
    dependency_cache = dependency_cache or {}

    # solve sub dependencies
    sub_dependent: Dependent
    for sub_dependent in chain(sub_dependents or tuple(),
                               dependent.dependencies):
        sub_dependent.func = cast(Callable[..., Any], sub_dependent.func)
        sub_dependent.cache_key = cast(Callable[..., Any],
                                       sub_dependent.cache_key)
        func = sub_dependent.func

        # dependency overrides
        use_sub_dependant = sub_dependent
        if (dependency_overrides_provider and
                hasattr(dependency_overrides_provider, "dependency_overrides")):
            original_call = sub_dependent.func
            func = getattr(dependency_overrides_provider,
                           "dependency_overrides",
                           {}).get(original_call, original_call)
            use_sub_dependant = get_dependent(
                func=func,
                name=sub_dependent.name,
            )

        # solve sub dependency with current cache
        solved_result = await solve_dependencies(
            dependent=use_sub_dependant,
            bot=bot,
            event=event,
            state=state,
            matcher=matcher,
            dependency_overrides_provider=dependency_overrides_provider,
            dependency_cache=dependency_cache,
        )
        sub_values, sub_dependency_cache, ignored = solved_result
        if ignored:
            return values, dependency_cache, True
        # update cache?
        dependency_cache.update(sub_dependency_cache)

        # run dependency function
        if sub_dependent.use_cache and sub_dependent.cache_key in dependency_cache:
            solved = dependency_cache[sub_dependent.cache_key]
        elif is_gen_callable(func) or is_async_gen_callable(func):
            assert isinstance(
                stack, AsyncExitStack
            ), "Generator dependency should be called in context"
            if is_gen_callable(func):
                cm = run_sync_ctx_manager(contextmanager(func)(**sub_values))
            else:
                cm = asynccontextmanager(func)(**sub_values)
            solved = await stack.enter_async_context(cm)
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
    for field in dependent.params:
        field_info = field.field_info
        assert isinstance(field_info,
                          Param), "Params must be subclasses of Param"
        value = field_info._solve(bot=bot,
                                  event=event,
                                  state=state,
                                  matcher=matcher,
                                  exception=exception)
        _, errs_ = field.validate(value,
                                  values,
                                  loc=(ParamTypes(type(field_info)).name,
                                       field.alias))
        if errs_:
            logger.debug(
                f"Matcher {matcher} {ParamTypes(type(field_info)).name} "
                f"type {type(value)} not match depends {dependent.func} "
                f"annotation {field._type_display()}, ignored")
            return values, dependency_cache, True
        else:
            values[field.name] = value

    return values, dependency_cache, False


def Depends(dependency: Optional[Callable[..., Any]] = None,
            *,
            use_cache: bool = True) -> Any:
    return DependsClass(dependency=dependency, use_cache=use_cache)


from .params import Param
from .handler import Handler as Handler
from .matcher import Matcher as Matcher
from .matcher import matchers as matchers
from .params import ParamTypes as ParamTypes
