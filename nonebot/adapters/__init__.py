#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from functools import reduce
from typing import Dict, Union, Iterable, Optional

from nonebot.config import Config


class BaseBot(abc.ABC):

    @abc.abstractmethod
    def __init__(self,
                 type: str,
                 config: Config,
                 self_id: int,
                 *,
                 websocket=None):
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, message: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def call_api(self, api: str, data: dict):
        raise NotImplementedError


class BaseMessageSegment(dict):

    def __init__(self,
                 type_: Optional[str] = None,
                 data: Optional[Dict[str, str]] = None):
        super().__init__()
        if type_:
            self.type = type_
            self.data = data
        else:
            raise ValueError('The "type" field cannot be empty')

    def __str__(self):
        raise NotImplementedError

    def __getitem__(self, item):
        if item not in ("type", "data"):
            raise KeyError(f'Key "{item}" is not allowed')
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if key not in ("type", "data"):
            raise KeyError(f'Key "{key}" is not allowed')
        return super().__setitem__(key, value)

    # TODO: __eq__ __add__

    @property
    def type(self) -> str:
        return self["type"]

    @type.setter
    def type(self, value: str):
        self["type"] = value

    @property
    def data(self) -> Dict[str, str]:
        return self["data"]

    @data.setter
    def data(self, data: Optional[Dict[str, str]]):
        self["data"] = data or {}


class BaseMessage(list):

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
