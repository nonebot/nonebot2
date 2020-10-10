#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端驱动适配基类
===============

各驱动请继承以下基类
"""

import abc

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.typing import Bot, Dict, Type, Union, Optional, Callable


class BaseDriver(abc.ABC):
    """
    Driver 基类。将后端框架封装，以满足适配器使用。
    """

    _adapters: Dict[str, Type[Bot]] = {}
    """
    :类型: ``Dict[str, Type[Bot]]``
    :说明: 已注册的适配器列表
    """

    @abc.abstractmethod
    def __init__(self, env: Env, config: Config):
        self.env = env.environment
        self.config = config
        self._clients: Dict[str, Bot] = {}

    @classmethod
    def register_adapter(cls, name: str, adapter: Type[Bot]):
        cls._adapters[name] = adapter
        logger.opt(
            colors=True).debug(f'Succeeded to load adapter "<y>{name}</y>"')

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
            host: Optional[str] = None,
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
