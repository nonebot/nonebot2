#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from ipaddress import IPv4Address

from nonebot.config import Config


class BaseDriver(object):

    def __init__(self, config: Config):
        raise NotImplementedError

    @property
    def server_app(self):
        raise NotImplementedError

    @property
    def asgi(self):
        raise NotImplementedError

    @property
    def logger(self):
        raise NotImplementedError

    def run(self,
            host: Optional[IPv4Address] = None,
            port: Optional[int] = None,
            *args,
            **kwargs):
        raise NotImplementedError

    async def _handle_http(self):
        raise NotImplementedError

    async def _handle_ws_reverse(self):
        raise NotImplementedError

    async def _handle_http_api(self):
        raise NotImplementedError


class BaseWebSocket(object):

    def __init__(self, websocket):
        self._websocket = websocket

    @property
    def websocket(self):
        return self._websocket

    @property
    def closed(self):
        raise NotImplementedError

    async def accept(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def receive(self) -> dict:
        raise NotImplementedError

    async def send(self, data: dict):
        raise NotImplementedError
