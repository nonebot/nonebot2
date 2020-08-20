#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import asyncio

import httpx

from nonebot.config import Config
from nonebot.message import handle_event
from nonebot.typing import overrides, Driver, WebSocket, NoReturn
from nonebot.typing import Any, Dict, Union, Tuple, Iterable, Optional
from nonebot.exception import NetworkError, ActionFailed, ApiNotAvailable
from nonebot.adapters import BaseBot, BaseEvent, BaseMessage, BaseMessageSegment


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


def _handle_api_result(result: Optional[Dict[str, Any]]) -> Any:
    if isinstance(result, dict):
        if result.get("status") == "failed":
            raise ActionFailed(retcode=result.get("retcode"))
        return result.get("data")


class ResultStore:
    _seq = 1
    _futures: Dict[int, asyncio.Future] = {}

    @classmethod
    def get_seq(cls) -> int:
        s = cls._seq
        cls._seq = (cls._seq + 1) % sys.maxsize
        return s

    @classmethod
    def add_result(cls, result: Dict[str, Any]):
        if isinstance(result.get("echo"), dict) and \
                isinstance(result["echo"].get("seq"), int):
            future = cls._futures.get(result["echo"]["seq"])
            if future:
                future.set_result(result)

    @classmethod
    async def fetch(cls, seq: int, timeout: Optional[float]) -> Dict[str, Any]:
        future = asyncio.get_event_loop().create_future()
        cls._futures[seq] = future
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise NetworkError("WebSocket API call timeout")
        finally:
            del cls._futures[seq]


class Bot(BaseBot):

    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: WebSocket = None):
        if connection_type not in ["http", "websocket"]:
            raise ValueError("Unsupported connection type")

        super().__init__(driver,
                         connection_type,
                         config,
                         self_id,
                         websocket=websocket)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        return "cqhttp"

    @overrides(BaseBot)
    async def handle_message(self, message: dict):
        if not message:
            return

        event = Event(message)

        await handle_event(self, event)

    @overrides(BaseBot)
    async def call_api(self, api: str, **data) -> Union[Any, NoReturn]:
        if "self_id" in data:
            self_id = str(data.pop("self_id"))
            bot = self.driver.bots[self_id]
            return await bot.call_api(api, **data)

        if self.type == "websocket":
            seq = ResultStore.get_seq()
            await self.websocket.send({
                "action": api,
                "params": data,
                "echo": {
                    "seq": seq
                }
            })
            return _handle_api_result(await ResultStore.fetch(
                seq, self.config.api_timeout))

        elif self.type == "http":
            api_root = self.config.api_root.get(self.self_id)
            if not api_root:
                raise ApiNotAvailable
            elif not api_root.endswith("/"):
                api_root += "/"

            headers = {}
            if self.config.access_token is not None:
                headers["Authorization"] = "Bearer " + self.config.access_token

            try:
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.post(
                        api_root + api,
                        json=data,
                        timeout=self.config.api_timeout)

                if 200 <= response.status_code < 300:
                    result = response.json()
                    return _handle_api_result(result)
                raise NetworkError(f"HTTP request received unexpected "
                                   f"status code: {response.status_code}")
            except httpx.InvalidURL:
                raise NetworkError("API root url invalid")
            except httpx.HTTPError:
                raise NetworkError("HTTP request failed")


class Event(BaseEvent):

    def __init__(self, raw_event: dict):
        if "message" in raw_event:
            raw_event["message"] = Message(raw_event["message"])

        super().__init__(raw_event)

    @property
    @overrides(BaseEvent)
    def type(self) -> str:
        return self._raw_event["post_type"]

    @type.setter
    @overrides(BaseEvent)
    def type(self, value) -> None:
        self._raw_event["post_type"] = value

    @property
    @overrides(BaseEvent)
    def detail_type(self) -> str:
        return self._raw_event[f"{self.type}_type"]

    @detail_type.setter
    @overrides(BaseEvent)
    def detail_type(self, value) -> None:
        self._raw_event[f"{self.type}_type"] = value

    @property
    @overrides(BaseEvent)
    def sub_type(self) -> Optional[str]:
        return self._raw_event.get("sub_type")

    @type.setter
    @overrides(BaseEvent)
    def sub_type(self, value) -> None:
        self._raw_event["sub_type"] = value

    @property
    @overrides(BaseEvent)
    def user_id(self) -> Optional[int]:
        return self._raw_event.get("user_id")

    @user_id.setter
    @overrides(BaseEvent)
    def user_id(self, value) -> None:
        self._raw_event["user_id"] = value

    @property
    @overrides(BaseEvent)
    def message(self) -> Optional["Message"]:
        return self._raw_event.get("message")

    @message.setter
    @overrides(BaseEvent)
    def message(self, value) -> None:
        self._raw_event["message"] = value

    @property
    @overrides(BaseEvent)
    def raw_message(self) -> Optional[str]:
        return self._raw_event.get("raw_message")

    @raw_message.setter
    @overrides(BaseEvent)
    def raw_message(self, value) -> None:
        self._raw_event["raw_message"] = value

    @property
    @overrides(BaseEvent)
    def plain_text(self) -> Optional[str]:
        return self.message and self.message.extract_plain_text()

    @property
    @overrides(BaseEvent)
    def sender(self) -> Optional[dict]:
        return self._raw_event.get("sender")

    @sender.setter
    @overrides(BaseEvent)
    def sender(self, value) -> None:
        self._raw_event["sender"] = value


class MessageSegment(BaseMessageSegment):

    @overrides(BaseMessageSegment)
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

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

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
    def forward(id_: str) -> "MessageSegment":
        return MessageSegment("forward", {"id": id_})

    @staticmethod
    def image(file: str) -> "MessageSegment":
        return MessageSegment("image", {"file": file})

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
    def node(id_: int) -> "MessageSegment":
        return MessageSegment("node", {"id": str(id_)})

    @staticmethod
    def node_custom(name: str, uin: int,
                    content: "Message") -> "MessageSegment":
        return MessageSegment("node", {
            "name": name,
            "uin": str(uin),
            "content": str(content)
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
    def replay(id_: int) -> "MessageSegment":
        return MessageSegment("replay", {"id": str(id_)})

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
    @overrides(BaseMessage)
    def _construct(msg: Union[str, dict, list]) -> Iterable[MessageSegment]:
        if isinstance(msg, dict):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, list):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return

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
