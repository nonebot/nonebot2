import inspect
from typing import Any, Dict

from loguru import logger
from pydantic.typing import ForwardRef, evaluate_forwardref

from nonebot.typing import T_Handler


def get_typed_signature(func: T_Handler) -> inspect.Signature:
    signature = inspect.signature(func)
    globalns = getattr(func, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        try:
            annotation = evaluate_forwardref(annotation, globalns, globalns)
        except Exception as e:
            logger.opt(colors=True, exception=e).warning(
                f'Unknown ForwardRef["{param.annotation}"] for parameter {param.name}'
            )
            return inspect.Parameter.empty
    return annotation
