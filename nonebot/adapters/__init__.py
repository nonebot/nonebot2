#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from nonebot.config import Config


class BaseBot(object):

    def __init__(self, type: str, config: Config, *, websocket=None):
        raise NotImplementedError

    async def handle_message(self, message: dict):
        raise NotImplementedError

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

    def __init__(self, message: str = None):
        raise NotImplementedError

    def __str__(self):
        return ''.join((str(seg) for seg in self))
