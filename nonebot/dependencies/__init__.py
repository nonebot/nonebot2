"""本模块模块实现了依赖注入的定义与处理。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 0
    description: nonebot.dependencies 模块
"""

import abc
from collections.abc import Awaitable, Iterable
from dataclasses import dataclass, field
from functools import partial
import inspect
from typing import Any, Callable, Generic, Optional, TypeVar, cast

import anyio
from exceptiongroup import BaseExceptionGroup, catch

from nonebot.compat import FieldInfo, ModelField, PydanticUndefined
from nonebot.exception import SkippedException
from nonebot.log import logger
from nonebot.typing import _DependentCallable
from nonebot.utils import (
    flatten_exception_group,
    is_coroutine_callable,
    run_coro_with_shield,
    run_sync,
)

from .utils import check_field_type, get_typed_signature

R = TypeVar("R")
T = TypeVar("T", bound="Dependent")


class Param(abc.ABC, FieldInfo):
    """依赖注入的基本单元 —— 参数。

    继承自 `pydantic.fields.FieldInfo`，用于描述参数信息（不包括参数名）。
    """

    def __init__(self, *args, validate: bool = False, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.validate = validate

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type["Param"], ...]
    ) -> Optional["Param"]:
        return

    @classmethod
    def _check_parameterless(
        cls, value: Any, allow_types: tuple[type["Param"], ...]
    ) -> Optional["Param"]:
        return

    @abc.abstractmethod
    async def _solve(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _check(self, **kwargs: Any) -> None:
        return


@dataclass(frozen=True)
class Dependent(Generic[R]):
    """依赖注入容器

    参数:
        call: 依赖注入的可调用对象，可以是任何 Callable 对象
        pre_checkers: 依赖注入解析前的参数检查
        params: 具名参数列表
        parameterless: 匿名参数列表
        allow_types: 允许的参数类型
    """

    call: _DependentCallable[R]
    params: tuple[ModelField, ...] = field(default_factory=tuple)
    parameterless: tuple[Param, ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        if inspect.isfunction(self.call) or inspect.isclass(self.call):
            call_str = self.call.__name__
        else:
            call_str = repr(self.call)
        return (
            f"Dependent(call={call_str}"
            + (f", parameterless={self.parameterless}" if self.parameterless else "")
            + ")"
        )

    async def __call__(self, **kwargs: Any) -> R:
        exception: Optional[BaseExceptionGroup[SkippedException]] = None

        def _handle_skipped(exc_group: BaseExceptionGroup[SkippedException]):
            nonlocal exception
            exception = exc_group
            # raise one of the exceptions instead
            excs = list(flatten_exception_group(exc_group))
            logger.trace(f"{self} skipped due to {excs}")

        with catch({SkippedException: _handle_skipped}):
            # do pre-check
            await self.check(**kwargs)

            # solve param values
            values = await self.solve(**kwargs)

            # call function
            if is_coroutine_callable(self.call):
                return await cast(Callable[..., Awaitable[R]], self.call)(**values)
            else:
                return await run_sync(cast(Callable[..., R], self.call))(**values)

        raise exception

    @staticmethod
    def parse_params(
        call: _DependentCallable[R], allow_types: tuple[type[Param], ...]
    ) -> tuple[ModelField, ...]:
        fields: list[ModelField] = []
        params = get_typed_signature(call).parameters.values()

        for param in params:
            if isinstance(param.default, Param):
                field_info = param.default
            else:
                for allow_type in allow_types:
                    if field_info := allow_type._check_param(param, allow_types):
                        break
                else:
                    raise ValueError(
                        f"Unknown parameter {param.name} "
                        f"for function {call} with type {param.annotation}"
                    )

            annotation: Any = Any
            if param.annotation is not param.empty:
                annotation = param.annotation

            fields.append(
                ModelField.construct(
                    name=param.name, annotation=annotation, field_info=field_info
                )
            )

        return tuple(fields)

    @staticmethod
    def parse_parameterless(
        parameterless: tuple[Any, ...], allow_types: tuple[type[Param], ...]
    ) -> tuple[Param, ...]:
        parameterless_params: list[Param] = []
        for value in parameterless:
            for allow_type in allow_types:
                if param := allow_type._check_parameterless(value, allow_types):
                    break
            else:
                raise ValueError(f"Unknown parameterless {value}")
            parameterless_params.append(param)
        return tuple(parameterless_params)

    @classmethod
    def parse(
        cls,
        *,
        call: _DependentCallable[R],
        parameterless: Optional[Iterable[Any]] = None,
        allow_types: Iterable[type[Param]],
    ) -> "Dependent[R]":
        allow_types = tuple(allow_types)

        params = cls.parse_params(call, allow_types)
        parameterless_params = (
            ()
            if parameterless is None
            else cls.parse_parameterless(tuple(parameterless), allow_types)
        )

        return cls(call, params, parameterless_params)

    async def check(self, **params: Any) -> None:
        if self.parameterless:
            async with anyio.create_task_group() as tg:
                for param in self.parameterless:
                    tg.start_soon(partial(param._check, **params))

        if self.params:
            async with anyio.create_task_group() as tg:
                for param in self.params:
                    tg.start_soon(
                        partial(cast(Param, param.field_info)._check, **params)
                    )

    async def _solve_field(self, field: ModelField, params: dict[str, Any]) -> Any:
        param = cast(Param, field.field_info)
        value = await param._solve(**params)
        if value is PydanticUndefined:
            value = field.get_default()
        v = check_field_type(field, value)
        return v if param.validate else value

    async def solve(self, **params: Any) -> dict[str, Any]:
        # solve parameterless
        for param in self.parameterless:
            await param._solve(**params)

        # solve param values
        result: dict[str, Any] = {}
        if not self.params:
            return result

        async def _solve_field(field: ModelField, params: dict[str, Any]) -> None:
            value = await self._solve_field(field, params)
            result[field.name] = value

        async with anyio.create_task_group() as tg:
            for field in self.params:
                # shield the task to prevent cancellation
                # when one of the tasks raises an exception
                # this will improve the dependency cache reusability
                tg.start_soon(run_coro_with_shield, _solve_field(field, params))

        return result


__autodoc__ = {"CustomConfig": False}
