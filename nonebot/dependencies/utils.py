"""
FrontMatter:
    sidebar_position: 1
    description: nonebot.dependencies.utils 模块
"""

import inspect
from typing import Any, Dict, Callable, ForwardRef

from loguru import logger

from nonebot.exception import TypeMisMatch
from nonebot.typing import evaluate_forwardref
from nonebot._compat import PYDANTIC_V2, ConfigDict, ModelField


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """获取可调用对象签名"""

    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    """获取参数的类型注解"""

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


if PYDANTIC_V2:  # pragma: pydantic-v2
    CONFIG = ConfigDict(arbitrary_types_allowed=True)
else:  # pragma: pydantic-v1

    class CONFIG(ConfigDict):
        arbitrary_types_allowed: bool = True


def check_field_type(field: ModelField, value: Any) -> Any:
    """检查字段类型是否匹配"""

    try:
        return field.validate(value, CONFIG)
    except ValueError:
        raise TypeMisMatch(field, value)
