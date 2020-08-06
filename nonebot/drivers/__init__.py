#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from typing import Optional
from ipaddress import IPv4Address

from nonebot.config import Config


class BaseDriver(abc.ABC):

    @abc.abstractmethod
    def __init__(self, config: Config):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def server_app(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def asgi(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def logger(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self,
            host: Optional[IPv4Address] = None,
            port: Optional[int] = None,
            *args,
            **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def _handle_http(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _handle_ws_reverse(self):
        raise NotImplementedError


class BaseWebSocket(object):

    @abc.abstractmethod
    def __init__(self, websocket):
        self._websocket = websocket

    @property
    @abc.abstractmethod
    def websocket(self):
        return self._websocket

    @property
    @abc.abstractmethod
    def closed(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def accept(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self, code: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def receive(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, data: dict):
        raise NotImplementedError
