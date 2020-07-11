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
                 d: Optional[Dict[str, Any]] = None,
                 *,
                 type_: Optional[str] = None,
                 data: Optional[Dict[str, str]] = None):
        super().__init__()
        if isinstance(d, dict) and d.get('type'):
            self.update(d)
        elif type_:
            self.type = type_
            self.data = data
        else:
            raise ValueError('the "type" field cannot be None or empty')

    def __str__(self):
        raise NotImplementedError


class BaseMessage(list):

    def __init__(self, message: str = None):
        raise NotImplementedError

    def __str__(self):
        return ''.join((str(seg) for seg in self))
