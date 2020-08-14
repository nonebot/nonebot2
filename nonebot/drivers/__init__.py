#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from ipaddress import IPv4Address

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.typing import Bot, Dict, Type, Optional, Callable


class BaseDriver(abc.ABC):
    _adapters: Dict[str, Type[Bot]] = {}

    @abc.abstractmethod
    def __init__(self, env: Env, config: Config):
        self.env = env.environment
        self.config = config
        self._clients: Dict[str, Bot] = {}

    @classmethod
    def register_adapter(cls, name: str, adapter: Type[Bot]):
        cls._adapters[name] = adapter
        logger.debug(f'Succeeded to load adapter "{name}"')

    @property
    @abc.abstractmethod
    def type(self):
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

    @property
    def bots(self) -> Dict[str, Bot]:
        return self._clients

    @abc.abstractmethod
    def on_startup(self, func: Callable) -> Callable:
        raise NotImplementedError

    @abc.abstractmethod
    def on_shutdown(self, func: Callable) -> Callable:
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
