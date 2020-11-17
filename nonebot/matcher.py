"""
事件响应器
==========

该模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行 对话 。
"""

from nonebot.log import logger
import typing
import inspect
from functools import wraps
from datetime import datetime
from contextvars import ContextVar
from collections import defaultdict

from nonebot.rule import Rule
from nonebot.permission import Permission, USER
from nonebot.typing import Type, List, Dict, Union, Callable, Optional, NoReturn
from nonebot.typing import Bot, Event, Handler, Message, ArgsParser, MessageSegment
from nonebot.exception import PausedException, RejectedException, FinishedException

matchers: Dict[int, List[Type["Matcher"]]] = defaultdict(list)
"""
:类型: ``Dict[int, List[Type[Matcher]]]``
:说明: 用于存储当前所有的事件响应器
"""
current_bot: ContextVar = ContextVar("current_bot")
current_event: ContextVar = ContextVar("current_event")


class MatcherMeta(type):

    def __repr__(self) -> str:
        return (f"<Matcher from {self.module or 'unknow'}, "  # type: ignore
                f"type={self.type}, priority={self.priority}, "  # type: ignore
                f"temp={self.temp}>")  # type: ignore

    def __str__(self) -> str:
        return repr(self)


class Matcher(metaclass=MatcherMeta):
    """事件响应器类"""
    module: Optional[str] = None
    """
    :类型: ``Optional[str]``
    :说明: 事件响应器所在模块名称
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

    _default_state: dict = {}
    """
    :类型: ``dict``
    :说明: 事件响应器默认状态
    """

    _default_parser: Optional[ArgsParser] = None
    """
    :类型: ``Optional[ArgsParser]``
    :说明: 事件响应器默认参数解析函数
    """

    def __init__(self):
        """实例化 Matcher 以便运行
        """
        self.handlers = self.handlers.copy()
        self.state = self._default_state.copy()

    def __repr__(self) -> str:
        return (f"<Matcher from {self.module or 'unknow'}, type={self.type}, "
                f"priority={self.priority}, temp={self.temp}>")

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def new(cls,
            type_: str = "",
            rule: Optional[Rule] = None,
            permission: Optional[Permission] = None,
            handlers: Optional[List[Handler]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            *,
            module: Optional[str] = None,
            default_state: Optional[dict] = None,
            expire_time: Optional[datetime] = None) -> Type["Matcher"]:
        """
        :说明:
          创建一个新的事件响应器，并存储至 `matchers <#matchers>`_
        :参数:
          * ``type_: str``: 事件响应器类型，与 ``event.type`` 一致时触发，空字符串表示任意
          * ``rule: Optional[Rule]``: 匹配规则
          * ``permission: Optional[Permission]``: 权限
          * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器，即触发一次后删除
          * ``priority: int``: 响应优先级
          * ``block: bool``: 是否阻止事件向更低优先级的响应器传播
          * ``module: Optional[str]``: 事件响应器所在模块名称
          * ``default_state: Optional[dict]``: 默认状态 ``state``
          * ``expire_time: Optional[datetime]``: 事件响应器最终有效时间点，过时即被删除
        :返回:
          - ``Type[Matcher]``: 新的事件响应器类
        """

        NewMatcher = type(
            "Matcher", (Matcher,), {
                "module": module,
                "type": type_,
                "rule": rule or Rule(),
                "permission": permission or Permission(),
                "handlers": handlers or [],
                "temp": temp,
                "expire_time": expire_time,
                "priority": priority,
                "block": block,
                "_default_state": default_state or {}
            })

        matchers[priority].append(NewMatcher)

        return NewMatcher

    @classmethod
    async def check_perm(cls, bot: Bot, event: Event) -> bool:
        """
        :说明:
          检查是否满足触发权限
        :参数:
          * ``bot: Bot``: Bot 对象
          * ``event: Event``: 上报事件
        :返回:
          - ``bool``: 是否满足权限
        """
        return await cls.permission(bot, event)

    @classmethod
    async def check_rule(cls, bot: Bot, event: Event, state: dict) -> bool:
        """
        :说明:
          检查是否满足匹配规则
        :参数:
          * ``bot: Bot``: Bot 对象
          * ``event: Event``: 上报事件
          * ``state: dict``: 当前状态
        :返回:
          - ``bool``: 是否满足匹配规则
        """
        return (event.type == (cls.type or event.type) and
                await cls.rule(bot, event, state))

    @classmethod
    def args_parser(cls, func: ArgsParser) -> ArgsParser:
        """
        :说明:
          装饰一个函数来更改当前事件响应器的默认参数解析函数
        :参数:
          * ``func: ArgsParser``: 参数解析函数
        """
        cls._default_parser = func
        return func

    @classmethod
    def handle(cls) -> Callable[[Handler], Handler]:
        """
        :说明:
          装饰一个函数来向事件响应器直接添加一个处理函数
        :参数:
          * 无
        """

        def _decorator(func: Handler) -> Handler:
            cls.handlers.append(func)
            return func

        return _decorator

    @classmethod
    def receive(cls) -> Callable[[Handler], Handler]:
        """
        :说明:
          装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数
        :参数:
          * 无
        """

        async def _receive(bot: Bot, event: Event, state: dict) -> NoReturn:
            raise PausedException

        if cls.handlers:
            # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
            cls.handlers.append(_receive)

        def _decorator(func: Handler) -> Handler:
            if not cls.handlers or cls.handlers[-1] is not func:
                cls.handlers.append(func)

            return func

        return _decorator

    @classmethod
    def got(
        cls,
        key: str,
        prompt: Optional[Union[str, Message, MessageSegment]] = None,
        args_parser: Optional[ArgsParser] = None
    ) -> Callable[[Handler], Handler]:
        """
        :说明:
          装饰一个函数来指示 NoneBot 当要获取的 ``key`` 不存在时接收用户新的一条消息并经过 ``ArgsParser`` 处理后再运行该函数，如果 ``key`` 已存在则直接继续运行
        :参数:
          * ``key: str``: 参数名
          * ``prompt: Optional[Union[str, Message, MessageSegment]]``: 在参数不存在时向用户发送的消息
          * ``args_parser: Optional[ArgsParser]``: 可选参数解析函数，空则使用默认解析函数
        """

        async def _key_getter(bot: Bot, event: Event, state: dict):
            state["_current_key"] = key
            if key not in state:
                if prompt:
                    await bot.send(event=event,
                                   message=str(prompt).format(**state))
                raise PausedException
            else:
                state["_skip_key"] = True

        async def _key_parser(bot: Bot, event: Event, state: dict):
            if key in state and state.get("_skip_key"):
                del state["_skip_key"]
                return
            parser = args_parser or cls._default_parser
            if parser:
                await parser(bot, event, state)
            else:
                state[state["_current_key"]] = str(event.message)

        cls.handlers.append(_key_getter)
        cls.handlers.append(_key_parser)

        def _decorator(func: Handler) -> Handler:
            if not hasattr(cls.handlers[-1], "__wrapped__"):
                parser = cls.handlers.pop()

                @wraps(func)
                async def wrapper(bot: Bot, event: Event, state: dict):
                    await parser(bot, event, state)
                    await func(bot, event, state)
                    if "_current_key" in state:
                        del state["_current_key"]

                cls.handlers.append(wrapper)

            return func

        return _decorator

    @classmethod
    async def send(cls, message: Union[str, Message, MessageSegment], **kwargs):
        """
        :说明:
          发送一条消息给当前交互用户
        :参数:
          * ``message: Union[str, Message, MessageSegment]``: 消息内容
          * ``**kwargs``: 其他传递给 ``bot.send`` 的参数，请参考对应 adapter 的 bot 对象 api
        """
        bot = current_bot.get()
        event = current_event.get()
        await bot.send(event=event, message=message, **kwargs)

    @classmethod
    async def finish(cls,
                     message: Optional[Union[str, Message,
                                             MessageSegment]] = None,
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
                    prompt: Optional[Union[str, Message,
                                           MessageSegment]] = None,
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
                     prompt: Optional[Union[str, Message,
                                            MessageSegment]] = None,
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

    # 运行handlers
    async def run(self, bot: Bot, event: Event, state: dict):
        b_t = current_bot.set(bot)
        e_t = current_event.set(event)
        try:
            # Refresh preprocess state
            self.state.update(state)

            for _ in range(len(self.handlers)):
                handler = self.handlers.pop(0)
                annotation = typing.get_type_hints(handler)
                BotType = annotation.get("bot")
                if BotType and inspect.isclass(BotType) and not isinstance(
                        bot, BotType):
                    continue
                await handler(bot, event, self.state)

        except RejectedException:
            self.handlers.insert(0, handler)  # type: ignore
            Matcher.new(
                self.type,
                Rule(),
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
        except PausedException:
            Matcher.new(
                self.type,
                Rule(),
                USER(event.user_id, perm=self.permission),  # type:ignore
                self.handlers,
                temp=True,
                priority=0,
                block=True,
                module=self.module,
                default_state=self.state,
                expire_time=datetime.now() + bot.config.session_expire_timeout)
        except FinishedException:
            pass
        finally:
            logger.info(f"Matcher {self} running complete")
            current_bot.reset(b_t)
            current_event.reset(e_t)


class MatcherGroup:
    """事件响应器组合，统一管理。用法同 ``Matcher``"""

    def __init__(self,
                 type_: str = "",
                 rule: Optional[Rule] = None,
                 permission: Optional[Permission] = None,
                 handlers: Optional[list] = None,
                 temp: bool = False,
                 priority: int = 1,
                 block: bool = False,
                 *,
                 module: Optional[str] = None,
                 default_state: Optional[dict] = None,
                 expire_time: Optional[datetime] = None):
        """
        :说明:
          创建一个事件响应器组合，参数为默认值，与 ``Matcher.new`` 一致
        """
        self.matchers: List[Type[Matcher]] = []
        """
        :类型: ``List[Type[Matcher]]``
        :说明: 组内事件响应器列表
        """

        self.type = type_
        self.rule = rule or Rule()
        self.permission = permission or Permission()
        self.handlers = handlers
        self.temp = temp
        self.priority = priority
        self.block = block
        self.module = module
        self.expire_time = expire_time

        self._default_state = default_state

        self._default_parser: Optional[ArgsParser] = None

    def __repr__(self) -> str:
        return (
            f"<MatcherGroup from {self.module or 'unknow'}, type={self.type}, "
            f"priority={self.priority}, temp={self.temp}>")

    def __str__(self) -> str:
        return self.__repr__()

    def new(self,
            type_: str = "",
            rule: Optional[Rule] = None,
            permission: Optional[Permission] = None,
            handlers: Optional[list] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            *,
            module: Optional[str] = None,
            default_state: Optional[dict] = None,
            expire_time: Optional[datetime] = None) -> Type[Matcher]:
        """
        :说明:
          在组中创建一个新的事件响应器，参数留空则使用组合默认值

        \:\:\:danger 警告
        如果使用 handlers 参数覆盖组合默认值则该事件响应器不会随组合一起添加新的事件处理函数
        \:\:\:
        """
        matcher = Matcher.new(type_=type_ or self.type,
                              rule=self.rule & rule,
                              permission=permission or self.permission,
                              handlers=handlers or self.handlers,
                              temp=temp or self.temp,
                              priority=priority or self.priority,
                              block=block or self.block,
                              module=module or self.module,
                              default_state=default_state or
                              self._default_state,
                              expire_time=expire_time or self.expire_time)
        self.matchers.append(matcher)
        return matcher

    def args_parser(self, func: ArgsParser) -> ArgsParser:
        self._default_parser = func
        for matcher in self.matchers:
            matcher.args_parser(func)
        return func

    def handle(self) -> Callable[[Handler], Handler]:

        def _decorator(func: Handler) -> Handler:
            self.handlers.append(func)
            return func

        return _decorator

    def receive(self) -> Callable[[Handler], Handler]:

        async def _receive(bot: Bot, event: Event, state: dict) -> NoReturn:
            raise PausedException

        if self.handlers:
            # 已有前置handlers则接受一条新的消息，否则视为接收初始消息
            self.handlers.append(_receive)

        def _decorator(func: Handler) -> Handler:
            if not self.handlers or self.handlers[-1] is not func:
                self.handlers.append(func)

            return func

        return _decorator

    def got(
        self,
        key: str,
        prompt: Optional[str] = None,
        args_parser: Optional[ArgsParser] = None
    ) -> Callable[[Handler], Handler]:

        async def _key_getter(bot: Bot, event: Event, state: dict):
            state["_current_key"] = key
            if key not in state:
                if prompt:
                    await bot.send(event=event,
                                   message=str(prompt).format(state))
                raise PausedException
            else:
                state["_skip_key"] = True

        async def _key_parser(bot: Bot, event: Event, state: dict):
            if key in state and state.get("_skip_key"):
                del state["_skip_key"]
                return
            parser = args_parser or self._default_parser
            if parser:
                await parser(bot, event, state)
            else:
                state[state["_current_key"]] = str(event.message)

        self.handlers.append(_key_getter)
        self.handlers.append(_key_parser)

        def _decorator(func: Handler) -> Handler:
            if not hasattr(self.handlers[-1], "__wrapped__"):
                parser = self.handlers.pop()

                @wraps(func)
                async def wrapper(bot: Bot, event: Event, state: dict):
                    await parser(bot, event, state)
                    await func(bot, event, state)
                    if "_current_key" in state:
                        del state["_current_key"]

                self.handlers.append(wrapper)

            return func

        return _decorator

    async def send(self, message: Union[str, Message, MessageSegment],
                   **kwargs):
        bot = current_bot.get()
        event = current_event.get()
        await bot.send(event=event, message=message, **kwargs)

    async def finish(self,
                     message: Optional[Union[str, Message,
                                             MessageSegment]] = None,
                     **kwargs) -> NoReturn:
        bot = current_bot.get()
        event = current_event.get()
        if message:
            await bot.send(event=event, message=message, **kwargs)
        raise FinishedException

    async def pause(self,
                    prompt: Optional[Union[str, Message,
                                           MessageSegment]] = None,
                    **kwargs) -> NoReturn:
        bot = current_bot.get()
        event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt, **kwargs)
        raise PausedException

    async def reject(self,
                     prompt: Optional[Union[str, Message,
                                            MessageSegment]] = None,
                     **kwargs) -> NoReturn:
        bot = current_bot.get()
        event = current_event.get()
        if prompt:
            await bot.send(event=event, message=prompt, **kwargs)
        raise RejectedException
