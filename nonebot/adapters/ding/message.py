from nonebot.typing import Any, Dict, Union, Iterable
from nonebot.adapters import BaseMessage, BaseMessageSegment
from .utils import log
from .model import TextMessage


class MessageSegment(BaseMessageSegment):
    """
    钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    def __init__(self, type_: str, msg: Dict[str, Any]) -> None:
        data = {
            "msgtype": type_,
        }
        if msg:
            data.update(msg)
        log("DEBUG", f"data {data}")
        super().__init__(type=type_, data=data)

    @classmethod
    def from_segment(cls, segment: "MessageSegment"):
        return MessageSegment(segment.type, segment.data)

    def __str__(self):
        log("DEBUG", f"__str__: self.type {self.type} data {self.data}")
        if self.type == "text":
            return str(self.data["text"]["content"].strip())
        return ""

    def __add__(self, other) -> "Message":
        if isinstance(other, str):
            if self.type == 'text':
                self.data['text']['content'] += other
                return MessageSegment.from_segment(self)
        return Message(self) + other

    def atMobile(self, mobileNumber):
        self.data.setdefault("at", {})
        self.data["at"].setdefault("atMobiles", [])
        self.data["at"]["atMobiles"].append(mobileNumber)

    def atAll(self, value):
        self.data.setdefault("at", {})
        self.data["at"]["isAtAll"] = value

    @staticmethod
    def text(text_: str) -> "MessageSegment":
        return MessageSegment("text", {"text": {"content": text_.strip()}})

    @staticmethod
    def markdown(title: str, text: str) -> "MessageSegment":
        return MessageSegment("markdown", {
            "markdown": {
                "title": title,
                "text": text,
            },
        })

    @staticmethod
    def actionCardSingleBtn(title: str, text: str, btnTitle: str,
                            btnUrl) -> "MessageSegment":
        return MessageSegment(
            "actionCard", {
                "actionCard": {
                    "title": title,
                    "text": text,
                    "singleTitle": btnTitle,
                    "singleURL": btnUrl
                }
            })

    @staticmethod
    def actionCardSingleMultiBtns(
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
                "actionCard": {
                    "title": title,
                    "text": text,
                    "hideAvatar": "1" if hideAvatar else "0",
                    "btnOrientation": btnOrientation,
                    "btns": btns
                }
            })

    @staticmethod
    def feedCard(links: list = [],) -> "MessageSegment":
        """
        :参数:

            * ``links``: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]
        """
        return MessageSegment("feedCard", {"feedCard": {"links": links}})

    @staticmethod
    def empty() -> "MessageSegment":
        """不想回复消息到群里"""
        return MessageSegment("empty")


class Message(BaseMessage):
    """
    钉钉 协议 Message 适配。
    """

    @staticmethod
    def _construct(
            msg: Union[str, dict, list,
                       TextMessage]) -> Iterable[MessageSegment]:
        if isinstance(msg, dict):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, list):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return
        elif isinstance(msg, TextMessage):
            yield MessageSegment("text", {"text": msg.dict()})
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
