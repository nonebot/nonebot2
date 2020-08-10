#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from functools import reduce
from dataclasses import dataclass, field
from nonebot.rule import notice

from nonebot.config import Config
from nonebot.typing import Dict, Union, Iterable, WebSocket


class BaseBot(abc.ABC):

    @abc.abstractmethod
    def __init__(self,
                 connection_type: str,
                 config: Config,
                 self_id: int,
                 *,
                 websocket: WebSocket = None):
        self.connection_type = connection_type
        self.config = config
        self.self_id = self_id
        self.websocket = websocket

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


class BaseEvent(abc.ABC):

    def __init__(self, raw_event: dict):
        self._raw_event = raw_event

    def __repr__(self) -> str:
        # TODO: pretty print
        return f"<Event: >"

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    @type.setter
    @abc.abstractmethod
    def type(self, value):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def detail_type(self):
        raise NotImplementedError

    @detail_type.setter
    @abc.abstractmethod
    def detail_type(self, value):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sub_type(self):
        raise NotImplementedError

    @sub_type.setter
    @abc.abstractmethod
    def sub_type(self, value):
        raise NotImplementedError


@dataclass
class BaseMessageSegment(abc.ABC):
    type: str
    data: Dict[str, str] = field(default_factory=lambda: {})

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __add__(self, other):
        raise NotImplementedError


class BaseMessage(list, abc.ABC):

    def __init__(self,
                 message: Union[str, BaseMessageSegment, "BaseMessage"] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(message, str):
            self.extend(self._construct(message))
        elif isinstance(message, BaseMessage):
            self.extend(message)
        elif isinstance(message, BaseMessageSegment):
            self.append(message)

    def __str__(self):
        return ''.join((str(seg) for seg in self))

    @staticmethod
    @abc.abstractmethod
    def _construct(msg: str) -> Iterable[BaseMessageSegment]:
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
