"""
协议适配基类
============

各协议请继承以下基类，并使用 ``driver.register_adapter`` 注册适配器
"""

import abc
import asyncio
from copy import deepcopy
from functools import partial
from typing_extensions import Protocol
from dataclasses import dataclass, field
from typing import (Any, Set, List, Dict, Type, Tuple, Union, TypeVar, Mapping,
                    Generic, Optional, Iterable)

from pydantic import BaseModel

from nonebot.log import logger
from nonebot.config import Config
from nonebot.utils import DataclassEncoder
from nonebot.drivers import Driver, HTTPConnection, HTTPResponse
from nonebot.typing import T_CallingAPIHook, T_CalledAPIHook


class _ApiCall(Protocol):

    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Bot(abc.ABC):
    """
    Bot 基类。用于处理上报消息，并提供 API 调用接口。
    """

    driver: Driver
    """Driver 对象"""
    config: Config
    """Config 配置对象"""
    _calling_api_hook: Set[T_CallingAPIHook] = set()
    """
    :类型: ``Set[T_CallingAPIHook]``
    :说明: call_api 时执行的函数
    """
    _called_api_hook: Set[T_CalledAPIHook] = set()
    """
    :类型: ``Set[T_CalledAPIHook]``
    :说明: call_api 后执行的函数
    """

    def __init__(self, self_id: str, request: HTTPConnection):
        """
        :参数:

          * ``self_id: str``: 机器人 ID
          * ``request: HTTPConnection``: request 连接对象
        """
        self.self_id: str = self_id
        """机器人 ID"""
        self.request: HTTPConnection = request
        """连接信息"""

    def __getattr__(self, name: str) -> _ApiCall:
        return partial(self.call_api, name)

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """Adapter 类型"""
        raise NotImplementedError

    @classmethod
    def register(cls, driver: Driver, config: Config, **kwargs):
        """
        :说明:

          ``register`` 方法会在 ``driver.register_adapter`` 时被调用，用于初始化相关配置
        """
        cls.driver = driver
        cls.config = config

    @classmethod
    @abc.abstractmethod
    async def check_permission(
        cls, driver: Driver, request: HTTPConnection
    ) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        """
        :说明:

          检查连接请求是否合法的函数，如果合法则返回当前连接 ``唯一标识符``，通常为机器人 ID；如果不合法则抛出 ``RequestDenied`` 异常。

        :参数:

          * ``driver: Driver``: Driver 对象
          * ``request: HTTPConnection``: request 请求详情

        :返回:

          - ``Optional[str]``: 连接唯一标识符，``None`` 代表连接不合法
          - ``Optional[HTTPResponse]``: HTTP 上报响应
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, message: bytes):
        """
        :说明:

          处理上报消息的函数，转换为 ``Event`` 事件后调用 ``nonebot.message.handle_event`` 进一步处理事件。

        :参数:

          * ``message: bytes``: 收到的上报消息
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _call_api(self, api: str, **data) -> Any:
        """
        :说明:

          ``adapter`` 实际调用 api 的逻辑实现函数，实现该方法以调用 api。

        :参数:

          * ``api: str``: API 名称
          * ``**data``: API 数据
        """
        raise NotImplementedError

    async def call_api(self, api: str, **data: Any) -> Any:
        """
        :说明:

          调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

        :参数:

          * ``api: str``: API 名称
          * ``**data``: API 数据

        :示例:

        .. code-block:: python

            await bot.call_api("send_msg", message="hello world")
            await bot.send_msg(message="hello world")
        """
        coros = list(map(lambda x: x(self, api, data), self._calling_api_hook))
        if coros:
            try:
                logger.debug("Running CallingAPI hooks...")
                await asyncio.gather(*coros)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CallingAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>")

        exception = None
        result = None

        try:
            result = await self._call_api(api, **data)
        except Exception as e:
            exception = e

        coros = list(
            map(lambda x: x(self, exception, api, data, result),
                self._called_api_hook))
        if coros:
            try:
                logger.debug("Running CalledAPI hooks...")
                await asyncio.gather(*coros)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CalledAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>")

        if exception:
            raise exception
        return result

    @abc.abstractmethod
    async def send(self, event: "Event", message: Union[str, "Message",
                                                        "MessageSegment"],
                   **kwargs) -> Any:
        """
        :说明:

          调用机器人基础发送消息接口

        :参数:

          * ``event: Event``: 上报事件
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``**kwargs``
        """
        raise NotImplementedError

    @classmethod
    def on_calling_api(cls, func: T_CallingAPIHook) -> T_CallingAPIHook:
        """
        :说明:

          调用 api 预处理。

        :参数:

          * ``bot: Bot``: 当前 bot 对象
          * ``api: str``: 调用的 api 名称
          * ``data: Dict[str, Any]``: api 调用的参数字典
        """
        cls._calling_api_hook.add(func)
        return func

    @classmethod
    def on_called_api(cls, func: T_CalledAPIHook) -> T_CalledAPIHook:
        """
        :说明:

          调用 api 后处理。

        :参数:

          * ``bot: Bot``: 当前 bot 对象
          * ``exception: Optional[Exception]``: 调用 api 时发生的错误
          * ``api: str``: 调用的 api 名称
          * ``data: Dict[str, Any]``: api 调用的参数字典
          * ``result: Any``: api 调用的返回
        """
        cls._called_api_hook.add(func)
        return func


