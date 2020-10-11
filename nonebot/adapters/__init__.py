#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协议适配基类
============

各协议请继承以下基类，并使用 ``driver.register_adapter`` 注册适配器
"""

import abc
from functools import reduce, partial
from dataclasses import dataclass, field

from nonebot.config import Config
from nonebot.typing import Driver, Message, WebSocket
from nonebot.typing import Any, Dict, Union, Optional, Callable, Iterable, Awaitable


class BaseBot(abc.ABC):
    """
    Bot 基类。用于处理上报消息，并提供 API 调用接口。
    """

    @abc.abstractmethod
    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: Optional[WebSocket] = None):
        """
        :参数:
          * ``driver: Driver``: Driver 对象
          * ``connection_type: str``: http 或者 websocket
          * ``config: Config``: Config 对象
          * ``self_id: str``: 机器人 ID
          * ``websocket: Optional[WebSocket]``: Websocket 连接对象
        """
        self.driver = driver
        """Driver 对象"""
        self.connection_type = connection_type
        """连接类型"""
        self.config = config
        """Config 配置对象"""
        self.self_id = self_id
        """机器人 ID"""
        self.websocket = websocket
        """Websocket 连接对象"""

    def __getattr__(self, name: str) -> Callable[..., Awaitable[Any]]:
        return partial(self.call_api, name)

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """Adapter 类型"""
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, message: dict):
        """
        :说明:
          处理上报消息的函数，转换为 ``Event`` 事件后调用 ``nonebot.message.handle_event`` 进一步处理事件。
        :参数:
          * ``message: dict``: 收到的上报消息
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def call_api(self, api: str, **data):
        """
        :说明:
          调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用
        :参数:
          * ``api: str``: API 名称
          * ``**data``: API 数据
        :示例:

        .. code-block:: python

            await bot.call_api("send_msg", data={"message": "hello world"})
            await bot.send_msg(message="hello world")
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, event: "BaseEvent",
                   message: Union[str, "BaseMessage",
                                  "BaseMessageSegment"], **kwargs):
        """
        :说明:
          调用机器人基础发送消息接口
        :参数:
          * ``event: Event``: 上报事件
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``**kwargs``
        """
        raise NotImplementedError


class BaseEvent(abc.ABC):
    """
    Event 基类。提供上报信息的关键信息，其余信息可从原始上报消息获取。
    """

    def __init__(self, raw_event: dict):
        """
        :参数:
          * ``raw_event: dict``: 原始上报消息
        """
        self._raw_event = raw_event

    def __repr__(self) -> str:
        return f"<Event {self.self_id}: {self.name} {self.time}>"

    @property
    def raw_event(self) -> dict:
        """原始上报消息"""
        return self._raw_event

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """事件 ID"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """事件名称"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def self_id(self) -> str:
        """机器人 ID"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def time(self) -> int:
        """事件发生时间"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """事件主类型"""
        raise NotImplementedError

    @type.setter
    @abc.abstractmethod
    def type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def detail_type(self) -> str:
        """事件详细类型"""
        raise NotImplementedError

    @detail_type.setter
    @abc.abstractmethod
    def detail_type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sub_type(self) -> Optional[str]:
        """事件子类型"""
        raise NotImplementedError

    @sub_type.setter
    @abc.abstractmethod
    def sub_type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def user_id(self) -> Optional[int]:
        """触发事件的主体 ID"""
        raise NotImplementedError

    @user_id.setter
    @abc.abstractmethod
    def user_id(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def group_id(self) -> Optional[int]:
        """触发事件的主体群 ID"""
        raise NotImplementedError

    @group_id.setter
    @abc.abstractmethod
    def group_id(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def to_me(self) -> Optional[bool]:
        """事件是否为发送给机器人的消息"""
        raise NotImplementedError

    @to_me.setter
    @abc.abstractmethod
    def to_me(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def message(self) -> Optional[Message]:
        """消息内容"""
        raise NotImplementedError

    @message.setter
    @abc.abstractmethod
    def message(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def reply(self) -> Optional[dict]:
        """回复的消息"""
        raise NotImplementedError

    @reply.setter
    @abc.abstractmethod
    def reply(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def raw_message(self) -> Optional[str]:
        """原始消息"""
        raise NotImplementedError

    @raw_message.setter
    @abc.abstractmethod
    def raw_message(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def plain_text(self) -> Optional[str]:
        """纯文本消息"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sender(self) -> Optional[dict]:
        """消息发送者信息"""
        raise NotImplementedError

    @sender.setter
    @abc.abstractmethod
    def sender(self, value) -> None:
        raise NotImplementedError


