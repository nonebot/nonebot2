from typing import Any, Dict, Union, Tuple, Mapping, Iterable, Optional

from nonebot.typing import overrides
from nonebot.adapters import (
    Message as BaseMessage,
    MessageSegment as BaseMessageSegment,
)


class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> "Message":
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return self.data.get("text")

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> "MessageSegment":
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping, Iterable[Mapping]]
    ) -> Iterable[MessageSegment]:
        # TODO
        if isinstance(msg, Mapping):
            for key in msg:
                if key == "text":
                    yield MessageSegment(
                        key, {key: msg[key], "entities": msg.get("entities")}
                    )
                elif key in [
                    "animation",
                    "audio",
                    "document",
                    "photo",
                    "video",
                    "voice",
                ]:
                    yield MessageSegment(
                        key,
                        {
                            key: msg[key],
                            "caption": msg.get("caption"),
                            "caption_entities": msg.get("caption_entities"),
                        },
                    )
                elif key in ["sticker", "video_note", "dice", "poll"]:
                    yield MessageSegment(key, {key: msg[key]})
            return
        elif isinstance(msg, Iterable) and not isinstance(msg, str):
            for seg in msg:
                yield MessageSegment(seg.type, seg.data or {})
            return
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
