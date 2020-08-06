#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Tuple, Iterable, Optional

import httpx

from nonebot.event import Event
from nonebot.config import Config
from nonebot.message import handle_event
from nonebot.drivers import BaseWebSocket
from nonebot.exception import ApiNotAvailable
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


def _b2s(b: bool) -> str:
    return str(b).lower()


class Bot(BaseBot):

    def __init__(self,
                 connection_type: str,
                 config: Config,
                 self_id: int,
                 *,
                 websocket: BaseWebSocket = None):
        if connection_type not in ["http", "websocket"]:
            raise ValueError("Unsupported connection type")
        self.type = "coolq"
        self.connection_type = connection_type
        self.config = config
        self.self_id = self_id
        self.websocket = websocket

    async def handle_message(self, message: dict):
        # TODO: convert message into event
        event = Event.from_payload(message)

        if not event:
            return

        if "message" in event.keys():
            event["message"] = Message(event["message"])

        await handle_event(self, event)

    async def call_api(self, api: str, data: dict):
        # TODO: Call API
        if self.type == "websocket":
            pass
        elif self.type == "http":
            api_root = self.config.api_root.get(self.self_id)
            if not api_root:
                raise ApiNotAvailable
            elif not api_root.endswith("/"):
                api_root += "/"

            headers = {}
            if self.config.access_token:
                headers["Authorization"] = "Bearer " + self.config.access_token

            async with httpx.AsyncClient() as client:
                response = await client.post(api_root + api)

            if 200 <= response.status_code < 300:
                # TODO: handle http api response
                return ...
            raise httpx.HTTPError(
                "<HttpFailed {0.status_code} for url: {0.url}>", response)


class MessageSegment(BaseMessageSegment):

    def __str__(self):
        type_ = self.type
        data = self.data.copy()

        # process special types
        if type_ == "at_all":
            type_ = "at"
            data = {"qq": "all"}
        elif type_ == "poke":
            type_ = "shake"
            data.clear()
        elif type_ == "text":
            return escape(data.get("text", ""), escape_comma=False)

        params = ",".join([f"{k}={escape(str(v))}" for k, v in data.items()])
        return f"[CQ:{type_}{',' if params else ''}{params}]"

    @staticmethod
    def anonymous(ignore_failure: bool = False) -> "MessageSegment":
        return MessageSegment("anonymous", {"ignore": _b2s(ignore_failure)})

    @staticmethod
    def at(user_id: int) -> "MessageSegment":
        return MessageSegment("at", {"qq": str(user_id)})

    @staticmethod
    def at_all() -> "MessageSegment":
        return MessageSegment("at_all")

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "group", "id": str(group_id)})

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "qq", "id": str(user_id)})

    @staticmethod
    def face(id_: int) -> "MessageSegment":
        return MessageSegment("face", {"id": str(id_)})

    @staticmethod
    def image(file: str) -> "MessageSegment":
        return MessageSegment("image", {"file": "file"})

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: str = "",
                 content: str = "") -> "MessageSegment":
        return MessageSegment(
            "location", {
                "lat": str(latitude),
                "lon": str(longitude),
                "title": title,
                "content": content
            })

    @staticmethod
    def magic_face(type_: str) -> "MessageSegment":
        if type_ not in ["dice", "rpc"]:
            raise ValueError(
                f"Coolq doesn't support magic face type {type_}. Supported types: dice, rpc."
            )
        return MessageSegment("magic_face", {"type": type_})

    @staticmethod
    def music(type_: str,
              id_: int,
              style: Optional[int] = None) -> "MessageSegment":
        if style is None:
            return MessageSegment("music", {"type": type_, "id": id_})
        else:
            return MessageSegment("music", {
                "type": type_,
                "id": id_,
                "style": style
            })

    @staticmethod
    def music_custom(type_: str,
                     url: str,
                     audio: str,
                     title: str,
                     content: str = "",
                     img_url: str = "") -> "MessageSegment":
        return MessageSegment(
            "music", {
                "type": type_,
                "url": url,
                "audio": audio,
                "title": title,
                "content": content,
                "image": img_url
            })

    @staticmethod
    def poke(type_: str = "Poke") -> "MessageSegment":
        if type_ not in ["Poke"]:
            raise ValueError(
                f"Coolq doesn't support poke type {type_}. Supported types: Poke."
            )
        return MessageSegment("poke", {"type": type_})

    @staticmethod
    def record(file: str, magic: bool = False) -> "MessageSegment":
        return MessageSegment("record", {"file": file, "magic": _b2s(magic)})

    @staticmethod
    def share(url: str = "",
              title: str = "",
              content: str = "",
              img_url: str = "") -> "MessageSegment":
        return MessageSegment("share", {
            "url": url,
            "title": title,
            "content": content,
            "img_url": img_url
        })

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})


class Message(BaseMessage):

    @staticmethod
    def _construct(msg: str) -> Iterable[MessageSegment]:

        def _iter_message() -> Iterable[Tuple[str, str]]:
            text_begin = 0
            for cqcode in re.finditer(
                    r"\[CQ:(?P<type>[a-zA-Z0-9-_.]+)"
                    r"(?P<params>"
                    r"(?:,[a-zA-Z0-9-_.]+=?[^,\]]*)*"
                    r"),?\]", msg):
                yield "text", unescape(msg[text_begin:cqcode.pos +
                                           cqcode.start()])
                text_begin = cqcode.pos + cqcode.end()
                yield cqcode.group("type"), cqcode.group("params").lstrip(",")
            yield "text", unescape(msg[text_begin:])

        for type_, data in _iter_message():
            if type_ == "text":
                if data:
                    # only yield non-empty text segment
                    yield MessageSegment(type_, {"text": data})
            else:
                data = {
                    k: v for k, v in map(
                        lambda x: x.split("=", maxsplit=1),
                        filter(lambda x: x, (
                            x.lstrip() for x in data.split(","))))
                }
                if type_ == "at" and data["qq"] == "all":
                    type_ = "at_all"
                    data.clear()
                elif type_ in ["dice", "rpc"]:
                    type_ = "magic_face"
                    data["type"] = type_
                elif type_ == "shake":
                    type_ = "poke"
                    data["type"] = "Poke"
                yield MessageSegment(type_, data)
