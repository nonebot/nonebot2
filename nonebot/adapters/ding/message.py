from typing import Any, Dict, Union, Iterable

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment):
    """
    钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    def __init__(self, type_: str, data: Dict[str, Any]) -> None:
        super().__init__(type=type_, data=data)

    def __str__(self):
        if self.type == "text":
            return str(self.data["content"])
        elif self.type == "markdown":
            return str(self.data["text"])
        return ""

    def __add__(self, other) -> "Message":
        return Message(self) + other

    def __radd__(self, other) -> "Message":
        return Message(other) + self

    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def atAll() -> "MessageSegment":
        return MessageSegment("at", {"isAtAll": True})

    @staticmethod
    def atMobiles(*mobileNumber: str) -> "MessageSegment":
        return MessageSegment("at", {"atMobiles": list(mobileNumber)})

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"content": text})

    @staticmethod
    def markdown(title: str, text: str) -> "MessageSegment":
        return MessageSegment(
            "markdown",
            {
                "title": title,
                "text": text,
            },
        )

    @staticmethod
    def actionCardSingleBtn(title: str, text: str, btnTitle: str,
                            btnUrl) -> "MessageSegment":
        return MessageSegment(
            "actionCard", {
                "title": title,
                "text": text,
                "singleTitle": btnTitle,
                "singleURL": btnUrl
            })

    @staticmethod
    def actionCardMultiBtns(
        title: str,
        text: str,
        btns: list = [],
        hideAvatar: bool = False,
        btnOrientation: str = '1',
    ) -> "MessageSegment":
        """
        :参数:

            * ``btnOrientation``: 0：按钮竖直排列 1：按钮横向排列

            * ``btns``: [{ "title": title, "actionURL": actionURL }, ...]
        """
        return MessageSegment(
            "actionCard", {
                "title": title,
                "text": text,
                "hideAvatar": "1" if hideAvatar else "0",
                "btnOrientation": btnOrientation,
                "btns": btns
            })

    @staticmethod
    def feedCard(links: list = []) -> "MessageSegment":
        """
        :参数:

            * ``links``: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]
        """
        return MessageSegment("feedCard", {"links": links})

    @staticmethod
    def empty() -> "MessageSegment":
        """不想回复消息到群里"""
        return MessageSegment("empty", {})


class Message(BaseMessage):
    """
    钉钉 协议 Message 适配。
    """

    @classmethod
    def _validate(cls, value):
        return cls(value)

    @staticmethod
    def _construct(msg: Union[str, dict, list]) -> Iterable[MessageSegment]:
        if isinstance(msg, dict):
            yield MessageSegment(msg["type"], msg.get("data") or {})
        elif isinstance(msg, list):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)

    def _produce(self) -> dict:
        data = {}
        for segment in self:
            if segment.type == "text":
                data["msgtype"] = "text"
                data.setdefault("text", {})
                data["text"]["content"] = data["text"].setdefault(
                    "content", "") + segment.data["content"]
            elif segment.type == "markdown":
                data["msgtype"] = "markdown"
                data.setdefault("markdown", {})
                data["markdown"]["text"] = data["markdown"].setdefault(
                    "content", "") + segment.data["content"]
            elif segment.type == "empty":
                data["msgtype"] = "empty"
            elif segment.type == "at" and "atMobiles" in segment.data:
                data.setdefault("at", {})
                data["at"]["atMobiles"] = data["at"].setdefault(
                    "atMobiles", []) + segment.data["atMobiles"]
            elif segment.data:
                data.setdefault(segment.type, {})
                data[segment.type].update(segment.data)
        return data
