import re
from io import BytesIO
from pathlib import Path
from base64 import b64encode
from typing import Type, Union, Tuple, Mapping, Iterable, Optional

from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment

from .utils import log, escape, unescape, _b2s


class MessageSegment(BaseMessageSegment["Message"]):
    """
    CQHTTP 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()

        # process special types
        if type_ == "text":
            return escape(
                data.get("text", ""),  # type: ignore
                escape_comma=False)

        params = ",".join(
            [f"{k}={escape(str(v))}" for k, v in data.items() if v is not None])
        return f"[CQ:{type_}{',' if params else ''}{params}]"

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + (MessageSegment.text(other) if isinstance(
            other, str) else other)

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return (MessageSegment.text(other)
                if isinstance(other, str) else Message(other)) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def anonymous(ignore_failure: Optional[bool] = None) -> "MessageSegment":
        return MessageSegment("anonymous", {"ignore": _b2s(ignore_failure)})

    @staticmethod
    def at(user_id: Union[int, str]) -> "MessageSegment":
        return MessageSegment("at", {"qq": str(user_id)})

    @staticmethod
    def contact(type_: str, id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": type_, "id": str(id)})

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "group", "id": str(group_id)})

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "qq", "id": str(user_id)})

    @staticmethod
    def dice() -> "MessageSegment":
        return MessageSegment("dice", {})

    @staticmethod
    def face(id_: int) -> "MessageSegment":
        return MessageSegment("face", {"id": str(id_)})

    @staticmethod
    def forward(id_: str) -> "MessageSegment":
        log("WARNING", "Forward Message only can be received!")
        return MessageSegment("forward", {"id": id_})

    @staticmethod
    def image(file: Union[str, bytes, BytesIO, Path],
              type_: Optional[str] = None,
              cache: bool = True,
              proxy: bool = True,
              timeout: Optional[int] = None) -> "MessageSegment":
        if isinstance(file, BytesIO):
            file = file.read()
        if isinstance(file, bytes):
            file = f"base64://{b64encode(file).decode()}"
        elif isinstance(file, Path):
            file = f"file:///{file.resolve()}"
        return MessageSegment(
            "image", {
                "file": file,
                "type": type_,
                "cache": _b2s(cache),
                "proxy": _b2s(proxy),
                "timeout": timeout
            })

    @staticmethod
    def json(data: str) -> "MessageSegment":
        return MessageSegment("json", {"data": data})

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: Optional[str] = None,
                 content: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "location", {
                "lat": str(latitude),
                "lon": str(longitude),
                "title": title,
                "content": content
            })

    @staticmethod
    def music(type_: str, id_: int) -> "MessageSegment":
        return MessageSegment("music", {"type": type_, "id": id_})

    @staticmethod
    def music_custom(url: str,
                     audio: str,
                     title: str,
                     content: Optional[str] = None,
                     img_url: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "music", {
                "type": "custom",
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
    def node_custom(user_id: int, nickname: str,
                    content: Union[str, "Message"]) -> "MessageSegment":
        return MessageSegment("node", {
            "user_id": str(user_id),
            "nickname": nickname,
            "content": content
        })

    @staticmethod
    def poke(type_: str, id_: str) -> "MessageSegment":
        return MessageSegment("poke", {"type": type_, "id": id_})

    @staticmethod
    def record(file: Union[str, bytes, BytesIO, Path],
               magic: Optional[bool] = None,
               cache: Optional[bool] = None,
               proxy: Optional[bool] = None,
               timeout: Optional[int] = None) -> "MessageSegment":
        if isinstance(file, BytesIO):
            file = file.read()
        if isinstance(file, bytes):
            file = f"base64://{b64encode(file).decode()}"
        elif isinstance(file, Path):
            file = f"file:///{file.resolve()}"
        return MessageSegment(
            "record", {
                "file": file,
                "magic": _b2s(magic),
                "cache": _b2s(cache),
                "proxy": _b2s(proxy),
                "timeout": timeout
            })

    @staticmethod
    def reply(id_: int) -> "MessageSegment":
        return MessageSegment("reply", {"id": str(id_)})

    @staticmethod
    def rps() -> "MessageSegment":
        return MessageSegment("rps", {})

    @staticmethod
    def shake() -> "MessageSegment":
        return MessageSegment("shake", {})

    @staticmethod
    def share(url: str = "",
              title: str = "",
              content: Optional[str] = None,
              image: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("share", {
            "url": url,
            "title": title,
            "content": content,
            "image": image
        })

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def video(file: Union[str, bytes, BytesIO, Path],
              cache: Optional[bool] = None,
              proxy: Optional[bool] = None,
              timeout: Optional[int] = None) -> "MessageSegment":
        if isinstance(file, BytesIO):
            file = file.read()
        if isinstance(file, bytes):
            file = f"base64://{b64encode(file).decode()}"
        elif isinstance(file, Path):
            file = f"file:///{file.resolve()}"
        return MessageSegment(
            "video", {
                "file": file,
                "cache": _b2s(cache),
                "proxy": _b2s(proxy),
                "timeout": timeout
            })

    @staticmethod
    def xml(data: str) -> "MessageSegment":
        return MessageSegment("xml", {"data": data})


class Message(BaseMessage[MessageSegment]):
    """
    CQHTTP 协议 Message 适配。
    """

    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @overrides(BaseMessage)
    def __add__(self, other: Union[str, Mapping,
                                   Iterable[Mapping]]) -> "Message":
        return super(Message, self).__add__(
            MessageSegment.text(other) if isinstance(other, str) else other)

    @overrides(BaseMessage)
    def __radd__(self, other: Union[str, Mapping,
                                    Iterable[Mapping]]) -> "Message":
        return super(Message, self).__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other)

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping,
                   Iterable[Mapping]]) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, Iterable) and not isinstance(msg, str):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return
        elif isinstance(msg, str):

            def _iter_message(msg: str) -> Iterable[Tuple[str, str]]:
                text_begin = 0
                for cqcode in re.finditer(
                        r"\[CQ:(?P<type>[a-zA-Z0-9-_.]+)"
                        r"(?P<params>"
                        r"(?:,[a-zA-Z0-9-_.]+=[^,\]]+)*"
                        r"),?\]", msg):
                    yield "text", msg[text_begin:cqcode.pos + cqcode.start()]
                    text_begin = cqcode.pos + cqcode.end()
                    yield cqcode.group("type"), cqcode.group("params").lstrip(
                        ",")
                yield "text", msg[text_begin:]

            for type_, data in _iter_message(msg):
                if type_ == "text":
                    if data:
                        # only yield non-empty text segment
                        yield MessageSegment(type_, {"text": unescape(data)})
                else:
                    data = {
                        k: unescape(v) for k, v in map(
                            lambda x: x.split("=", maxsplit=1),
                            filter(lambda x: x, (
                                x.lstrip() for x in data.split(","))))
                    }
                    yield MessageSegment(type_, data)

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        return "".join(seg.data["text"] for seg in self if seg.is_text())