T = TypeVar("T")
TMS = TypeVar("TMS", covariant=True)
TM = TypeVar("TM", bound="Message")


@dataclass
class MessageSegment(Mapping, abc.ABC, Generic[TM]):
    """消息段基类"""
    type: str
    """
    - 类型: ``str``
    - 说明: 消息段类型
    """
    data: Dict[str, Any] = field(default_factory=lambda: {})
    """
    - 类型: ``Dict[str, Union[str, list]]``
    - 说明: 消息段数据
    """

    @classmethod
    @abc.abstractmethod
    def get_message_class(cls) -> Type[TM]:
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        """该消息段所代表的 str，在命令匹配部分使用"""
        raise NotImplementedError

    def __len__(self) -> int:
        return len(str(self))

    def __ne__(self: T, other: T) -> bool:
        return not self == other

    def __add__(self, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        return self.get_message_class()(self) + other  # type: ignore

    def __radd__(self, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        return self.get_message_class()(other) + self  # type: ignore

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    def __iter__(self):
        yield from self.data.__iter__()

    def __contains__(self, key: Any) -> bool:
        return key in self.data

    def get(self, key: str, default: Any = None):
        return getattr(self, key, default)

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def copy(self: T) -> T:
        return deepcopy(self)

    @abc.abstractmethod
    def is_text(self) -> bool:
        raise NotImplementedError


class Message(List[TMS], abc.ABC):
    """消息数组"""

    def __init__(self: TM,
                 message: Union[str, None, Mapping, Iterable[Mapping], TMS, TM,
                                Any] = None,
                 *args,
                 **kwargs):
        """
        :参数:

          * ``message: Union[str, list, dict, MessageSegment, Message, Any]``: 消息内容
        """
        super().__init__(*args, **kwargs)
        if message is None:
            return
        elif isinstance(message, Message):
            self.extend(message)
        elif isinstance(message, MessageSegment):
            self.append(message)
        else:
            self.extend(self._construct(message))

    @classmethod
    @abc.abstractmethod
    def get_segment_class(cls) -> Type[TMS]:
        raise NotImplementedError

    def __str__(self):
        return "".join(str(seg) for seg in self)

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value):
        return cls(value)

    @staticmethod
    @abc.abstractmethod
    def _construct(
            msg: Union[str, Mapping, Iterable[Mapping], Any]) -> Iterable[TMS]:
        raise NotImplementedError

    def __add__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        result = self.copy()
        result += other
        return result

    def __radd__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        result = self.__class__(other)  # type: ignore
        return result + self

    def __iadd__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        if isinstance(other, MessageSegment):
            self.append(other)
        elif isinstance(other, Message):
            self.extend(other)
        else:
            self.extend(self._construct(other))
        return self

    def append(self: TM, obj: Union[str, TMS]) -> TM:
        """
        :说明:

          添加一个消息段到消息数组末尾

        :参数:

          * ``obj: Union[str, MessageSegment]``: 要添加的消息段
        """
        if isinstance(obj, MessageSegment):
            super(Message, self).append(obj)
        elif isinstance(obj, str):
            self.extend(self._construct(obj))
        else:
            raise ValueError(f"Unexpected type: {type(obj)} {obj}")
        return self

    def extend(self: TM, obj: Union[TM, Iterable[TMS]]) -> TM:
        """
        :说明:

          拼接一个消息数组或多个消息段到消息数组末尾

        :参数:

          * ``obj: Union[Message, Iterable[MessageSegment]]``: 要添加的消息数组
        """
        for segment in obj:
            self.append(segment)
        return self

    def copy(self: TM) -> TM:
        return deepcopy(self)

    def extract_plain_text(self: "Message[MessageSegment]") -> str:
        """
        :说明:

          提取消息内纯文本消息
        """

        return "".join(str(seg) for seg in self if seg.is_text())


class Event(abc.ABC, BaseModel):
    """Event 基类。提供获取关键信息的方法，其余信息可直接获取。"""

    class Config:
        extra = "allow"
        json_encoders = {Message: DataclassEncoder}

    @abc.abstractmethod
    def get_type(self) -> str:
        """
        :说明:

          获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。

        :返回:

          * ``Literal["message", "notice", "request", "meta_event"]``
          * 其他自定义 ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_name(self) -> str:
        """
        :说明:

          获取事件名称的方法。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_description(self) -> str:
        """
        :说明:

          获取事件描述的方法，通常为事件具体内容。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    def get_log_string(self) -> str:
        """
        :说明:

          获取事件日志信息的方法，通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 ``NoLogException`` 异常。

        :返回:

          * ``str``

        :异常:

          - ``NoLogException``
        """
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    @abc.abstractmethod
    def get_user_id(self) -> str:
        """
        :说明:

          获取事件主体 id 的方法，通常是用户 id 。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_session_id(self) -> str:
        """
        :说明:

          获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_message(self) -> Message:
        """
        :说明:

          获取事件消息内容的方法。

        :返回:

          * ``Message``
        """
        raise NotImplementedError

    def get_plaintext(self) -> str:
        """
        :说明:

          获取消息纯文本的方法，通常不需要修改，默认通过 ``get_message().extract_plain_text`` 获取。

        :返回:

          * ``str``
        """
        return self.get_message().extract_plain_text()

    @abc.abstractmethod
    def is_tome(self) -> bool:
        """
        :说明:

          获取事件是否与机器人有关的方法。

        :返回:

          * ``bool``
        """
        raise NotImplementedError
