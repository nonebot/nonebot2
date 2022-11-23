import asyncio
import inspect
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager
from typing import TYPE_CHECKING, Any, Type, Tuple, Literal, Callable, Optional, cast

from pydantic.fields import Required, Undefined, ModelField

from nonebot.dependencies.utils import check_field_type
from nonebot.dependencies import Param, Dependent, CustomConfig
from nonebot.typing import T_State, T_Handler, T_DependencyCache
from nonebot.utils import (
    get_name,
    run_sync,
    is_gen_callable,
    run_sync_ctx_manager,
    is_async_gen_callable,
    is_coroutine_callable,
    generic_check_issubclass,
)

if TYPE_CHECKING:
    from nonebot.matcher import Matcher
    from nonebot.adapters import Bot, Event


class DependsInner:
    def __init__(
        self,
        dependency: Optional[T_Handler] = None,
        *,
        use_cache: bool = True,
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache

    def __repr__(self) -> str:
        dep = get_name(self.dependency)
        cache = "" if self.use_cache else ", use_cache=False"
        return f"DependsInner({dep}{cache})"


def Depends(
    dependency: Optional[T_Handler] = None,
    *,
    use_cache: bool = True,
) -> Any:
    """子依赖装饰器

    参数:
        dependency: 依赖函数。默认为参数的类型注释。
        use_cache: 是否使用缓存。默认为 `True`。

    用法:
        ```python
        def depend_func() -> Any:
            return ...

        def depend_gen_func():
            try:
                yield ...
            finally:
                ...

        async def handler(param_name: Any = Depends(depend_func), gen: Any = Depends(depend_gen_func)):
            ...
        ```
    """
    return DependsInner(dependency, use_cache=use_cache)


class DependParam(Param):
    """子依赖参数"""

    def __repr__(self) -> str:
        return f"Depends({self.extra['dependent']})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["DependParam"]:
        if isinstance(param.default, DependsInner):
            dependency: T_Handler
            if param.default.dependency is None:
                assert param.annotation is not param.empty, "Dependency cannot be empty"
                dependency = param.annotation
            else:
                dependency = param.default.dependency
            sub_dependent = Dependent[Any].parse(
                call=dependency,
                allow_types=allow_types,
            )
            return cls(
                Required, use_cache=param.default.use_cache, dependent=sub_dependent
            )

    @classmethod
    def _check_parameterless(
        cls, value: Any, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["Param"]:
        if isinstance(value, DependsInner):
            assert value.dependency, "Dependency cannot be empty"
            dependent = Dependent[Any].parse(
                call=value.dependency, allow_types=allow_types
            )
            return cls(Required, use_cache=value.use_cache, dependent=dependent)

    async def _solve(
        self,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
        **kwargs: Any,
    ) -> Any:
        use_cache: bool = self.extra["use_cache"]
        dependency_cache = {} if dependency_cache is None else dependency_cache

        sub_dependent: Dependent = self.extra["dependent"]
        call = cast(Callable[..., Any], sub_dependent.call)

        # solve sub dependency with current cache
        sub_values = await sub_dependent.solve(
            stack=stack,
            dependency_cache=dependency_cache,
            **kwargs,
        )

        # run dependency function
        task: asyncio.Task[Any]
        if use_cache and call in dependency_cache:
            return await dependency_cache[call]
        elif is_gen_callable(call) or is_async_gen_callable(call):
            assert isinstance(
                stack, AsyncExitStack
            ), "Generator dependency should be called in context"
            if is_gen_callable(call):
                cm = run_sync_ctx_manager(contextmanager(call)(**sub_values))
            else:
                cm = asynccontextmanager(call)(**sub_values)
            task = asyncio.create_task(stack.enter_async_context(cm))
            dependency_cache[call] = task
            return await task
        elif is_coroutine_callable(call):
            task = asyncio.create_task(call(**sub_values))
            dependency_cache[call] = task
            return await task
        else:
            task = asyncio.create_task(run_sync(call)(**sub_values))
            dependency_cache[call] = task
            return await task

    async def _check(self, **kwargs: Any) -> None:
        # run sub dependent pre-checkers
        sub_dependent: Dependent = self.extra["dependent"]
        await sub_dependent.check(**kwargs)


class BotParam(Param):
    """{ref}`nonebot.adapters.Bot` 参数"""

    def __repr__(self) -> str:
        return (
            "BotParam("
            + (
                repr(cast(ModelField, checker).type_)
                if (checker := self.extra.get("checker"))
                else ""
            )
            + ")"
        )

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["BotParam"]:
        from nonebot.adapters import Bot

        if param.default == param.empty:
            if generic_check_issubclass(param.annotation, Bot):
                checker: Optional[ModelField] = None
                if param.annotation is not Bot:
                    checker = ModelField(
                        name=param.name,
                        type_=param.annotation,
                        class_validators=None,
                        model_config=CustomConfig,
                        default=None,
                        required=True,
                    )
                return cls(Required, checker=checker)
            elif param.annotation == param.empty and param.name == "bot":
                return cls(Required)

    async def _solve(self, bot: "Bot", **kwargs: Any) -> Any:
        return bot

    async def _check(self, bot: "Bot", **kwargs: Any) -> None:
        if checker := self.extra.get("checker"):
            check_field_type(checker, bot)


class EventParam(Param):
    """{ref}`nonebot.adapters.Event` 参数"""

    def __repr__(self) -> str:
        return (
            "EventParam("
            + (
                repr(cast(ModelField, checker).type_)
                if (checker := self.extra.get("checker"))
                else ""
            )
            + ")"
        )

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["EventParam"]:
        from nonebot.adapters import Event

        if param.default == param.empty:
            if generic_check_issubclass(param.annotation, Event):
                checker: Optional[ModelField] = None
                if param.annotation is not Event:
                    checker = ModelField(
                        name=param.name,
                        type_=param.annotation,
                        class_validators=None,
                        model_config=CustomConfig,
                        default=None,
                        required=True,
                    )
                return cls(Required, checker=checker)
            elif param.annotation == param.empty and param.name == "event":
                return cls(Required)

    async def _solve(self, event: "Event", **kwargs: Any) -> Any:
        return event

    async def _check(self, event: "Event", **kwargs: Any) -> Any:
        if checker := self.extra.get("checker", None):
            check_field_type(checker, event)


class StateParam(Param):
    """事件处理状态参数"""

    def __repr__(self) -> str:
        return "StateParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["StateParam"]:
        if param.default == param.empty:
            if param.annotation is T_State:
                return cls(Required)
            elif param.annotation == param.empty and param.name == "state":
                return cls(Required)

    async def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class MatcherParam(Param):
    """事件响应器实例参数"""

    def __repr__(self) -> str:
        return "MatcherParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["MatcherParam"]:
        from nonebot.matcher import Matcher

        if generic_check_issubclass(param.annotation, Matcher) or (
            param.annotation == param.empty and param.name == "matcher"
        ):
            return cls(Required)

    async def _solve(self, matcher: "Matcher", **kwargs: Any) -> Any:
        return matcher


class ArgInner:
    def __init__(
        self, key: Optional[str], type: Literal["message", "str", "plaintext"]
    ) -> None:
        self.key = key
        self.type = type

    def __repr__(self) -> str:
        return f"ArgInner(key={self.key!r}, type={self.type!r})"


def Arg(key: Optional[str] = None) -> Any:
    """`got` 的 Arg 参数消息"""
    return ArgInner(key, "message")


def ArgStr(key: Optional[str] = None) -> str:
    """`got` 的 Arg 参数消息文本"""
    return ArgInner(key, "str")  # type: ignore


def ArgPlainText(key: Optional[str] = None) -> str:
    """`got` 的 Arg 参数消息纯文本"""
    return ArgInner(key, "plaintext")  # type: ignore


class ArgParam(Param):
    """`got` 的 Arg 参数"""

    def __repr__(self) -> str:
        return f"ArgParam(key={self.extra['key']!r}, type={self.extra['type']!r})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["ArgParam"]:
        if isinstance(param.default, ArgInner):
            return cls(
                Required, key=param.default.key or param.name, type=param.default.type
            )

    async def _solve(self, matcher: "Matcher", **kwargs: Any) -> Any:
        message = matcher.get_arg(self.extra["key"])
        if message is None:
            return message
        if self.extra["type"] == "message":
            return message
        elif self.extra["type"] == "str":
            return str(message)
        else:
            return message.extract_plain_text()


class ExceptionParam(Param):
    """`run_postprocessor` 的异常参数"""

    def __repr__(self) -> str:
        return "ExceptionParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["ExceptionParam"]:
        if generic_check_issubclass(param.annotation, Exception) or (
            param.annotation == param.empty and param.name == "exception"
        ):
            return cls(Required)

    async def _solve(self, exception: Optional[Exception] = None, **kwargs: Any) -> Any:
        return exception


class DefaultParam(Param):
    """默认值参数"""

    def __repr__(self) -> str:
        return f"DefaultParam(default={self.default!r})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["DefaultParam"]:
        if param.default != param.empty:
            return cls(param.default)

    async def _solve(self, **kwargs: Any) -> Any:
        return Undefined


__autodoc__ = {
    "DependsInner": False,
    "StateInner": False,
    "ArgInner": False,
}
