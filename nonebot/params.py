import inspect
from typing import Any, List, Type, Callable, Optional, cast
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager

from pydantic.fields import Required, Undefined

from nonebot.adapters import Bot, Event
from nonebot.typing import T_State, T_Handler
from nonebot.dependencies import Param, Dependent
from nonebot.utils import (
    CacheDict,
    get_name,
    run_sync,
    is_gen_callable,
    run_sync_ctx_manager,
    is_async_gen_callable,
    is_coroutine_callable,
    generic_check_issubclass,
)


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
        return f"{self.__class__.__name__}({dep}{cache})"


def Depends(
    dependency: Optional[T_Handler] = None,
    *,
    use_cache: bool = True,
) -> Any:
    """
    :说明:

      参数依赖注入装饰器

    :参数:

      * ``dependency: Optional[Callable[..., Any]] = None``: 依赖函数。默认为参数的类型注释。
      * ``use_cache: bool = True``: 是否使用缓存。默认为 ``True``。
      * ``allow_types: Optional[List[Type[Param]]] = None``: 允许的参数类型。默认为 ``None``。

    .. code-block:: python

        def depend_func() -> Any:
            return ...

        def depend_gen_func():
            try:
                yield ...
            finally:
                ...

        async def handler(param_name: Any = Depends(depend_func), gen: Any = Depends(depend_gen_func)):
            ...
    """
    return DependsInner(dependency, use_cache=use_cache)


class DependParam(Param):
    @classmethod
    def _check_param(
        cls,
        dependent: Dependent,
        name: str,
        param: inspect.Parameter,
    ) -> Optional["DependParam"]:
        if isinstance(param.default, DependsInner):
            dependency: T_Handler
            if param.default.dependency is None:
                assert param.annotation is not param.empty, "Dependency cannot be empty"
                dependency = param.annotation
            else:
                dependency = param.default.dependency
            dependent = Dependent[Any].parse(
                call=dependency,
                allow_types=dependent.allow_types,
            )
            return cls(Required, use_cache=param.default.use_cache, dependent=dependent)

    @classmethod
    def _check_parameterless(
        cls, dependent: "Dependent", value: Any
    ) -> Optional["Param"]:
        if isinstance(value, DependsInner):
            assert value.dependency, "Dependency cannot be empty"
            dependent = Dependent[Any].parse(
                call=value.dependency, allow_types=dependent.allow_types
            )
            return cls(Required, use_cache=value.use_cache, dependent=dependent)

    async def _solve(
        self,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[CacheDict[T_Handler, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        use_cache: bool = self.extra["use_cache"]
        dependency_cache = CacheDict() if dependency_cache is None else dependency_cache

        sub_dependent: Dependent = self.extra["dependent"]
        sub_dependent.call = cast(Callable[..., Any], sub_dependent.call)
        call = sub_dependent.call

        # solve sub dependency with current cache
        sub_values = await sub_dependent.solve(
            stack=stack,
            dependency_cache=dependency_cache,
            **kwargs,
        )

        # run dependency function
        async with dependency_cache:
            if use_cache and call in dependency_cache:
                solved = dependency_cache[call]
            elif is_gen_callable(call) or is_async_gen_callable(call):
                assert isinstance(
                    stack, AsyncExitStack
                ), "Generator dependency should be called in context"
                if is_gen_callable(call):
                    cm = run_sync_ctx_manager(contextmanager(call)(**sub_values))
                else:
                    cm = asynccontextmanager(call)(**sub_values)
                solved = await stack.enter_async_context(cm)
            elif is_coroutine_callable(call):
                return await call(**sub_values)
            else:
                return await run_sync(call)(**sub_values)

            # save current dependency to cache
            if call not in dependency_cache:
                dependency_cache[call] = solved

        return solved


class BotParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["BotParam"]:
        if param.default == param.empty and (
            generic_check_issubclass(param.annotation, Bot)
            or (param.annotation == param.empty and name == "bot")
        ):
            return cls(Required)

    async def _solve(self, bot: Bot, **kwargs: Any) -> Any:
        return bot


class EventParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["EventParam"]:
        if param.default == param.empty and (
            generic_check_issubclass(param.annotation, Event)
            or (param.annotation == param.empty and name == "event")
        ):
            return cls(Required)

    async def _solve(self, event: Event, **kwargs: Any) -> Any:
        return event


class StateInner:
    ...


def State() -> Any:
    return StateInner()


class StateParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["StateParam"]:
        if isinstance(param.default, StateInner):
            return cls(Required)

    async def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


class MatcherParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["MatcherParam"]:
        if generic_check_issubclass(param.annotation, Matcher) or (
            param.annotation == param.empty and name == "matcher"
        ):
            return cls(Required)

    async def _solve(self, matcher: "Matcher", **kwargs: Any) -> Any:
        return matcher


class ExceptionParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["ExceptionParam"]:
        if generic_check_issubclass(param.annotation, Exception) or (
            param.annotation == param.empty and name == "exception"
        ):
            return cls(Required)

    async def _solve(self, exception: Optional[Exception] = None, **kwargs: Any) -> Any:
        return exception


class DefaultParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["DefaultParam"]:
        if param.default != param.empty:
            return cls(param.default)

    async def _solve(self, **kwargs: Any) -> Any:
        return Undefined


from nonebot.matcher import Matcher
