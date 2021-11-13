import inspect
from itertools import chain
from typing import Any, Dict, List, Tuple, Callable, Optional, cast

from .models import Dependent
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .models import Depends as DependsClass
from nonebot.utils import run_sync, is_coroutine_callable
from .utils import (generic_get_types, get_typed_signature,
                    generic_check_issubclass)


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


def get_parameterless_sub_dependant(*, depends: DependsClass) -> Dependent:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends, dependency=depends.dependency)


def get_sub_dependant(
    *,
    depends: DependsClass,
    dependency: Callable[..., Any],
    name: Optional[str] = None,
) -> Dependent:
    sub_dependant = get_dependent(
        func=dependency,
        name=name,
        use_cache=depends.use_cache,
    )
    return sub_dependant


def get_dependent(*,
                  func: Callable[..., Any],
                  name: Optional[str] = None,
                  use_cache: bool = True) -> Dependent:
    signature = get_typed_signature(func)
    params = signature.parameters
    dependent = Dependent(func=func, name=name, use_cache=use_cache)
    for param_name, param in params.items():
        if isinstance(param.default, DependsClass):
            sub_dependent = get_param_sub_dependent(param=param)
            dependent.dependencies.append(sub_dependent)
            continue

        if generic_check_issubclass(param.annotation, Bot):
            if dependent.bot_param_name is not None:
                raise ValueError(f"{func} has more than one Bot parameter: "
                                 f"{dependent.bot_param_name} / {param_name}")
            dependent.bot_param_name = param_name
            dependent.bot_param_type = generic_get_types(param.annotation)
        elif generic_check_issubclass(param.annotation, Event):
            if dependent.event_param_name is not None:
                raise ValueError(f"{func} has more than one Event parameter: "
                                 f"{dependent.event_param_name} / {param_name}")
            dependent.event_param_name = param_name
            dependent.event_param_type = generic_get_types(param.annotation)
        elif generic_check_issubclass(param.annotation, dict):
            if dependent.state_param_name is not None:
                raise ValueError(f"{func} has more than one State parameter: "
                                 f"{dependent.state_param_name} / {param_name}")
            dependent.state_param_name = param_name
        elif generic_check_issubclass(param.annotation, Matcher):
            if dependent.matcher_param_name is not None:
                raise ValueError(
                    f"{func} has more than one Matcher parameter: "
                    f"{dependent.matcher_param_name} / {param_name}")
            dependent.matcher_param_name = param_name
        else:
            raise ValueError(
                f"Unknown parameter {param_name} with type {param.annotation}")

    return dependent


async def solve_dependencies(
    *,
    dependent: Dependent,
    bot: Bot,
    event: Event,
    state: T_State,
    matcher: "Matcher",
    sub_dependents: Optional[List[Dependent]] = None,
    dependency_overrides_provider: Optional[Any] = None,
    dependency_cache: Optional[Dict[Tuple[Callable[..., Any]], Any]] = None,
) -> Tuple[Dict[str, Any], Dict[Tuple[Callable[..., Any]], Any], bool]:
    values: Dict[str, Any] = {}
    dependency_cache = dependency_cache or {}

    # solve sub dependencies
    sub_dependent: Dependent
    for sub_dependent in chain(sub_dependents or tuple(),
                               dependent.dependencies):
        sub_dependent.func = cast(Callable[..., Any], sub_dependent.func)
        sub_dependent.cache_key = cast(Tuple[Callable[..., Any]],
                                       sub_dependent.cache_key)
        func = sub_dependent.func

        # check bot and event type
        if sub_dependent.bot_param_type and not isinstance(
                bot, sub_dependent.bot_param_type):
            return values, dependency_cache, True
        elif sub_dependent.event_param_type and not isinstance(
                event, sub_dependent.event_param_type):
            return values, dependency_cache, True

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
    if dependent.bot_param_name is not None:
        values[dependent.bot_param_name] = bot
    if dependent.event_param_name is not None:
        values[dependent.event_param_name] = event
    if dependent.state_param_name is not None:
        values[dependent.state_param_name] = state
    if dependent.matcher_param_name is not None:
        values[dependent.matcher_param_name] = matcher
    return values, dependency_cache, False


def Depends(dependency: Optional[Callable[..., Any]] = None,
            *,
            use_cache: bool = True) -> Any:
    return DependsClass(dependency=dependency, use_cache=use_cache)


from .handler import Handler as Handler
from .matcher import Matcher as Matcher
from .matcher import matchers as matchers
