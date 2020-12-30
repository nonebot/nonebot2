from copy import copy
from typing import Any, Dict, Union, Iterable

from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment):
    """
    钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @overrides(BaseMessageSegment)
    def __init__(self, type_: str, data: Dict[str, Any]) -> None:
        super().__init__(type=type_, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self):
        if self.type == "text":
            return str(self.data["content"])
        elif self.type == "markdown":
            return str(self.data["text"])
        return ""

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return Message(other) + self

    @overrides(BaseMessageSegment)
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
    def image(picURL: str) -> "MessageSegment":
        return MessageSegment("image", {"picURL": picURL})

    @staticmethod
    def extension(dict_: dict) -> "MessageSegment":
        """"标记 text 文本的 extension 属性，需要与 text 消息段相加。
        """
        return MessageSegment("extension", dict_)

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
    def actionCardSingleBtn(title: str, text: str, singleTitle: str,
                            singleURL) -> "MessageSegment":
        return MessageSegment(
            "actionCard", {
                "title": title,
                "text": text,
                "singleTitle": singleTitle,
                "singleURL": singleURL
            })

    @staticmethod
    def actionCardMultiBtns(
        title: str,
        text: str,
        btns: list,
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
    def feedCard(links: list) -> "MessageSegment":
        """
        :参数:

            * ``links``: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]
        """
        return MessageSegment("feedCard", {"links": links})

    @staticmethod
    def raw(data) -> "MessageSegment":
        return MessageSegment('raw', data)

    def to_dict(self) -> dict:
        # 让用户可以直接发送原始的消息格式
        if self.type == "raw":
            return copy(self.data)

        # 不属于消息内容，只是作为消息段的辅助
        if self.type in ["at", "extension"]:
            return {self.type: copy(self.data)}

        return {"msgtype": self.type, self.type: copy(self.data)}


class Message(BaseMessage):
    """
    钉钉 协议 Message 适配。
    """

    @staticmethod
    @overrides(BaseMessage)
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
            # text 可以和 text 合并
            if segment.type == "text" and data.get("msgtype") == 'text':
                data.setdefault("text", {})
                data["text"]["content"] = data["text"].setdefault(
                    "content", "") + segment.data["content"]
            else:
                data.update(segment.to_dict())
        return data
