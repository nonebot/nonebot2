from collections.abc import Iterable
from contextlib import AsyncExitStack, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta
import inspect
from pathlib import Path
import sys
from types import ModuleType
from typing import (  # noqa: UP035
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Self
import warnings

from exceptiongroup import BaseExceptionGroup, catch

from nonebot.consts import (
    ARG_KEY,
    LAST_RECEIVE_KEY,
    PAUSE_PROMPT_RESULT_KEY,
    RECEIVE_KEY,
    REJECT_CACHE_TARGET,
    REJECT_PROMPT_RESULT_KEY,
    REJECT_TARGET,
)
from nonebot.dependencies import Dependent, Param
from nonebot.exception import (
    FinishedException,
    PausedException,
    RejectedException,
    SkippedException,
    StopPropagation,
)
from nonebot.internal.adapter import (
    Bot,
    Event,
    Message,
    MessageSegment,
    MessageTemplate,
)
from nonebot.internal.params import (
    ArgParam,
    BotParam,
    DefaultParam,
    DependParam,
    Depends,
    EventParam,
    MatcherParam,
    StateParam,
)
from nonebot.internal.permission import Permission, User
from nonebot.internal.rule import Rule
from nonebot.log import logger
from nonebot.typing import (
    T_DependencyCache,
    T_Handler,
    T_PermissionUpdater,
    T_State,
    T_TypeUpdater,
)
from nonebot.utils import classproperty, flatten_exception_group

from . import matchers

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

T = TypeVar("T")

current_bot: ContextVar[Bot] = ContextVar("current_bot")
current_event: ContextVar[Event] = ContextVar("current_event")
current_matcher: ContextVar["Matcher"] = ContextVar("current_matcher")
current_handler: ContextVar[Dependent[Any]] = ContextVar("current_handler")


@dataclass
class MatcherSource:
    """Matcher 源代码上下文信息"""

    plugin_id: Optional[str] = None
    """事件响应器所在插件标识符"""
    module_name: Optional[str] = None
    """事件响应器所在插件模块的路径名"""
    lineno: Optional[int] = None
    """事件响应器所在行号"""

    @property
    def plugin(self) -> Optional["Plugin"]:
        """事件响应器所在插件"""
        from nonebot.plugin import get_plugin

        if self.plugin_id is not None:
            return get_plugin(self.plugin_id)

    @property
    def plugin_name(self) -> Optional[str]:
        """事件响应器所在插件名"""
        return self.plugin and self.plugin.name

    @property
    def module(self) -> Optional[ModuleType]:
        if self.module_name is not None:
            return sys.modules.get(self.module_name)

    @property
    def file(self) -> Optional[Path]:
        if self.module is not None and (file := inspect.getsourcefile(self.module)):
            return Path(file).absolute()


class MatcherMeta(type):
    if TYPE_CHECKING:
        type: str
        _source: Optional[MatcherSource]
        module_name: Optional[str]

    def __repr__(self) -> str:
        return (
            f"{self.__name__}(type={self.type!r}"
            + (f", module={self.module_name}" if self.module_name else "")
            + (
                f", lineno={self._source.lineno}"
                if self._source and self._source.lineno is not None
                else ""
            )
            + ")"
        )


class Matcher(metaclass=MatcherMeta):
    """事件响应器类"""

    _source: ClassVar[Optional[MatcherSource]] = None

    type: ClassVar[str] = ""
    """事件响应器类型"""
    rule: ClassVar[Rule] = Rule()
    """事件响应器匹配规则"""
    permission: ClassVar[Permission] = Permission()
    """事件响应器触发权限"""
    handlers: ClassVar[list[Dependent[Any]]] = []
    """事件响应器拥有的事件处理函数列表"""
    priority: ClassVar[int] = 1
    """事件响应器优先级"""
    block: bool = False
    """事件响应器是否阻止事件传播"""
    temp: ClassVar[bool] = False
    """事件响应器是否为临时"""
    expire_time: ClassVar[Optional[datetime]] = None
    """事件响应器过期时间点"""

    _default_state: ClassVar[T_State] = {}
    """事件响应器默认状态"""

    _default_type_updater: ClassVar[Optional[Dependent[str]]] = None
    """事件响应器类型更新函数"""
    _default_permission_updater: ClassVar[Optional[Dependent[Permission]]] = None
    """事件响应器权限更新函数"""

    HANDLER_PARAM_TYPES: ClassVar[tuple[Type[Param], ...]] = (  # noqa: UP006
        DependParam,
        BotParam,
        EventParam,
        StateParam,
        ArgParam,
        MatcherParam,
        DefaultParam,
    )

    def __init__(self):
        self.remain_handlers: list[Dependent[Any]] = self.handlers.copy()
        self.state = self._default_state.copy()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(type={self.type!r}"
            + (f", module={self.module_name}" if self.module_name else "")
            + (
                f", lineno={self._source.lineno}"
                if self._source and self._source.lineno is not None
                else ""
            )
            + ")"
        )

    @classmethod
    def new(
        cls,
        type_: str = "",
        rule: Optional[Rule] = None,
        permission: Optional[Permission] = None,
        handlers: Optional[list[Union[T_Handler, Dependent[Any]]]] = None,
        temp: bool = False,
        priority: int = 1,
        block: bool = False,
        *,
        plugin: Optional["Plugin"] = None,
        module: Optional[ModuleType] = None,
        source: Optional[MatcherSource] = None,
        expire_time: Optional[Union[datetime, timedelta]] = None,
        default_state: Optional[T_State] = None,
        default_type_updater: Optional[Union[T_TypeUpdater, Dependent[str]]] = None,
        default_permission_updater: Optional[
            Union[T_PermissionUpdater, Dependent[Permission]]
        ] = None,
    ) -> Type[Self]:  # noqa: UP006
        """
        创建一个新的事件响应器，并存储至 `matchers <#matchers>`_

        参数:
            type_: 事件响应器类型，与 `event.get_type()` 一致时触发，空字符串表示任意
            rule: 匹配规则
            permission: 权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器，即触发一次后删除
            priority: 响应优先级
            block: 是否阻止事件向更低优先级的响应器传播
            plugin: **Deprecated.** 事件响应器所在插件
            module: **Deprecated.** 事件响应器所在模块
            source: 事件响应器源代码上下文信息
            expire_time: 事件响应器最终有效时间点，过时即被删除
            default_state: 默认状态 `state`
            default_type_updater: 默认事件类型更新函数
            default_permission_updater: 默认会话权限更新函数

        返回:
            Type[Matcher]: 新的事件响应器类
        """
        if plugin is not None:
            warnings.warn(
                (
                    "Pass `plugin` context info to create Matcher is deprecated. "
                    "Use `source` instead."
                ),
                DeprecationWarning,
            )
        if module is not None:
            warnings.warn(
                (
                    "Pass `module` context info to create Matcher is deprecated. "
                    "Use `source` instead."
                ),
                DeprecationWarning,
            )
        source = source or (
            MatcherSource(
                plugin_id=plugin and plugin.id_,
                module_name=module and module.__name__,
            )
            if plugin is not None or module is not None
            else None
        )

        NewMatcher = type(
            cls.__name__,
            (cls,),
            {
                "_source": source,
                "type": type_,
                "rule": rule or Rule(),
                "permission": permission or Permission(),
                "handlers": (
                    [
                        (
                            handler
                            if isinstance(handler, Dependent)
                            else Dependent[Any].parse(
                                call=handler, allow_types=cls.HANDLER_PARAM_TYPES
                            )
                        )
                        for handler in handlers
                    ]
                    if handlers
                    else []
                ),
                "temp": temp,
                "expire_time": (
                    expire_time
                    and (
                        expire_time
                        if isinstance(expire_time, datetime)
                        else datetime.now() + expire_time
                    )
                ),
                "priority": priority,
                "block": block,
                "_default_state": default_state or {},
                "_default_type_updater": (
                    default_type_updater
                    and (
                        default_type_updater
                        if isinstance(default_type_updater, Dependent)
                        else Dependent[str].parse(
                            call=default_type_updater,
                            allow_types=cls.HANDLER_PARAM_TYPES,
                        )
                    )
                ),
                "_default_permission_updater": (
                    default_permission_updater
                    and (
                        default_permission_updater
                        if isinstance(default_permission_updater, Dependent)
                        else Dependent[Permission].parse(
                            call=default_permission_updater,
                            allow_types=cls.HANDLER_PARAM_TYPES,
                        )
                    )
                ),
            },
        )

        logger.trace(f"Define new matcher {NewMatcher}")

        matchers[priority].append(NewMatcher)

        return NewMatcher  # type: ignore

    @classmethod
    def destroy(cls) -> None:
        """销毁当前的事件响应器"""
        matchers[cls.priority].remove(cls)

    @classproperty
    def plugin(cls) -> Optional["Plugin"]:
        """事件响应器所在插件"""
        return cls._source and cls._source.plugin

    @classproperty
    def plugin_id(cls) -> Optional[str]:
        """事件响应器所在插件标识符"""
        return cls._source and cls._source.plugin_id

    @classproperty
    def plugin_name(cls) -> Optional[str]:
        """事件响应器所在插件名"""
        return cls._source and cls._source.plugin_name

    @classproperty
    def module(cls) -> Optional[ModuleType]:
        """事件响应器所在插件模块"""
        return cls._source and cls._source.module

    @classproperty
    def module_name(cls) -> Optional[str]:
        """事件响应器所在插件模块路径"""
        return cls._source and cls._source.module_name

    @classmethod
    async def check_perm(
        cls,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """检查是否满足触发权限

        参数:
            bot: Bot 对象
            event: 上报事件
            stack: 异步上下文栈
            dependency_cache: 依赖缓存

        返回:
            是否满足权限
        """
        event_type = event.get_type()
        return event_type == (cls.type or event_type) and await cls.permission(
            bot, event, stack, dependency_cache
        )

    @classmethod
    async def check_rule(
        cls,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """检查是否满足匹配规则

        参数:
            bot: Bot 对象
            event: 上报事件
            state: 当前状态
            stack: 异步上下文栈
            dependency_cache: 依赖缓存

        返回:
            是否满足匹配规则
        """
        event_type = event.get_type()
        return event_type == (cls.type or event_type) and await cls.rule(
            bot, event, state, stack, dependency_cache
        )

    @classmethod
    def type_updater(cls, func: T_TypeUpdater) -> T_TypeUpdater:
        """装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数

        参数:
            func: 响应事件类型更新函数
        """
        cls._default_type_updater = Dependent[str].parse(
            call=func, allow_types=cls.HANDLER_PARAM_TYPES
        )
        return func

    @classmethod
    def permission_updater(cls, func: T_PermissionUpdater) -> T_PermissionUpdater:
        """装饰一个函数来更改当前事件响应器的默认会话权限更新函数

        参数:
            func: 会话权限更新函数
        """
        cls._default_permission_updater = Dependent[Permission].parse(
            call=func, allow_types=cls.HANDLER_PARAM_TYPES
        )
        return func

    @classmethod
    def append_handler(
        cls, handler: T_Handler, parameterless: Optional[Iterable[Any]] = None
    ) -> Dependent[Any]:
        handler_ = Dependent[Any].parse(
            call=handler,
            parameterless=parameterless,
            allow_types=cls.HANDLER_PARAM_TYPES,
        )
        cls.handlers.append(handler_)
        return handler_

    @classmethod
    def handle(
        cls, parameterless: Optional[Iterable[Any]] = None
    ) -> Callable[[T_Handler], T_Handler]:
        """装饰一个函数来向事件响应器直接添加一个处理函数

        参数:
            parameterless: 非参数类型依赖列表
        """

        def _decorator(func: T_Handler) -> T_Handler:
            cls.append_handler(func, parameterless=parameterless)
            return func

        return _decorator

    @classmethod
    def receive(
        cls, id: str = "", parameterless: Optional[Iterable[Any]] = None
    ) -> Callable[[T_Handler], T_Handler]:
        """装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数

        参数:
            id: 消息 ID
            parameterless: 非参数类型依赖列表
        """

        async def _receive(event: Event, matcher: "Matcher") -> None:
            matcher.set_target(RECEIVE_KEY.format(id=id))
            if matcher.get_target() == RECEIVE_KEY.format(id=id):
                matcher.set_receive(id, event)
                return
            if matcher.get_receive(id, ...) is not ...:
                return
            await matcher.reject()

        _parameterless = (Depends(_receive), *(parameterless or ()))

        def _decorator(func: T_Handler) -> T_Handler:
            if cls.handlers and cls.handlers[-1].call is func:
                func_handler = cls.handlers[-1]
                new_handler = Dependent(
                    call=func_handler.call,
                    params=func_handler.params,
                    parameterless=Dependent.parse_parameterless(
                        tuple(_parameterless), cls.HANDLER_PARAM_TYPES
                    )
                    + func_handler.parameterless,
                )
                cls.handlers[-1] = new_handler
            else:
                cls.append_handler(func, parameterless=_parameterless)

            return func

        return _decorator

    @classmethod
    def got(
        cls,
        key: str,
        prompt: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        parameterless: Optional[Iterable[Any]] = None,
    ) -> Callable[[T_Handler], T_Handler]:
        """装饰一个函数来指示 NoneBot 获取一个参数 `key`

        当要获取的 `key` 不存在时接收用户新的一条消息再运行该函数，
        如果 `key` 已存在则直接继续运行

        参数:
            key: 参数名
            prompt: 在参数不存在时向用户发送的消息
            parameterless: 非参数类型依赖列表
        """

        async def _key_getter(event: Event, matcher: "Matcher"):
            matcher.set_target(ARG_KEY.format(key=key))
            if matcher.get_target() == ARG_KEY.format(key=key):
                matcher.set_arg(key, event.get_message())
                return
            if matcher.get_arg(key, ...) is not ...:
                return
            await matcher.reject(prompt)

        _parameterless = (Depends(_key_getter), *(parameterless or ()))

        def _decorator(func: T_Handler) -> T_Handler:
            if cls.handlers and cls.handlers[-1].call is func:
                func_handler = cls.handlers[-1]
                new_handler = Dependent(
                    call=func_handler.call,
                    params=func_handler.params,
                    parameterless=Dependent.parse_parameterless(
                        tuple(_parameterless), cls.HANDLER_PARAM_TYPES
                    )
                    + func_handler.parameterless,
                )
                cls.handlers[-1] = new_handler
            else:
                cls.append_handler(func, parameterless=_parameterless)

            return func

        return _decorator

    @classmethod
    async def send(
        cls,
        message: Union[str, Message, MessageSegment, MessageTemplate],
        **kwargs: Any,
    ) -> Any:
        """发送一条消息给当前交互用户

        参数:
            message: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        bot = current_bot.get()
        event = current_event.get()
        if isinstance(message, MessageTemplate):
            state = current_matcher.get().state
            _message = message.format(**state)
        else:
            _message = message
        return await bot.send(event=event, message=_message, **kwargs)

    @classmethod
    async def finish(
        cls,
        message: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        **kwargs,
    ) -> NoReturn:
        """发送一条消息给当前交互用户并结束当前事件响应器

        参数:
            message: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        if message is not None:
            await cls.send(message, **kwargs)
        raise FinishedException

    @classmethod
    async def pause(
        cls,
        prompt: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        **kwargs,
    ) -> NoReturn:
        """发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数

        参数:
            prompt: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        try:
            matcher = current_matcher.get()
        except Exception:
            matcher = None

        if prompt is not None:
            result = await cls.send(prompt, **kwargs)
            if matcher is not None:
                matcher.state[PAUSE_PROMPT_RESULT_KEY] = result
        raise PausedException

    @classmethod
    async def reject(
        cls,
        prompt: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        **kwargs,
    ) -> NoReturn:
        """最近使用 `got` / `receive` 接收的消息不符合预期，
        发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

        参数:
            prompt: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        try:
            matcher = current_matcher.get()
            key = matcher.get_target()
        except Exception:
            matcher = None
            key = None

        key = REJECT_PROMPT_RESULT_KEY.format(key=key) if key is not None else None

        if prompt is not None:
            result = await cls.send(prompt, **kwargs)
            if key is not None and matcher:
                matcher.state[key] = result
        raise RejectedException

    @classmethod
    async def reject_arg(
        cls,
        key: str,
        prompt: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        **kwargs,
    ) -> NoReturn:
        """最近使用 `got` 接收的消息不符合预期，
        发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一条消息后从头开始执行当前处理函数

        参数:
            key: 参数名
            prompt: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        matcher = current_matcher.get()
        arg_key = ARG_KEY.format(key=key)
        matcher.set_target(arg_key)

        if prompt is not None:
            result = await cls.send(prompt, **kwargs)
            matcher.state[REJECT_PROMPT_RESULT_KEY.format(key=arg_key)] = result
        raise RejectedException

    @classmethod
    async def reject_receive(
        cls,
        id: str = "",
        prompt: Optional[Union[str, Message, MessageSegment, MessageTemplate]] = None,
        **kwargs,
    ) -> NoReturn:
        """最近使用 `receive` 接收的消息不符合预期，
        发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

        参数:
            id: 消息 id
            prompt: 消息内容
            kwargs: {ref}`nonebot.adapters.Bot.send` 的参数，
                请参考对应 adapter 的 bot 对象 api
        """
        matcher = current_matcher.get()
        receive_key = RECEIVE_KEY.format(id=id)
        matcher.set_target(receive_key)

        if prompt is not None:
            result = await cls.send(prompt, **kwargs)
            matcher.state[REJECT_PROMPT_RESULT_KEY.format(key=receive_key)] = result
        raise RejectedException

    @classmethod
    def skip(cls) -> NoReturn:
        """跳过当前事件处理函数，继续下一个处理函数

        通常在事件处理函数的依赖中使用。
        """
        raise SkippedException

    @overload
    def get_receive(self, id: str) -> Union[Event, None]: ...

    @overload
    def get_receive(self, id: str, default: T) -> Union[Event, T]: ...

    def get_receive(
        self, id: str, default: Optional[T] = None
    ) -> Optional[Union[Event, T]]:
        """获取一个 `receive` 事件

        如果没有找到对应的事件，返回 `default` 值
        """
        return self.state.get(RECEIVE_KEY.format(id=id), default)

    def set_receive(self, id: str, event: Event) -> None:
        """设置一个 `receive` 事件"""
        self.state[RECEIVE_KEY.format(id=id)] = event
        self.state[LAST_RECEIVE_KEY] = event

    @overload
    def get_last_receive(self) -> Union[Event, None]: ...

    @overload
    def get_last_receive(self, default: T) -> Union[Event, T]: ...

    def get_last_receive(
        self, default: Optional[T] = None
    ) -> Optional[Union[Event, T]]:
        """获取最近一次 `receive` 事件

        如果没有事件，返回 `default` 值
        """
        return self.state.get(LAST_RECEIVE_KEY, default)

    @overload
    def get_arg(self, key: str) -> Union[Message, None]: ...

    @overload
    def get_arg(self, key: str, default: T) -> Union[Message, T]: ...

    def get_arg(
        self, key: str, default: Optional[T] = None
    ) -> Optional[Union[Message, T]]:
        """获取一个 `got` 消息

        如果没有找到对应的消息，返回 `default` 值
        """
        return self.state.get(ARG_KEY.format(key=key), default)

    def set_arg(self, key: str, message: Message) -> None:
        """设置一个 `got` 消息"""
        self.state[ARG_KEY.format(key=key)] = message

    def set_target(self, target: str, cache: bool = True) -> None:
        if cache:
            self.state[REJECT_CACHE_TARGET] = target
        else:
            self.state[REJECT_TARGET] = target

    @overload
    def get_target(self) -> Union[str, None]: ...

    @overload
    def get_target(self, default: T) -> Union[str, T]: ...

    def get_target(self, default: Optional[T] = None) -> Optional[Union[str, T]]:
        return self.state.get(REJECT_TARGET, default)

    def stop_propagation(self):
        """阻止事件传播"""
        self.block = True

    async def update_type(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> str:
        updater = self.__class__._default_type_updater
        return (
            await updater(
                bot=bot,
                event=event,
                state=self.state,
                matcher=self,
                stack=stack,
                dependency_cache=dependency_cache,
            )
            if updater
            else "message"
        )

    async def update_permission(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> Permission:
        if updater := self.__class__._default_permission_updater:
            return await updater(
                bot=bot,
                event=event,
                state=self.state,
                matcher=self,
                stack=stack,
                dependency_cache=dependency_cache,
            )
        return Permission(User.from_event(event, perm=self.permission))

    async def resolve_reject(self):
        handler = current_handler.get()
        self.remain_handlers.insert(0, handler)
        if REJECT_CACHE_TARGET in self.state:
            self.state[REJECT_TARGET] = self.state[REJECT_CACHE_TARGET]

    @contextmanager
    def ensure_context(self, bot: Bot, event: Event):
        b_t = current_bot.set(bot)
        e_t = current_event.set(event)
        m_t = current_matcher.set(self)
        try:
            yield
        finally:
            current_bot.reset(b_t)
            current_event.reset(e_t)
            current_matcher.reset(m_t)

    async def simple_run(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ):
        logger.trace(
            f"{self} run with incoming args: "
            f"bot={bot}, event={event!r}, state={state!r}"
        )

        def _handle_stop_propagation(exc_group: BaseExceptionGroup[StopPropagation]):
            self.block = True

        with self.ensure_context(bot, event):
            try:
                with catch({StopPropagation: _handle_stop_propagation}):
                    # Refresh preprocess state
                    self.state.update(state)

                    while self.remain_handlers:
                        handler = self.remain_handlers.pop(0)
                        current_handler.set(handler)
                        logger.debug(f"Running handler {handler}")

                        def _handle_skipped(
                            exc_group: BaseExceptionGroup[SkippedException],
                        ):
                            logger.debug(f"Handler {handler} skipped")

                        with catch({SkippedException: _handle_skipped}):
                            await handler(
                                matcher=self,
                                bot=bot,
                                event=event,
                                state=self.state,
                                stack=stack,
                                dependency_cache=dependency_cache,
                            )
            finally:
                logger.info(f"{self} running complete")

    # 运行handlers
    async def run(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ):
        exc: Optional[Union[FinishedException, RejectedException, PausedException]] = (
            None
        )

        def _handle_special_exception(
            exc_group: BaseExceptionGroup[
                Union[FinishedException, RejectedException, PausedException]
            ],
        ):
            nonlocal exc
            excs = list(flatten_exception_group(exc_group))
            if len(excs) > 1:
                logger.warning(
                    "Multiple session control exceptions occurred. "
                    "NoneBot will choose the proper one."
                )
                finished_exc = next(
                    (e for e in excs if isinstance(e, FinishedException)),
                    None,
                )
                rejected_exc = next(
                    (e for e in excs if isinstance(e, RejectedException)),
                    None,
                )
                paused_exc = next(
                    (e for e in excs if isinstance(e, PausedException)),
                    None,
                )
                exc = finished_exc or rejected_exc or paused_exc
            elif isinstance(
                excs[0], (FinishedException, RejectedException, PausedException)
            ):
                exc = excs[0]

        with catch(
            {
                (
                    FinishedException,
                    RejectedException,
                    PausedException,
                ): _handle_special_exception
            }
        ):
            await self.simple_run(bot, event, state, stack, dependency_cache)

        if isinstance(exc, FinishedException):
            pass
        elif isinstance(exc, RejectedException):
            await self.resolve_reject()
            type_ = await self.update_type(bot, event, stack, dependency_cache)
            permission = await self.update_permission(
                bot, event, stack, dependency_cache
            )

            self.new(
                type_,
                Rule(),
                permission,
                self.remain_handlers,
                temp=True,
                priority=0,
                block=True,
                source=self.__class__._source,
                expire_time=bot.config.session_expire_timeout,
                default_state=self.state,
                default_type_updater=self.__class__._default_type_updater,
                default_permission_updater=self.__class__._default_permission_updater,
            )
        elif isinstance(exc, PausedException):
            type_ = await self.update_type(bot, event, stack, dependency_cache)
            permission = await self.update_permission(
                bot, event, stack, dependency_cache
            )

            self.new(
                type_,
                Rule(),
                permission,
                self.remain_handlers,
                temp=True,
                priority=0,
                block=True,
                source=self.__class__._source,
                expire_time=bot.config.session_expire_timeout,
                default_state=self.state,
                default_type_updater=self.__class__._default_type_updater,
                default_permission_updater=self.__class__._default_permission_updater,
            )
