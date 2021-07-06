import itertools

from dataclasses import dataclass
import json
from typing import Any, Dict, List, Tuple, Type, Union, Mapping, Iterable

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
    def file(file_key: str, file_name: str) -> "MessageSegment":
        return MessageSegment("file", {
            "file_key": file_key,
            "file_name": file_name
        })

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
    def sticker(file_key) -> "MessageSegment":
        return MessageSegment("sticker", {"file_key": file_key})

    @staticmethod
    def interactive(title: str, elements: list) -> "MessageSegment":
        return MessageSegment("interactive", {
            "title": title,
            "elements": elements
        })

    @staticmethod
    def hongbao(text: str) -> "MessageSegment":
        return MessageSegment("hongbao", {"text": text})

    @staticmethod
    def share_calendar_event(summary: str, start_time: str,
                             end_time: str) -> "MessageSegment":
        return MessageSegment("share_calendar_event", {
            "summary": summary,
            "start_time": start_time,
            "end_time": end_time
        })

    @staticmethod
    def share_chat(chat_id: str) -> "MessageSegment":
        return MessageSegment("share_chat", {"chat_id": chat_id})

    @staticmethod
    def share_user(user_id: str) -> "MessageSegment":
        return MessageSegment("share_user", {"user_id": user_id})

    @staticmethod
    def system(template: str, from_user: list,
               to_chatters: list) -> "MessageSegment":
        return MessageSegment(
            "system", {
                "template": template,
                "from_user": from_user,
                "to_chatters": to_chatters
            })

    @staticmethod
    def location(name: str, longitude: str, latitude: str) -> "MessageSegment":
        return MessageSegment("location", {
            "name": name,
            "longitude": longitude,
            "latitude": latitude
        })

    @staticmethod
    def video_chat(topic: str, start_time: str) -> "MessageSegment":
        return MessageSegment("video_chat", {
            "topic": topic,
            "start_time": start_time,
        })


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

    def _produce(self) -> dict:
        raise NotImplementedError

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        return "".join(seg.data["text"] for seg in self if seg.is_text())


@dataclass
class MessageSerializer:
    """
    飞书 协议 Message 序列化器。
    """
    message: Message

    def serialize(self):
        for segment in self.message:
            if segment.type == "post":
                raise NotImplementedError
            else:
                return json.dumps(segment.data)


@dataclass
class MessageDeserializer:
    """
    飞书 协议 Message 反序列化器。
    """
    data: Dict[str, Any]
    type: str

    def deserialize(self):
        print(self.type, self.data)
        if self.type == "post":
            return self._parse_rich_text(self.data)
        else:
            return Message(MessageSegment(self.type, self.data))

    def _parse_rich_text(self, message_data: Dict[str,
                                                  Any]) -> List[MessageSegment]:

        def _iter_message(
            message_data: Dict[str,
                               Any]) -> Iterable[Tuple[str, Dict[str, Any]]]:
            content: dict = message_data.get("content", {})
            if content:
                for element in list(itertools.chain(*content)):
                    tag = element.get("tag")
                    yield tag, element

        temp = Message()
        for type_, data in _iter_message(message_data):
            temp += MessageSegment(type_, data)

        return temp
