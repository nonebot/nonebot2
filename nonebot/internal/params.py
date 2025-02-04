from contextlib import AsyncExitStack, asynccontextmanager, contextmanager
from enum import Enum
import inspect
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    Literal,
    Optional,
    Union,
    cast,
)
from typing_extensions import Self, get_args, get_origin, override

import anyio
from exceptiongroup import BaseExceptionGroup, catch
from pydantic.fields import FieldInfo as PydanticFieldInfo

from nonebot.compat import FieldInfo, ModelField, PydanticUndefined, extract_field_info
from nonebot.consts import ARG_KEY, REJECT_PROMPT_RESULT_KEY
from nonebot.dependencies import Dependent, Param
from nonebot.dependencies.utils import check_field_type
from nonebot.exception import SkippedException
from nonebot.typing import (
    _STATE_FLAG,
    T_DependencyCache,
    T_Handler,
    T_State,
    origin_is_annotated,
)
from nonebot.utils import (
    generic_check_issubclass,
    get_name,
    is_async_gen_callable,
    is_coroutine_callable,
    is_gen_callable,
    run_sync,
    run_sync_ctx_manager,
)

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event, Message
    from nonebot.matcher import Matcher


class DependsInner:
    def __init__(
        self,
        dependency: Optional[T_Handler] = None,
        *,
        use_cache: bool = True,
        validate: Union[bool, PydanticFieldInfo] = False,
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache
        self.validate = validate

    def __repr__(self) -> str:
        dep = get_name(self.dependency)
        cache = "" if self.use_cache else ", use_cache=False"
        validate = f", validate={self.validate}" if self.validate else ""
        return f"DependsInner({dep}{cache}{validate})"


def Depends(
    dependency: Optional[T_Handler] = None,
    *,
    use_cache: bool = True,
    validate: Union[bool, PydanticFieldInfo] = False,
) -> Any:
    """子依赖装饰器

    参数:
        dependency: 依赖函数。默认为参数的类型注释。
        use_cache: 是否使用缓存。默认为 `True`。
        validate: 是否使用 Pydantic 类型校验。默认为 `False`。

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
    return DependsInner(dependency, use_cache=use_cache, validate=validate)


class CacheState(str, Enum):
    """子依赖缓存状态"""

    PENDING = "PENDING"
    FINISHED = "FINISHED"


class DependencyCache:
    """子依赖结果缓存。

    用于缓存子依赖的结果，以避免重复计算。
    """

    def __init__(self):
        self._state = CacheState.PENDING
        self._result: Any = None
        self._exception: Optional[BaseException] = None
        self._waiter = anyio.Event()

    def done(self) -> bool:
        return self._state == CacheState.FINISHED

    def result(self) -> Any:
        """获取子依赖结果"""

        if self._state != CacheState.FINISHED:
            raise RuntimeError("Result is not ready")

        if self._exception is not None:
            raise self._exception
        return self._result

    def exception(self) -> Optional[BaseException]:
        """获取子依赖异常"""

        if self._state != CacheState.FINISHED:
            raise RuntimeError("Result is not ready")

        return self._exception

    def set_result(self, result: Any) -> None:
        """设置子依赖结果"""

        if self._state != CacheState.PENDING:
            raise RuntimeError(f"Cache state invalid: {self._state}")

        self._result = result
        self._state = CacheState.FINISHED
        self._waiter.set()

    def set_exception(self, exception: BaseException) -> None:
        """设置子依赖异常"""

        if self._state != CacheState.PENDING:
            raise RuntimeError(f"Cache state invalid: {self._state}")

        self._exception = exception
        self._state = CacheState.FINISHED
        self._waiter.set()

    async def wait(self):
        """等待子依赖结果"""
        await self._waiter.wait()
        if self._state != CacheState.FINISHED:
            raise RuntimeError("Invalid cache state")

        if self._exception is not None:
            raise self._exception

        return self._result


class DependParam(Param):
    """子依赖注入参数。

    本注入解析所有子依赖注入，然后将它们的返回值作为参数值传递给父依赖。

    本注入应该具有最高优先级，因此应该在其他参数之前检查。
    """

    def __init__(
        self, *args, dependent: Dependent[Any], use_cache: bool, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.dependent = dependent
        self.use_cache = use_cache

    def __repr__(self) -> str:
        return f"Depends({self.dependent}, use_cache={self.use_cache})"

    @classmethod
    def _from_field(
        cls,
        sub_dependent: Dependent[Any],
        use_cache: bool,
        validate: Union[bool, PydanticFieldInfo],
    ) -> Self:
        kwargs = {}
        if isinstance(validate, PydanticFieldInfo):
            kwargs.update(extract_field_info(validate))

        kwargs["validate"] = bool(validate)
        kwargs["dependent"] = sub_dependent
        kwargs["use_cache"] = use_cache

        return cls(**kwargs)

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        type_annotation, depends_inner = param.annotation, None
        # extract type annotation and dependency from Annotated
        if get_origin(param.annotation) is Annotated:
            type_annotation, *extra_args = get_args(param.annotation)
            depends_inner = next(
                (x for x in reversed(extra_args) if isinstance(x, DependsInner)), None
            )

        # param default value takes higher priority
        depends_inner = (
            param.default if isinstance(param.default, DependsInner) else depends_inner
        )
        # not a dependent
        if depends_inner is None:
            return

        dependency: T_Handler
        # sub dependency is not specified, use type annotation
        if depends_inner.dependency is None:
            assert type_annotation is not inspect.Signature.empty, (
                "Dependency cannot be empty"
            )
            dependency = type_annotation
        else:
            dependency = depends_inner.dependency
        # parse sub dependency
        sub_dependent = Dependent[Any].parse(
            call=dependency,
            allow_types=allow_types,
        )

        return cls._from_field(
            sub_dependent, depends_inner.use_cache, depends_inner.validate
        )

    @classmethod
    @override
    def _check_parameterless(
        cls, value: Any, allow_types: tuple[type[Param], ...]
    ) -> Optional["Param"]:
        if isinstance(value, DependsInner):
            assert value.dependency, "Dependency cannot be empty"
            dependent = Dependent[Any].parse(
                call=value.dependency, allow_types=allow_types
            )
            return cls._from_field(dependent, value.use_cache, value.validate)

    @override
    async def _solve(
        self,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
        **kwargs: Any,
    ) -> Any:
        use_cache: bool = self.use_cache
        dependency_cache = {} if dependency_cache is None else dependency_cache

        sub_dependent = self.dependent
        call = cast(Callable[..., Any], sub_dependent.call)

        # solve sub dependency with current cache
        exc: Optional[BaseExceptionGroup[SkippedException]] = None

        def _handle_skipped(exc_group: BaseExceptionGroup[SkippedException]):
            nonlocal exc
            exc = exc_group

        with catch({SkippedException: _handle_skipped}):
            sub_values = await sub_dependent.solve(
                stack=stack,
                dependency_cache=dependency_cache,
                **kwargs,
            )

        if exc is not None:
            raise exc

        # run dependency function
        if use_cache and call in dependency_cache:
            return await dependency_cache[call].wait()

        if is_gen_callable(call) or is_async_gen_callable(call):
            assert isinstance(stack, AsyncExitStack), (
                "Generator dependency should be called in context"
            )
            if is_gen_callable(call):
                cm = run_sync_ctx_manager(contextmanager(call)(**sub_values))
            else:
                cm = asynccontextmanager(call)(**sub_values)

            target = stack.enter_async_context(cm)
        elif is_coroutine_callable(call):
            target = call(**sub_values)
        else:
            target = run_sync(call)(**sub_values)

        dependency_cache[call] = cache = DependencyCache()
        try:
            result = await target
        except Exception as e:
            cache.set_exception(e)
            raise
        except BaseException as e:
            cache.set_exception(e)
            # remove cache when base exception occurs
            # e.g. CancelledError
            dependency_cache.pop(call, None)
            raise
        else:
            cache.set_result(result)
            return result

    @override
    async def _check(self, **kwargs: Any) -> None:
        # run sub dependent pre-checkers
        await self.dependent.check(**kwargs)


class BotParam(Param):
    """{ref}`nonebot.adapters.Bot` 注入参数。

    本注入解析所有类型为且仅为 {ref}`nonebot.adapters.Bot` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `bot` 且没有类型注解的参数。
    """

    def __init__(
        self, *args, checker: Optional[ModelField] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.checker = checker

    def __repr__(self) -> str:
        return (
            "BotParam("
            + (repr(self.checker.annotation) if self.checker is not None else "")
            + ")"
        )

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        from nonebot.adapters import Bot

        # param type is Bot(s) or subclass(es) of Bot or None
        if generic_check_issubclass(param.annotation, Bot):
            checker: Optional[ModelField] = None
            if param.annotation is not Bot:
                checker = ModelField.construct(
                    name=param.name, annotation=param.annotation, field_info=FieldInfo()
                )
            return cls(checker=checker)
        # legacy: param is named "bot" and has no type annotation
        elif param.annotation == param.empty and param.name == "bot":
            return cls()

    @override
    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, bot: "Bot", **kwargs: Any
    ) -> Any:
        return bot

    @override
    async def _check(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, bot: "Bot", **kwargs: Any
    ) -> None:
        if self.checker is not None:
            check_field_type(self.checker, bot)


class EventParam(Param):
    """{ref}`nonebot.adapters.Event` 注入参数

    本注入解析所有类型为且仅为 {ref}`nonebot.adapters.Event` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `event` 且没有类型注解的参数。
    """

    def __init__(
        self, *args, checker: Optional[ModelField] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.checker = checker

    def __repr__(self) -> str:
        return (
            "EventParam("
            + (repr(self.checker.annotation) if self.checker is not None else "")
            + ")"
        )

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        from nonebot.adapters import Event

        # param type is Event(s) or subclass(es) of Event or None
        if generic_check_issubclass(param.annotation, Event):
            checker: Optional[ModelField] = None
            if param.annotation is not Event:
                checker = ModelField.construct(
                    name=param.name, annotation=param.annotation, field_info=FieldInfo()
                )
            return cls(checker=checker)
        # legacy: param is named "event" and has no type annotation
        elif param.annotation == param.empty and param.name == "event":
            return cls()

    @override
    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, event: "Event", **kwargs: Any
    ) -> Any:
        return event

    @override
    async def _check(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, event: "Event", **kwargs: Any
    ) -> Any:
        if self.checker is not None:
            check_field_type(self.checker, event)


class StateParam(Param):
    """事件处理状态注入参数

    本注入解析所有类型为 `T_State` 的参数。

    为保证兼容性，本注入还会解析名为 `state` 且没有类型注解的参数。
    """

    def __repr__(self) -> str:
        return "StateParam()"

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        # param type is T_State
        if origin_is_annotated(
            get_origin(param.annotation)
        ) and _STATE_FLAG in get_args(param.annotation):
            return cls()
        # legacy: param is named "state" and has no type annotation
        elif param.annotation == param.empty and param.name == "state":
            return cls()

    @override
    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, state: T_State, **kwargs: Any
    ) -> Any:
        return state


class MatcherParam(Param):
    """事件响应器实例注入参数

    本注入解析所有类型为且仅为 {ref}`nonebot.matcher.Matcher` 及其子类或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `matcher` 且没有类型注解的参数。
    """

    def __init__(
        self, *args, checker: Optional[ModelField] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.checker = checker

    def __repr__(self) -> str:
        return (
            "MatcherParam("
            + (repr(self.checker.annotation) if self.checker is not None else "")
            + ")"
        )

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        from nonebot.matcher import Matcher

        # param type is Matcher(s) or subclass(es) of Matcher or None
        if generic_check_issubclass(param.annotation, Matcher):
            checker: Optional[ModelField] = None
            if param.annotation is not Matcher:
                checker = ModelField.construct(
                    name=param.name, annotation=param.annotation, field_info=FieldInfo()
                )
            return cls(checker=checker)
        # legacy: param is named "matcher" and has no type annotation
        elif param.annotation == param.empty and param.name == "matcher":
            return cls()

    @override
    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, matcher: "Matcher", **kwargs: Any
    ) -> Any:
        return matcher

    @override
    async def _check(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, matcher: "Matcher", **kwargs: Any
    ) -> Any:
        if self.checker is not None:
            check_field_type(self.checker, matcher)


class ArgInner:
    def __init__(
        self, key: Optional[str], type: Literal["message", "str", "plaintext", "prompt"]
    ) -> None:
        self.key: Optional[str] = key
        self.type: Literal["message", "str", "plaintext", "prompt"] = type

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


def ArgPromptResult(key: Optional[str] = None) -> Any:
    """`arg` prompt 发送结果"""
    return ArgInner(key, "prompt")


class ArgParam(Param):
    """Arg 注入参数

    本注入解析事件响应器操作 `got` 所获取的参数。

    可以通过 `Arg`、`ArgStr`、`ArgPlainText` 等函数参数 `key` 指定获取的参数，
    留空则会根据参数名称获取。
    """

    def __init__(
        self,
        *args,
        key: str,
        type: Literal["message", "str", "plaintext", "prompt"],
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.key = key
        self.type = type

    def __repr__(self) -> str:
        return f"ArgParam(key={self.key!r}, type={self.type!r})"

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        if isinstance(param.default, ArgInner):
            return cls(key=param.default.key or param.name, type=param.default.type)
        elif get_origin(param.annotation) is Annotated:
            for arg in get_args(param.annotation)[:0:-1]:
                if isinstance(arg, ArgInner):
                    return cls(key=arg.key or param.name, type=arg.type)

    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, matcher: "Matcher", **kwargs: Any
    ) -> Any:
        if self.type == "message":
            return self._solve_message(matcher)
        elif self.type == "str":
            return self._solve_str(matcher)
        elif self.type == "plaintext":
            return self._solve_plaintext(matcher)
        elif self.type == "prompt":
            return self._solve_prompt(matcher)
        else:
            raise ValueError(f"Unknown Arg type: {self.type}")

    def _solve_message(self, matcher: "Matcher") -> Optional["Message"]:
        return matcher.get_arg(self.key)

    def _solve_str(self, matcher: "Matcher") -> Optional[str]:
        message = matcher.get_arg(self.key)
        return str(message) if message is not None else None

    def _solve_plaintext(self, matcher: "Matcher") -> Optional[str]:
        message = matcher.get_arg(self.key)
        return message.extract_plain_text() if message is not None else None

    def _solve_prompt(self, matcher: "Matcher") -> Optional[Any]:
        return matcher.state.get(
            REJECT_PROMPT_RESULT_KEY.format(key=ARG_KEY.format(key=self.key))
        )


class ExceptionParam(Param):
    """{ref}`nonebot.message.run_postprocessor` 的异常注入参数

    本注入解析所有类型为 `Exception` 或 `None` 的参数。

    为保证兼容性，本注入还会解析名为 `exception` 且没有类型注解的参数。
    """

    def __repr__(self) -> str:
        return "ExceptionParam()"

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        # param type is Exception(s) or subclass(es) of Exception or None
        if generic_check_issubclass(param.annotation, Exception):
            return cls()
        # legacy: param is named "exception" and has no type annotation
        elif param.annotation == param.empty and param.name == "exception":
            return cls()

    @override
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
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        if param.default != param.empty:
            return cls(default=param.default)

    @override
    async def _solve(self, **kwargs: Any) -> Any:
        return PydanticUndefined


__autodoc__ = {
    "DependsInner": False,
    "StateInner": False,
    "ArgInner": False,
}
