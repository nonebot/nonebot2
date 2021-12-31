"""
依赖注入处理模块
================

该模块实现了依赖注入的定义与处理。
"""

import abc
import inspect
from typing import Any, Dict, List, Type, Generic, TypeVar, Callable, Optional

from pydantic import BaseConfig
from pydantic.schema import get_annotation_from_field_info
from pydantic.fields import Required, FieldInfo, Undefined, ModelField

from nonebot.log import logger
from .utils import get_typed_signature
from nonebot.exception import TypeMisMatch
from nonebot.utils import run_sync, is_coroutine_callable

T = TypeVar("T", bound="Dependent")
R = TypeVar("R")


class Param(abc.ABC, FieldInfo):
    @classmethod
    def _check_param(
        cls, dependent: "Dependent", name: str, param: inspect.Parameter
    ) -> Optional["Param"]:
        return None

    @classmethod
    def _check_parameterless(
        cls, dependent: "Dependent", value: Any
    ) -> Optional["Param"]:
        return None

    @abc.abstractmethod
    async def _solve(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class CustomConfig(BaseConfig):
    arbitrary_types_allowed = True


class Dependent(Generic[R]):
    def __init__(
        self,
        *,
        call: Callable[..., Any],
        pre_checkers: Optional[List[Param]] = None,
        params: Optional[List[ModelField]] = None,
        parameterless: Optional[List[Param]] = None,
        allow_types: Optional[List[Type[Param]]] = None,
    ) -> None:
        self.call = call
        self.pre_checkers = pre_checkers or []
        self.params = params or []
        self.parameterless = parameterless or []
        self.allow_types = allow_types or []

    def __repr__(self) -> str:
        return (
            f"<Dependent call={self.call}, params={self.params},"
            f" parameterless={self.parameterless}>"
        )

    def __str__(self) -> str:
        return self.__repr__()

    async def __call__(self, **kwargs: Any) -> R:
        values = await self.solve(**kwargs)

        if is_coroutine_callable(self.call):
            return await self.call(**values)
        else:
            return await run_sync(self.call)(**values)

    def parse_param(self, name: str, param: inspect.Parameter) -> Param:
        for allow_type in self.allow_types:
            field_info = allow_type._check_param(self, name, param)
            if field_info:
                return field_info
        else:
            raise ValueError(
                f"Unknown parameter {name} for function {self.call} with type {param.annotation}"
            )

    def parse_parameterless(self, value: Any) -> Param:
        for allow_type in self.allow_types:
            field_info = allow_type._check_parameterless(self, value)
            if field_info:
                return field_info
        else:
            raise ValueError(
                f"Unknown parameterless {value} for function {self.call} with type {type(value)}"
            )

    def prepend_parameterless(self, value: Any) -> None:
        self.parameterless.insert(0, self.parse_parameterless(value))

    def append_parameterless(self, value: Any) -> None:
        self.parameterless.append(self.parse_parameterless(value))

    @classmethod
    def parse(
        cls: Type[T],
        *,
        call: Callable[..., Any],
        parameterless: Optional[List[Any]] = None,
        allow_types: Optional[List[Type[Param]]] = None,
    ) -> T:
        signature = get_typed_signature(call)
        params = signature.parameters
        dependent = cls(
            call=call,
            allow_types=allow_types,
        )

        for param_name, param in params.items():
            default_value = Required
            if param.default != param.empty:
                default_value = param.default

            if isinstance(default_value, Param):
                field_info = default_value
                default_value = field_info.default
            else:
                field_info = dependent.parse_param(param_name, param)
                default_value = field_info.default

            annotation: Any = Any
            required = default_value == Required
            if param.annotation != param.empty:
                annotation = param.annotation
            annotation = get_annotation_from_field_info(
                annotation, field_info, param_name
            )
            dependent.params.append(
                ModelField(
                    name=param_name,
                    type_=annotation,
                    class_validators=None,
                    model_config=CustomConfig,
                    default=None if required else default_value,
                    required=required,
                    field_info=field_info,
                )
            )

        parameterless_params = [
            dependent.parse_parameterless(param) for param in (parameterless or [])
        ]
        dependent.parameterless.extend(parameterless_params)

        logger.trace(
            f"Parsed dependent with call={call}, "
            f"params={[param.field_info for param in dependent.params]}, "
            f"parameterless={dependent.parameterless}"
        )

        return dependent

    async def solve(
        self,
        **params: Any,
    ) -> Dict[str, Any]:
        values: Dict[str, Any] = {}

        for checker in self.pre_checkers:
            await checker._solve(**params)

        for param in self.parameterless:
            await param._solve(**params)

        for field in self.params:
            field_info = field.field_info
            assert isinstance(field_info, Param), "Params must be subclasses of Param"
            value = await field_info._solve(**params)
            if value == Undefined:
                value = field.get_default()
            _, errs_ = field.validate(value, values, loc=(str(field_info), field.alias))
            if errs_:
                logger.debug(
                    f"{field_info} "
                    f"type {type(value)} not match depends {self.call} "
                    f"annotation {field._type_display()}, ignored"
                )
                raise TypeMisMatch(field, value)
            else:
                values[field.name] = value

        return values
