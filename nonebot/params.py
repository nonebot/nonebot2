import asyncio
import inspect
from typing_extensions import Literal
from typing import Any, Dict, List, Tuple, Callable, Optional, cast
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager

from pydantic.fields import Required, Undefined, ModelField

from nonebot.log import logger
from nonebot.exception import TypeMisMatch
from nonebot.adapters import Bot, Event, Message
from nonebot.dependencies import Param, Dependent, CustomConfig
from nonebot.typing import T_State, T_Handler, T_DependencyCache
from nonebot.consts import (
    CMD_KEY,
    PREFIX_KEY,
    REGEX_DICT,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    RAW_CMD_KEY,
    REGEX_GROUP,
    REGEX_MATCHED,
)
from nonebot.utils import (
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
            sub_dependent = Dependent[Any].parse(
                call=dependency,
                allow_types=dependent.allow_types,
            )
            dependent.pre_checkers.extend(sub_dependent.pre_checkers)
            sub_dependent.pre_checkers.clear()
            return cls(
                Required, use_cache=param.default.use_cache, dependent=sub_dependent
            )

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
        dependency_cache: Optional[T_DependencyCache] = None,
        **kwargs: Any,
    ) -> Any:
        use_cache: bool = self.extra["use_cache"]
        dependency_cache = {} if dependency_cache is None else dependency_cache

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
        task: asyncio.Task[Any]
        if use_cache and call in dependency_cache:
            solved = await dependency_cache[call]
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
            solved = await task
        elif is_coroutine_callable(call):
            task = asyncio.create_task(call(**sub_values))
            dependency_cache[call] = task
            solved = await task
        else:
            task = asyncio.create_task(run_sync(call)(**sub_values))
            dependency_cache[call] = task
            solved = await task

        return solved


class _BotChecker(Param):
    async def _solve(self, bot: Bot, **kwargs: Any) -> Any:
        field: ModelField = self.extra["field"]
        _, errs_ = field.validate(bot, {}, loc=("bot",))
        if errs_:
            logger.debug(
                f"Bot type {type(bot)} not match "
                f"annotation {field._type_display()}, ignored"
            )
            raise TypeMisMatch(field, bot)


class BotParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["BotParam"]:
        if param.default == param.empty:
            if generic_check_issubclass(param.annotation, Bot):
                if param.annotation is not Bot:
                    dependent.pre_checkers.append(
                        _BotChecker(
                            Required,
                            field=ModelField(
                                name=name,
                                type_=param.annotation,
                                class_validators=None,
                                model_config=CustomConfig,
                                default=None,
                                required=True,
                            ),
                        )
                    )
                return cls(Required)
            elif param.annotation == param.empty and name == "bot":
                return cls(Required)

    async def _solve(self, bot: Bot, **kwargs: Any) -> Any:
        return bot


class _EventChecker(Param):
    async def _solve(self, event: Event, **kwargs: Any) -> Any:
        field: ModelField = self.extra["field"]
        _, errs_ = field.validate(event, {}, loc=("event",))
        if errs_:
            logger.debug(
                f"Event type {type(event)} not match "
                f"annotation {field._type_display()}, ignored"
            )
            raise TypeMisMatch(field, event)


class EventParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["EventParam"]:
        if param.default == param.empty:
            if generic_check_issubclass(param.annotation, Event):
                if param.annotation is not Event:
                    dependent.pre_checkers.append(
                        _EventChecker(
                            Required,
                            field=ModelField(
                                name=name,
                                type_=param.annotation,
                                class_validators=None,
                                model_config=CustomConfig,
                                default=None,
                                required=True,
                            ),
                        )
                    )
                return cls(Required)
            elif param.annotation == param.empty and name == "event":
                return cls(Required)

    async def _solve(self, event: Event, **kwargs: Any) -> Any:
        return event


async def _event_type(event: Event) -> str:
    return event.get_type()


def EventType() -> str:
    return Depends(_event_type)


async def _event_message(event: Event) -> Message:
    return event.get_message()


def EventMessage() -> Any:
    return Depends(_event_message)


async def _event_plain_text(event: Event) -> str:
    return event.get_plaintext()


def EventPlainText() -> str:
    return Depends(_event_plain_text)


async def _event_to_me(event: Event) -> bool:
    return event.is_tome()


def EventToMe() -> bool:
    return Depends(_event_to_me)


class StateInner:
    ...


def State() -> T_State:
    return StateInner()  # type: ignore


class StateParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["StateParam"]:
        if isinstance(param.default, StateInner):
            return cls(Required)

    async def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state


def _command(state=State()) -> Message:
    return state[PREFIX_KEY][CMD_KEY]


def Command() -> Tuple[str, ...]:
    return Depends(_command, use_cache=False)


def _raw_command(state=State()) -> Message:
    return state[PREFIX_KEY][RAW_CMD_KEY]


def RawCommand() -> str:
    return Depends(_raw_command, use_cache=False)


def _command_arg(state=State()) -> Message:
    return state[PREFIX_KEY][CMD_ARG_KEY]


def CommandArg() -> Any:
    return Depends(_command_arg, use_cache=False)


def _shell_command_args(state=State()) -> Any:
    return state[SHELL_ARGS]


def ShellCommandArgs():
    return Depends(_shell_command_args, use_cache=False)


def _shell_command_argv(state=State()) -> List[str]:
    return state[SHELL_ARGV]


def ShellCommandArgv() -> Any:
    return Depends(_shell_command_argv, use_cache=False)


def _regex_matched(state=State()) -> str:
    return state[REGEX_MATCHED]


def RegexMatched() -> str:
    return Depends(_regex_matched, use_cache=False)


def _regex_group(state=State()):
    return state[REGEX_GROUP]


def RegexGroup() -> Tuple[Any, ...]:
    return Depends(_regex_group, use_cache=False)


def _regex_dict(state=State()):
    return state[REGEX_DICT]


def RegexDict() -> Dict[str, Any]:
    return Depends(_regex_dict, use_cache=False)


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


def Received(id: Optional[str] = None, default: Any = None) -> Any:
    def _received(matcher: "Matcher"):
        return matcher.get_receive(id or "", default)

    return Depends(_received, use_cache=False)


def LastReceived(default: Any = None) -> Any:
    def _last_received(matcher: "Matcher") -> Any:
        return matcher.get_last_receive(default)

    return Depends(_last_received, use_cache=False)


class ArgInner:
    def __init__(
        self, key: Optional[str], type: Literal["message", "str", "plaintext"]
    ) -> None:
        self.key = key
        self.type = type


def Arg(key: Optional[str] = None) -> Any:
    return ArgInner(key, "message")


def ArgStr(key: Optional[str] = None) -> str:
    return ArgInner(key, "str")  # type: ignore


def ArgPlainText(key: Optional[str] = None) -> str:
    return ArgInner(key, "plaintext")  # type: ignore


class ArgParam(Param):
    @classmethod
    def _check_param(
        cls, dependent: Dependent, name: str, param: inspect.Parameter
    ) -> Optional["ArgParam"]:
        if isinstance(param.default, ArgInner):
            return cls(Required, key=param.default.key or name, type=param.default.type)

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
