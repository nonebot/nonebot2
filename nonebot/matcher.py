"""
事件响应器
==========

该模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行对话 。
"""

from functools import wraps
from types import ModuleType
from datetime import datetime
from contextvars import ContextVar
from collections import defaultdict
from typing import (Any, Type, List, Dict, Union, Mapping, Iterable, Callable,
                    Optional, NoReturn, TYPE_CHECKING)

from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.handler import Handler
from nonebot.permission import Permission, USER
from nonebot.typing import (T_State, T_StateFactory, T_Handler, T_ArgsParser,
                            T_TypeUpdater, T_PermissionUpdater)
from nonebot.exception import (PausedException, RejectedException,
                               FinishedException, StopPropagation)

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event, Message, MessageSegment

matchers: Dict[int, List[Type["Matcher"]]] = defaultdict(list)
"""
:类型: ``Dict[int, List[Type[Matcher]]]``
:说明: 用于存储当前所有的事件响应器
"""
current_bot: ContextVar = ContextVar("current_bot")
current_event: ContextVar = ContextVar("current_event")


class MatcherMeta(type):
    if TYPE_CHECKING:
        module: Optional[str]
        plugin_name: Optional[str]
        module_name: Optional[str]
        module_prefix: Optional[str]
        type: str
        rule: Rule
        permission: Permission
        handlers: List[T_Handler]
        priority: int
        block: bool
        temp: bool
        expire_time: Optional[datetime]

    def __repr__(self) -> str:
        return (f"<Matcher from {self.module_name or 'unknown'}, "
                f"type={self.type}, priority={self.priority}, "
                f"temp={self.temp}>")

    def __str__(self) -> str:
        return repr(self)


