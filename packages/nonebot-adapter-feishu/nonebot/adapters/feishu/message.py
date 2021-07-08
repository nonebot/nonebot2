import json
import itertools

from dataclasses import dataclass
from typing import Any, Dict, Tuple, Type, Union, Mapping, Iterable

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment
from nonebot.typing import overrides


class MessageSegment(BaseMessageSegment["Message"]):
    """
    飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    def __str__(self) -> str:
        if self.type == "text" or self.type == "hongbao":
            return str(self.data["text"])

        elif self.type == "image":
            return "[图片]"

        return ""

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
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def post(title: str, content: list) -> "MessageSegment":
        return MessageSegment("post", {"title": title, "content": content})

    @staticmethod
    def image(image_key: str) -> "MessageSegment":
        return MessageSegment("image", {"image_key": image_key})

    @staticmethod
    def interactive(title: str, elements: list) -> "MessageSegment":
        return MessageSegment("interactive", {
            "title": title,
            "elements": elements
        })

    @staticmethod
    def share_chat(chat_id: str) -> "MessageSegment":
        return MessageSegment("share_chat", {"chat_id": chat_id})

    @staticmethod
    def share_user(user_id: str) -> "MessageSegment":
        return MessageSegment("share_user", {"user_id": user_id})

    @staticmethod
    def audio(file_key: str, duration: int) -> "MessageSegment":
        return MessageSegment("audio", {
            "file_key": file_key,
            "duration": duration
        })

    @staticmethod
    def media(file_key: str, image_key: str, file_name: str,
              duration: int) -> "MessageSegment":
        return MessageSegment(
            "media", {
                "file_key": file_key,
                "image_key": image_key,
                "file_name": file_name,
                "duration": duration
            })

    @staticmethod
    def file(file_key: str, file_name: str) -> "MessageSegment":
        return MessageSegment("file", {
            "file_key": file_key,
            "file_name": file_name
        })

    @staticmethod
    def sticker(file_key) -> "MessageSegment":
        return MessageSegment("sticker", {"file_key": file_key})


class Message(BaseMessage[MessageSegment]):
    """
    飞书 协议 Message 适配。
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
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
        elif isinstance(msg, Iterable):
            for seg in msg:
                if isinstance(seg, MessageSegment):
                    yield seg
                else:
                    yield MessageSegment(seg["type"], seg.get("data") or {})

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        return "".join(seg.data["text"] for seg in self if seg.is_text())


@dataclass
class MessageSerializer:
    """
    飞书 协议 Message 序列化器。
    """
    message: Message

    def serialize(self) -> Tuple[str, str]:
        return self.message[0].type, json.dumps(self.message[0].data)


@dataclass
class MessageDeserializer:
    """
    飞书 协议 Message 反序列化器。
    """
    type: str
    data: Dict[str, Any]

    def deserialize(self) -> Message:
        if self.type == "post":
            msg = Message()
            if self.data["title"] != "":
                msg += MessageSegment("text", {'text': self.data["title"]})
            for seg in itertools.chain(*self.data["content"]):
                tag = seg.pop("tag")
                msg += MessageSegment(tag if tag != "img" else "image", seg)
            return msg

        else:
            return Message(MessageSegment(self.type, self.data))