@dataclass
class BaseMessageSegment(abc.ABC):
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

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __add__(self, other):
        raise NotImplementedError

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    @classmethod
    @abc.abstractmethod
    def text(cls, text: str) -> "BaseMessageSegment":
        return cls("text", {"text": text})


class BaseMessage(list, abc.ABC):
    """消息数组"""

    def __init__(self,
                 message: Union[str, dict, list, BaseMessageSegment,
                                "BaseMessage"] = None,
                 *args,
                 **kwargs):
        """
        :参数:
          * ``message: Union[str, dict, list, MessageSegment, Message]``: 消息内容
        """
        super().__init__(*args, **kwargs)
        if isinstance(message, (str, dict, list)):
            self.extend(self._construct(message))
        elif isinstance(message, BaseMessage):
            self.extend(message)
        elif isinstance(message, BaseMessageSegment):
            self.append(message)

    def __str__(self):
        return ''.join((str(seg) for seg in self))

    @staticmethod
    @abc.abstractmethod
    def _construct(msg: Union[str, dict, list]) -> Iterable[BaseMessageSegment]:
        raise NotImplementedError

    def __add__(
            self, other: Union[str, BaseMessageSegment,
                               "BaseMessage"]) -> "BaseMessage":
        result = self.__class__(self)
        if isinstance(other, str):
            result.extend(self._construct(other))
        elif isinstance(other, BaseMessageSegment):
            result.append(other)
        elif isinstance(other, BaseMessage):
            result.extend(other)
        return result

    def __radd__(self, other: Union[str, BaseMessageSegment, "BaseMessage"]):
        result = self.__class__(other)
        return result.__add__(self)

    def append(self, obj: Union[str, BaseMessageSegment]) -> "BaseMessage":
        """
        :说明:
          添加一个消息段到消息数组末尾
        :参数:
          * ``obj: Union[str, MessageSegment]``: 要添加的消息段
        """
        if isinstance(obj, BaseMessageSegment):
            if obj.type == "text" and self and self[-1].type == "text":
                self[-1].data["text"] += obj.data["text"]
            else:
                super().append(obj)
        elif isinstance(obj, str):
            self.extend(self._construct(obj))
        else:
            raise ValueError(f"Unexpected type: {type(obj)} {obj}")
        return self

    def extend(
        self, obj: Union["BaseMessage",
                         Iterable[BaseMessageSegment]]) -> "BaseMessage":
        """
        :说明:
          拼接一个消息数组或多个消息段到消息数组末尾
        :参数:
          * ``obj: Union[Message, Iterable[MessageSegment]]``: 要添加的消息数组
        """
        for segment in obj:
            self.append(segment)
        return self

    def reduce(self) -> None:
        """
        :说明:
          缩减消息数组，即拼接相邻纯文本消息段
        """
        index = 0
        while index < len(self):
            if index > 0 and self[
                    index - 1].type == "text" and self[index].type == "text":
                self[index - 1].data["text"] += self[index].data["text"]
                del self[index]
            else:
                index += 1

    def extract_plain_text(self) -> str:
        """
        :说明:
          提取消息内纯文本消息
        """

        def _concat(x: str, y: BaseMessageSegment) -> str:
            return f"{x} {y.data['text']}" if y.type == "text" else x

        plain_text = reduce(_concat, self, "")
        return plain_text[1:] if plain_text else plain_text
