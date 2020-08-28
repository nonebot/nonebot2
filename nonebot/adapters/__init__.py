#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from functools import reduce, partial
from dataclasses import dataclass, field

from nonebot.config import Config
from nonebot.typing import Driver, Message, WebSocket
from nonebot.typing import Any, Dict, Union, Optional, Callable, Iterable, Awaitable


class BaseBot(abc.ABC):

    @abc.abstractmethod
    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: WebSocket = None):
        self.driver = driver
        self.connection_type = connection_type
        self.config = config
        self.self_id = self_id
        self.websocket = websocket

    def __getattr__(self, name: str) -> Callable[..., Awaitable[Any]]:
        return partial(self.call_api, name)

    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, message: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def call_api(self, api: str, data: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, *args, **kwargs):
        raise NotImplementedError


# TODO: improve event
class BaseEvent(abc.ABC):

    def __init__(self, raw_event: dict):
        self._raw_event = raw_event

    def __repr__(self) -> str:
        return f"<Event {self.self_id}: {self.name} {self.time}>"

    @property
    def raw_event(self) -> dict:
        return self._raw_event

    @property
    @abc.abstractmethod
    def id(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def self_id(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def time(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError

    @type.setter
    @abc.abstractmethod
    def type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def detail_type(self) -> str:
        raise NotImplementedError

    @detail_type.setter
    @abc.abstractmethod
    def detail_type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sub_type(self) -> Optional[str]:
        raise NotImplementedError

    @sub_type.setter
    @abc.abstractmethod
    def sub_type(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def user_id(self) -> Optional[int]:
        raise NotImplementedError

    @user_id.setter
    @abc.abstractmethod
    def user_id(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def group_id(self) -> Optional[int]:
        raise NotImplementedError

    @group_id.setter
    @abc.abstractmethod
    def group_id(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def to_me(self) -> Optional[bool]:
        raise NotImplementedError

    @to_me.setter
    @abc.abstractmethod
    def to_me(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def message(self) -> Optional[Message]:
        raise NotImplementedError

    @message.setter
    @abc.abstractmethod
    def message(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def reply(self) -> Optional[dict]:
        raise NotImplementedError

    @reply.setter
    @abc.abstractmethod
    def reply(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def raw_message(self) -> Optional[str]:
        raise NotImplementedError

    @raw_message.setter
    @abc.abstractmethod
    def raw_message(self, value) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def plain_text(self) -> Optional[str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sender(self) -> Optional[dict]:
        raise NotImplementedError

    @sender.setter
    @abc.abstractmethod
    def sender(self, value) -> None:
        raise NotImplementedError


@dataclass
class BaseMessageSegment(abc.ABC):
    type: str
    data: Dict[str, Union[str, list]] = field(default_factory=lambda: {})

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __add__(self, other):
        raise NotImplementedError


class BaseMessage(list, abc.ABC):

    def __init__(self,
                 message: Union[str, dict, list, BaseMessageSegment,
                                "BaseMessage"] = None,
                 *args,
                 **kwargs):
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
        for segment in obj:
            self.append(segment)
        return self

    def reduce(self) -> None:
        index = 0
        while index < len(self):
            if index > 0 and self[
                    index - 1].type == "text" and self[index].type == "text":
                self[index - 1].data["text"] += self[index].data["text"]
                del self[index]
            else:
                index += 1

    def extract_plain_text(self) -> str:

        def _concat(x: str, y: BaseMessageSegment) -> str:
            return f"{x} {y.data['text']}" if y.type == "text" else x

        return reduce(_concat, self, "")
