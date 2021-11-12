import inspect
from typing import Any, Callable, Optional

from .models import Dependent
from .models import Depends as Depends
from nonebot.adapters import Bot, Event
from .utils import get_typed_signature, generic_check_issubclass


def get_param_sub_dependent(*, param: inspect.Parameter) -> Dependent:
    depends: Depends = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    return get_sub_dependant(
        depends=depends,
        dependency=dependency,
        name=param.name,
    )


def get_parameterless_sub_dependant(*, depends: Depends) -> Dependent:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends, dependency=depends.dependency)


def get_sub_dependant(
    *,
    depends: Depends,
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
        if isinstance(param.default, Depends):
            sub_dependent = get_param_sub_dependent(param=param)
            dependent.dependencies.append(sub_dependent)
            continue

        if generic_check_issubclass(param.annotation, Bot):
            dependent.bot_param_name = param_name
            continue
        elif generic_check_issubclass(param.annotation, Event):
            dependent.event_param_name = param_name
            continue
        elif generic_check_issubclass(param.annotation, dict):
            dependent.state_param_name = param_name
            continue
        elif generic_check_issubclass(param.annotation, Matcher):
            dependent.matcher_param_name = param_name
            continue

        raise ValueError(
            f"Unknown parameter {param_name} with type {param.annotation}")

    return dependent


from .handler import Handler as Handler
from .matcher import Matcher as Matcher
