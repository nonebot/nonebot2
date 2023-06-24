import asyncio
import inspect
from typing_extensions import Annotated
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager
from typing import TYPE_CHECKING, Any, Type, Tuple, Literal, Callable, Optional, cast

from pydantic.typing import get_args, get_origin
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

        async def handler(
            param_name: Any = Depends(depend_func),
            gen: Any = Depends(depend_gen_func),
        ):
            ...
        ```
    """
    return DependsInner(dependency, use_cache=use_cache)


class DependParam(Param):
    """子依赖注入参数。

    本注入解析所有子依赖注入，然后将它们的返回值作为参数值传递给父依赖。

    本注入应该具有最高优先级，因此应该在其他参数之前检查。
    """

    def __repr__(self) -> str:
        return f"Depends({self.extra['dependent']})"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["DependParam"]:
        type_annotation, depends_inner = param.annotation, None
        if get_origin(param.annotation) is Annotated:
            type_annotation, *extra_args = get_args(param.annotation)
            depends_inner = next(
                (x for x in extra_args if isinstance(x, DependsInner)), None
            )

        depends_inner = (
            param.default if isinstance(param.default, DependsInner) else depends_inner
        )
        if depends_inner is None:
            return

        dependency: T_Handler
        if depends_inner.dependency is None:
            assert (
                type_annotation is not inspect.Signature.empty
            ), "Dependency cannot be empty"
            dependency = type_annotation
        else:
            dependency = depends_inner.dependency
        sub_dependent = Dependent[Any].parse(
            call=dependency,
            allow_types=allow_types,
        )
        return cls(Required, use_cache=depends_inner.use_cache, dependent=sub_dependent)

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
    """{ref}`nonebot.adapters.Bot` 注入参数。

    本注入解析所有类型为且仅为 {ref}`nonebot.adapters.Bot` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `bot` 且没有类型注解的参数。
    """

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

        # param type is Bot(s) or subclass(es) of Bot or None
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
        # legacy: param is named "bot" and has no type annotation
        elif param.annotation == param.empty and param.name == "bot":
            return cls(Required)

    async def _solve(self, bot: "Bot", **kwargs: Any) -> Any:
        return bot

    async def _check(self, bot: "Bot", **kwargs: Any) -> None:
        if checker := self.extra.get("checker"):
            check_field_type(checker, bot)


class EventParam(Param):
    """{ref}`nonebot.adapters.Event` 注入参数

    本注入解析所有类型为且仅为 {ref}`nonebot.adapters.Event` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `event` 且没有类型注解的参数。
    """

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

        # param type is Event(s) or subclass(es) of Event or None
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
        # legacy: param is named "event" and has no type annotation
        elif param.annotation == param.empty and param.name == "event":
            return cls(Required)

    async def _solve(self, event: "Event", **kwargs: Any) -> Any:
        return event

    async def _check(self, event: "Event", **kwargs: Any) -> Any:
        if checker := self.extra.get("checker", None):
            check_field_type(checker, event)


class StateParam(Param):
    """事件处理状态注入参数

    本注入解析所有类型为 `T_State` 的参数。

    为保证兼容性，本注入还会解析名为 `state` 且没有类型注解的参数。
    """

    def __repr__(self) -> str:
        return "StateParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["StateParam"]:
        # param type is T_State
        if param.annotation is T_State:
            return cls(Required)
        # legacy: param is named "state" and has no type annotation
        elif param.annotation == param.empty and param.name == "state":
            return cls(Required)

    async def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class MatcherParam(Param):
    """事件响应器实例注入参数

    本注入解析所有类型为且仅为 {ref}`nonebot.matcher.Matcher` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `matcher` 且没有类型注解的参数。
    """

    def __repr__(self) -> str:
        return "MatcherParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["MatcherParam"]:
        from nonebot.matcher import Matcher

        # param type is Matcher(s) or subclass(es) of Matcher or None
        if generic_check_issubclass(param.annotation, Matcher):
            checker: Optional[ModelField] = None
            if param.annotation is not Matcher:
                checker = ModelField(
                    name=param.name,
                    type_=param.annotation,
                    class_validators=None,
                    model_config=CustomConfig,
                    default=None,
                    required=True,
                )
            return cls(Required, checker=checker)
        # legacy: param is named "matcher" and has no type annotation
        elif param.annotation == param.empty and param.name == "matcher":
            return cls(Required)

    async def _solve(self, matcher: "Matcher", **kwargs: Any) -> Any:
        return matcher

    async def _check(self, matcher: "Matcher", **kwargs: Any) -> Any:
        if checker := self.extra.get("checker", None):
            check_field_type(checker, matcher)


class ArgInner:
    def __init__(
        self, key: Optional[str], type: Literal["message", "str", "plaintext"]
    ) -> None:
        self.key = key
        self.type = type

    def __repr__(self) -> str:
        return f"ArgInner(key={self.key!r}, type={self.type!r})"


def Arg(key: Optional[str] = None) -> Any:
    """Arg 参数消息"""
    return ArgInner(key, "message")


def ArgStr(key: Optional[str] = None) -> str:
    """Arg 参数消息文本"""
    return ArgInner(key, "str")  # type: ignore


def ArgPlainText(key: Optional[str] = None) -> str:
    """Arg 参数消息纯文本"""
    return ArgInner(key, "plaintext")  # type: ignore


class ArgParam(Param):
    """Arg 注入参数

    本注入解析事件响应器操作 `got` 所获取的参数。

    可以通过 `Arg`、`ArgStr`、`ArgPlainText` 等函数参数 `key` 指定获取的参数，
    留空则会根据参数名称获取。
    """

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
        elif get_origin(param.annotation) is Annotated:
            for arg in get_args(param.annotation):
                if isinstance(arg, ArgInner):
                    return cls(Required, key=arg.key or param.name, type=arg.type)

    async def _solve(self, matcher: "Matcher", **kwargs: Any) -> Any:
        key: str = self.extra["key"]
        message = matcher.get_arg(key)
        if message is None:
            return message
        if self.extra["type"] == "message":
            return message
        elif self.extra["type"] == "str":
            return str(message)
        else:
            return message.extract_plain_text()


class ExceptionParam(Param):
    """{ref}`nonebot.message.run_postprocessor` 的异常注入参数

    本注入解析所有类型为 `Exception` 或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `exception` 且没有类型注解的参数。
    """

    def __repr__(self) -> str:
        return "ExceptionParam()"

    @classmethod
    def _check_param(
        cls, param: inspect.Parameter, allow_types: Tuple[Type[Param], ...]
    ) -> Optional["ExceptionParam"]:
        # param type is Exception(s) or subclass(es) of Exception or None
        if generic_check_issubclass(param.annotation, Exception):
            return cls(Required)
        # legacy: param is named "exception" and has no type annotation
        elif param.annotation == param.empty and param.name == "exception":
            return cls(Required)

    async def _solve(self, exception: Optional[Exception] = None, **kwargs: Any) -> Any:
        return exception


class DefaultParam(Param):
    """默认值注入参数

    本注入解析所有剩余未能解析且具有默认值的参数。

    本注入参数应该具有最低优先级，因此应该在所有其他注入参数之后使用。
    """

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
