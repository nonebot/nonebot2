#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx

from nonebot.event import Event
from nonebot.config import Config
from nonebot.message import handle_event
from nonebot.drivers import BaseWebSocket
from nonebot.adapters import BaseBot, BaseMessage, BaseMessageSegment


def escape(s: str, *, escape_comma: bool = True) -> str:
    """
    对字符串进行 CQ 码转义。

    ``escape_comma`` 参数控制是否转义逗号（``,``）。
    """
    s = s.replace("&", "&amp;") \
        .replace("[", "&#91;") \
        .replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


def unescape(s: str) -> str:
    """对字符串进行 CQ 码去转义。"""
    return s.replace("&#44;", ",") \
        .replace("&#91;", "[") \
        .replace("&#93;", "]") \
        .replace("&amp;", "&")


class Bot(BaseBot):

    def __init__(self,
                 type_: str,
                 config: Config,
                 *,
                 websocket: BaseWebSocket = None):
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

    def __str__(self):
        type_ = self.type
        data = self.data.copy()

        # process special types
        if type_ == "text":
            return escape(data.get("text", ""), escape_comma=False)
        elif type_ == "at_all":
            type_ = "at"
            data = {"qq": "all"}

        params = ",".join([f"{k}={escape(str(v))}" for k, v in data.items()])
        return f"[CQ:{type_}{',' if params else ''}{params}]"

    @staticmethod
    def at(user_id: int) -> "MessageSegment":
        return MessageSegment("at", {"qq": str(user_id)})

    @staticmethod
    def at_all() -> "MessageSegment":
        return MessageSegment("at_all")

    @staticmethod
    def dice() -> "MessageSegment":
        return MessageSegment(type_="dice")


class Message(BaseMessage):
    pass
