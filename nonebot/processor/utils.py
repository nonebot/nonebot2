import inspect
from typing import Any, Dict, Type, Tuple, Union, Callable

from pydantic.typing import (ForwardRef, GenericAlias, get_args, get_origin,
                             evaluate_forwardref)


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
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def generic_check_issubclass(
        cls: Any, class_or_tuple: Union[Type[Any], Tuple[Type[Any],
                                                         ...]]) -> bool:
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        if get_origin(cls) is Union:
            for type_ in get_args(cls):
                if not generic_check_issubclass(type_, class_or_tuple):
                    return False
            return True
        raise
