from copy import copy
from typing import Any, Dict, Type, Union, Mapping, Iterable

from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):
    """
    钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return str(self.data["content"])
        elif self.type == "markdown":
            return str(self.data["text"])
        return ""

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def atAll() -> "MessageSegment":
        """@全体"""
        return MessageSegment("at", {"isAtAll": True})

    @staticmethod
    def atMobiles(*mobileNumber: str) -> "MessageSegment":
        """@指定手机号人员"""
        return MessageSegment("at", {"atMobiles": list(mobileNumber)})

    @staticmethod
    def atDingtalkIds(*dingtalkIds: str) -> "MessageSegment":
        """@指定 id，@ 默认会在消息段末尾。
        所以你可以在消息中使用 @{senderId} 占位，发送出去之后 @ 就会出现在占位的位置：
        ```python
        message = MessageSegment.text(f"@{event.senderId}，你好")
        message += MessageSegment.atDingtalkIds(event.senderId)
        ```
        """
        return MessageSegment("at", {"atDingtalkIds": list(dingtalkIds)})

    @staticmethod
    def text(text: str) -> "MessageSegment":
        """发送 ``text`` 类型消息"""
        return MessageSegment("text", {"content": text})

    @staticmethod
    def image(picURL: str) -> "MessageSegment":
        """发送 ``image`` 类型消息"""
        return MessageSegment("image", {"picURL": picURL})

    @staticmethod
    def extension(dict_: dict) -> "MessageSegment":
        """标记 text 文本的 extension 属性，需要与 text 消息段相加。"""
        return MessageSegment("extension", dict_)

    @staticmethod
    def code(code_language: str, code: str) -> "Message":
        """发送 code 消息段"""
        message = MessageSegment.text(code)
        message += MessageSegment.extension({
            "text_type": "code_snippet",
            "code_language": code_language
        })
        return message

    @staticmethod
    def markdown(title: str, text: str) -> "MessageSegment":
        """发送 ``markdown`` 类型消息"""
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
        """发送 ``actionCardSingleBtn`` 类型消息"""
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
        发送 ``actionCardMultiBtn`` 类型消息

        :参数:

            * ``btnOrientation``: 0：按钮竖直排列 1：按钮横向排列
            * ``btns``: ``[{ "title": title, "actionURL": actionURL }, ...]``
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
        发送 ``feedCard`` 类型消息

        :参数:

            * ``links``: ``[{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]``
        """
        return MessageSegment("feedCard", {"links": links})

    @staticmethod
    def raw(data) -> "MessageSegment":
        return MessageSegment('raw', data)

    def to_dict(self) -> Dict[str, Any]:
        # 让用户可以直接发送原始的消息格式
        if self.type == "raw":
            return copy(self.data)

        # 不属于消息内容，只是作为消息段的辅助
        if self.type in ["at", "extension"]:
            return {self.type: copy(self.data)}

        return {"msgtype": self.type, self.type: copy(self.data)}


class Message(BaseMessage[MessageSegment]):
    """
    钉钉 协议 Message 适配。
    """

    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping,
                   Iterable[Mapping]]) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping):
            yield MessageSegment(msg["type"], msg.get("data") or {})
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
        elif isinstance(msg, Iterable):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})

    def _produce(self) -> dict:
        data = {}
        segment: MessageSegment
        for segment in self:
            # text 可以和 text 合并
            if segment.type == "text" and data.get("msgtype") == 'text':
                data.setdefault("text", {})
                data["text"]["content"] = data["text"].setdefault(
                    "content", "") + segment.data["content"]
            else:
                data.update(segment.to_dict())
        return data
