#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx

from nonebot.event import Event
from nonebot.config import Config
from nonebot.adapters import BaseBot, BaseMessage, BaseMessageSegment
from nonebot.message import handle_event


class Bot(BaseBot):

    def __init__(self, type_: str, config: Config, *, websocket=None):
        if type_ not in ["http", "websocket"]:
            raise ValueError("Unsupported connection type")
        self.type = type_
        self.config = config
        self.websocket = websocket

    async def handle_message(self, message: dict):
        # TODO: convert message into event
        event = Event.from_payload(message)

        # TODO: Handle Meta Event
        await handle_event(self, event)

    async def call_api(self, api: str, data: dict):
        if self.type == "websocket":
            pass
        elif self.type == "http":
            pass


class MessageSegment(BaseMessageSegment):
    pass


class Message(BaseMessage):
    pass
