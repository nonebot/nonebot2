import inspect
from typing import Any, Dict, Type, Tuple, Union, Callable
from typing_extensions import GenericAlias, get_args, get_origin  # type: ignore

from loguru import logger
from pydantic.typing import ForwardRef, evaluate_forwardref


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        ) for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str,
                                                                  Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        try:
            annotation = evaluate_forwardref(annotation, globalns, globalns)
        except Exception as e:
            logger.opt(colors=True, exception=e).warning(
                f"Unknown ForwardRef[\"{param.annotation}\"] for parameter {param.name}"
            )
            return inspect.Parameter.empty
    return annotation


def generic_check_issubclass(
        cls: Any, class_or_tuple: Union[Type[Any], Tuple[Type[Any],
                                                         ...]]) -> bool:
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        if get_origin(cls) is Union:
            for type_ in get_args(cls):
                if not generic_check_issubclass(type_, class_or_tuple):
                    return False
            return True
        elif isinstance(cls, GenericAlias):
            origin = get_origin(cls)
            return bool(origin and issubclass(origin, class_or_tuple))
        raise


def generic_get_types(cls: Any) -> Tuple[Type[Any], ...]:
    if get_origin(cls) is Union:
        return get_args(cls)
    return (cls,)