class Matcher(metaclass=MatcherMeta):
    """事件响应器类"""
    module: Optional[ModuleType] = None
    """
    :类型: ``Optional[ModuleType]``
    :说明: 事件响应器所在模块
    """
    plugin_name: Optional[str] = module and getattr(module, "__plugin_name__",
                                                    None)
    """
    :类型: ``Optional[str]``
    :说明: 事件响应器所在插件名
    """
    module_name: Optional[str] = module and getattr(module, "__module_name__",
                                                    None)
    """
    :类型: ``Optional[str]``
    :说明: 事件响应器所在模块名
    """
    module_prefix: Optional[str] = module and getattr(module,
                                                      "__module_prefix__", None)
    """
    :类型: ``Optional[str]``
    :说明: 事件响应器所在模块前缀
    """

    type: str = ""
    """
    :类型: ``str``
    :说明: 事件响应器类型
    """
    rule: Rule = Rule()
    """
    :类型: ``Rule``
    :说明: 事件响应器匹配规则
    """
    permission: Permission = Permission()
    """
    :类型: ``Permission``
    :说明: 事件响应器触发权限
    """
    handlers: List[Handler] = []
    """
    :类型: ``List[Handler]``
    :说明: 事件响应器拥有的事件处理函数列表
    """
    priority: int = 1
    """
    :类型: ``int``
    :说明: 事件响应器优先级
    """
    block: bool = False
    """
    :类型: ``bool``
    :说明: 事件响应器是否阻止事件传播
    """
    temp: bool = False
    """
    :类型: ``bool``
    :说明: 事件响应器是否为临时
    """
    expire_time: Optional[datetime] = None
    """
    :类型: ``Optional[datetime]``
    :说明: 事件响应器过期时间点
    """

    _default_state: T_State = {}
    """
    :类型: ``T_State``
    :说明: 事件响应器默认状态
    """
    _default_state_factory: Optional[T_StateFactory] = None
    """
    :类型: ``Optional[T_State]``
    :说明: 事件响应器默认工厂函数
    """

    _default_parser: Optional[T_ArgsParser] = None
    """
    :类型: ``Optional[T_ArgsParser]``
    :说明: 事件响应器默认参数解析函数
    """
    _default_type_updater: Optional[T_TypeUpdater] = None
    """
    :类型: ``Optional[T_TypeUpdater]``
    :说明: 事件响应器类型更新函数
    """
    _default_permission_updater: Optional[T_PermissionUpdater] = None
    """
    :类型: ``Optional[T_PermissionUpdater]``
    :说明: 事件响应器权限更新函数
    """

    def __init__(self):
        """实例化 Matcher 以便运行"""
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()

    def __repr__(self) -> str:
        return (
            f"<Matcher from {self.module_name or 'unknown'}, type={self.type}, "
            f"priority={self.priority}, temp={self.temp}>")

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def new(
        cls,
        type_: str = "",
        rule: Optional[Rule] = None,
        permission: Optional[Permission] = None,
        handlers: Optional[Union[List[T_Handler], List[Handler],
                                 List[Union[T_Handler, Handler]]]] = None,
        temp: bool = False,
        priority: int = 1,
        block: bool = False,
        *,
        module: Optional[ModuleType] = None,
        expire_time: Optional[datetime] = None,
        default_state: Optional[T_State] = None,
        default_state_factory: Optional[T_StateFactory] = None,
        default_parser: Optional[T_ArgsParser] = None,
        default_type_updater: Optional[T_TypeUpdater] = None,
        default_permission_updater: Optional[T_PermissionUpdater] = None
    ) -> Type["Matcher"]:
        """
        :说明:

          创建一个新的事件响应器，并存储至 `matchers <#matchers>`_

        :参数:

          * ``type_: str``: 事件响应器类型，与 ``event.get_type()`` 一致时触发，空字符串表示任意
          * ``rule: Optional[Rule]``: 匹配规则
          * ``permission: Optional[Permission]``: 权限
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器，即触发一次后删除
          * ``priority: int``: 响应优先级
          * ``block: bool``: 是否阻止事件向更低优先级的响应器传播
          * ``module: Optional[str]``: 事件响应器所在模块名称
          * ``default_state: Optional[T_State]``: 默认状态 ``state``
          * ``default_state_factory: Optional[T_StateFactory]``: 默认状态 ``state`` 的工厂函数
          * ``expire_time: Optional[datetime]``: 事件响应器最终有效时间点，过时即被删除

        :返回:

          - ``Type[Matcher]``: 新的事件响应器类
        """

        NewMatcher = type(
            "Matcher", (Matcher,), {
                "module":
                    module,
                "plugin_name":
                    module and getattr(module, "__plugin_name__", None),
                "module_name":
                    module and getattr(module, "__module_name__", None),
                "module_prefix":
                    module and getattr(module, "__module_prefix__", None),
                "type":
                    type_,
                "rule":
                    rule or Rule(),
                "permission":
                    permission or Permission(),
                "handlers": [
                    handler
                    if isinstance(handler, Handler) else Handler(handler)
                    for handler in handlers
                ] if handlers else [],
                "temp":
                    temp,
                "expire_time":
                    expire_time,
                "priority":
                    priority,
                "block":
                    block,
                "_default_state":
                    default_state or {},
                "_default_state_factory":
                    staticmethod(default_state_factory)
                    if default_state_factory else None,
                "_default_parser":
                    default_parser,
                "_default_type_updater":
                    default_type_updater,
                "_default_permission_updater":
                    default_permission_updater
            })

        matchers[priority].append(NewMatcher)

        return NewMatcher

    @classmethod
    async def check_perm(cls, bot: "Bot", event: "Event") -> bool:
        """
        :说明:

          检查是否满足触发权限

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: 上报事件

        :返回:

          - ``bool``: 是否满足权限
        """
        event_type = event.get_type()
        return (event_type == (cls.type or event_type) and
                await cls.permission(bot, event))

    @classmethod
    async def check_rule(cls, bot: "Bot", event: "Event",
                         state: T_State) -> bool:
        """
        :说明:

          检查是否满足匹配规则

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: 上报事件
          * ``state: T_State``: 当前状态

        :返回:

          - ``bool``: 是否满足匹配规则
        """
        event_type = event.get_type()
        return (event_type == (cls.type or event_type) and
                await cls.rule(bot, event, state))

    @classmethod
    def args_parser(cls, func: T_ArgsParser) -> T_ArgsParser:
        """
        :说明:

          装饰一个函数来更改当前事件响应器的默认参数解析函数

        :参数:

          * ``func: T_ArgsParser``: 参数解析函数
        """
        cls._default_parser = func
        return func

    @classmethod
    def type_updater(cls, func: T_TypeUpdater) -> T_TypeUpdater:
        """
        :说明:

          装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数

        :参数:

          * ``func: T_TypeUpdater``: 响应事件类型更新函数
        """
        cls._default_type_updater = func
        return func

    @classmethod
    def permission_updater(cls,
                           func: T_PermissionUpdater) -> T_PermissionUpdater:
        """
        :说明:

          装饰一个函数来更改当前事件响应器的默认会话权限更新函数

        :参数:

          * ``func: T_PermissionUpdater``: 会话权限更新函数
        """
        cls._default_permission_updater = func
        return func

    @classmethod
    def append_handler(cls, handler: T_Handler) -> Handler:
        handler_ = Handler(handler)
        cls.handlers.append(handler_)
        return handler_

    @classmethod
    def handle(cls) -> Callable[[T_Handler], T_Handler]:
        """
        :说明:

          装饰一个函数来向事件响应器直接添加一个处理函数

        :参数:

          * 无
        """

        def _decorator(func: T_Handler) -> T_Handler:
            cls.append_handler(func)
            return func

        return _decorator

    @classmethod
    def receive(cls) -> Callable[[T_Handler], T_Handler]:
        """
        :说明:

          装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数

        :参数:

          * 无
        """

        async def _receive(bot: "Bot", event: "Event") -> NoReturn:
            raise PausedException

        if cls.handlers:
            # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
            receive_handler = cls.append_handler(_receive)
        else:
            receive_handler = None

        def _decorator(func: T_Handler) -> T_Handler:
            if not cls.handlers or cls.handlers[-1] is not func:
                func_handler = cls.append_handler(func)
                if receive_handler:
                    receive_handler.update_signature(
                        bot=func_handler.bot_type,
                        event=func_handler.event_type)

            return func

        return _decorator

    @classmethod
    def got(
        cls,
        key: str,
        prompt: Optional[Union[str, "Message", "MessageSegment"]] = None,
        args_parser: Optional[T_ArgsParser] = None
    ) -> Callable[[T_Handler], T_Handler]:
        """
        :说明:

          装饰一个函数来指示 NoneBot 当要获取的 ``key`` 不存在时接收用户新的一条消息并经过 ``ArgsParser`` 处理后再运行该函数，如果 ``key`` 已存在则直接继续运行

        :参数:

          * ``key: str``: 参数名
          * ``prompt: Optional[Union[str, Message, MessageSegment]]``: 在参数不存在时向用户发送的消息
          * ``args_parser: Optional[T_ArgsParser]``: 可选参数解析函数，空则使用默认解析函数
        """

        async def _key_getter(bot: "Bot", event: "Event", state: T_State):
            state["_current_key"] = key
            if key not in state:
                if prompt:
                    if isinstance(prompt, str):
                        await bot.send(event=event,
                                       message=prompt.format(**state))
                    elif isinstance(prompt, Mapping):
                        if prompt.is_text():
                            await bot.send(event=event,
                                           message=str(prompt).format(**state))
                        else:
                            await bot.send(event=event, message=prompt)
                    elif isinstance(prompt, Iterable):
                        await bot.send(
                            event=event,
                            message=prompt.__class__(
                                str(prompt).format(**state))  # type: ignore
                        )
                    else:
                        logger.warning("Unknown prompt type, ignored.")
                raise PausedException
            else:
                state["_skip_key"] = True

        async def _key_parser(bot: "Bot", event: "Event", state: T_State):
            if key in state and state.get("_skip_key"):
                del state["_skip_key"]
                return
            parser = args_parser or cls._default_parser
            if parser:
                # parser = cast(T_ArgsParser["Bot", "Event"], parser)
                await parser(bot, event, state)
            else:
                state[state["_current_key"]] = str(event.get_message())

        getter_handler = cls.append_handler(_key_getter)
        parser_handler = cls.append_handler(_key_parser)

        def _decorator(func: T_Handler) -> T_Handler:
            if not hasattr(cls.handlers[-1], "__wrapped__"):
                parser = cls.handlers.pop()
                func_handler = Handler(func)

                @wraps(func)
                async def wrapper(bot: "Bot", event: "Event", state: T_State,
                                  matcher: Matcher):
                    await parser(matcher, bot, event, state)
                    await func_handler(matcher, bot, event, state)
                    if "_current_key" in state:
                        del state["_current_key"]

                wrapper_handler = cls.append_handler(wrapper)

                getter_handler.update_signature(
                    bot=wrapper_handler.bot_type,
                    event=wrapper_handler.event_type)
                parser_handler.update_signature(
                    bot=wrapper_handler.bot_type,
                    event=wrapper_handler.event_type)

            return func

        return _decorator

    @classmethod
    async def send(cls, message: Union[str, "Message", "MessageSegment"],
                   **kwargs) -> Any:
        """
        :说明:

          发送一条消息给当前交互用户

        :参数:

          * ``message: Union[str, Message, MessageSegment]``: 消息内容
          * ``**kwargs``: 其他传递给 ``bot.send`` 的参数，请参考对应 adapter 的 bot 对象 api
        """
        bot: "Bot" = current_bot.get()
        event = current_event.get()
        return await bot.send(event=event, message=message, **kwargs)

    @classmethod
    async def finish(cls,
                     message: Optional[Union[str, "Message",
                                             "MessageSegment"]] = None,
                     **kwargs) -> NoReturn:
        """
        :说明:

          发送一条消息给当前交互用户并结束当前事件响应器

        :参数:

          * ``message: Union[str, Message, MessageSegment]``: 消息内容
          * ``**kwargs``: 其他传递给 ``bot.send`` 的参数，请参考对应 adapter 的 bot 对象 api
        """
        bot = current_bot.get()
        event = current_event.get()
        if message:
            await bot.send(event=event, message=message, **kwargs)
        raise FinishedException

    @classmethod
    async def pause(cls,
                    prompt: Optional[Union[str, "Message",
                                           "MessageSegment"]] = None,
                    **kwargs) -> NoReturn:
        """
        :说明:

          发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数

        :参数:

          * ``prompt: Union[str, Message, MessageSegment]``: 消息内容
          * ``**kwargs``: 其他传递给 ``bot.send`` 的参数，请参考对应 adapter 的 bot 对象 api
        """
        bot = current_bot.get()
        event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt, **kwargs)
        raise PausedException

    @classmethod
    async def reject(cls,
                     prompt: Optional[Union[str, "Message",
                                            "MessageSegment"]] = None,
                     **kwargs) -> NoReturn:
        """
        :说明:

          发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后重新运行当前处理函数

        :参数:

          * ``prompt: Union[str, Message, MessageSegment]``: 消息内容
          * ``**kwargs``: 其他传递给 ``bot.send`` 的参数，请参考对应 adapter 的 bot 对象 api
        """
        bot = current_bot.get()
        event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt, **kwargs)
        raise RejectedException

    def stop_propagation(self):
        """
        :说明:

          阻止事件传播
        """
        self.block = True

    # 运行handlers
    async def run(self, bot: "Bot", event: "Event", state: T_State):
        b_t = current_bot.set(bot)
        e_t = current_event.set(event)
        try:
            # Refresh preprocess state
            self.state = await self._default_state_factory(
                bot, event) if self._default_state_factory else self.state
            self.state.update(state)

            while self.handlers:
                handler = self.handlers.pop(0)
                await handler(self, bot, event, self.state)

        except RejectedException:
            self.handlers.insert(0, handler)  # type: ignore
            updater = self.__class__._default_type_updater
            if updater:
                type_ = await updater(
                    bot,
                    event,
                    self.state,  # type: ignore
                    self.type)
            else:
                type_ = "message"

            updater = self.__class__._default_permission_updater
            if updater:
                permission = await updater(
                    bot,
                    event,
                    self.state,  # type: ignore
                    self.permission)
            else:
                permission = USER(event.get_session_id(), perm=self.permission)

            Matcher.new(
                type_,
                Rule(),
                permission,
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                expire_time=datetime.now() + bot.config.session_expire_timeout,
                default_state=self.state,
                default_parser=self.__class__._default_parser,
                default_type_updater=self.__class__._default_type_updater,
                default_permission_updater=self.__class__.
                _default_permission_updater)
        except PausedException:
            updater = self.__class__._default_type_updater
            if updater:
                type_ = await updater(
                    bot,
                    event,
                    self.state,  # type: ignore
                    self.type)
            else:
                type_ = "message"

            updater = self.__class__._default_permission_updater
            if updater:
                permission = await updater(
                    bot,
                    event,
                    self.state,  # type: ignore
                    self.permission)
            else:
                permission = USER(event.get_session_id(), perm=self.permission)

            Matcher.new(
                type_,
                Rule(),
                permission,
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                expire_time=datetime.now() + bot.config.session_expire_timeout,
                default_state=self.state,
                default_parser=self.__class__._default_parser,
                default_type_updater=self.__class__._default_type_updater,
                default_permission_updater=self.__class__.
                _default_permission_updater)
        except FinishedException:
            pass
        except StopPropagation:
            self.block = True
        finally:
            logger.info(f"Matcher {self} running complete")
            current_bot.reset(b_t)
            current_event.reset(e_t)
