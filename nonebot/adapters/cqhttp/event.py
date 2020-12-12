from nonebot.adapters import BaseEvent
from nonebot.typing import Optional, overrides

from .message import Message


class Event(BaseEvent):
    """
    CQHTTP 协议 Event 适配。继承属性参考 `BaseEvent <./#class-baseevent>`_ 。
    """

    def __init__(self, raw_event: dict):
        if "message" in raw_event:
            raw_event["message"] = Message(raw_event["message"])

        super().__init__(raw_event)

    @property
    @overrides(BaseEvent)
    def id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件/消息 ID
        """
        return self._raw_event.get("message_id") or self._raw_event.get("flag")

    @property
    @overrides(BaseEvent)
    def name(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件名称，由类型与 ``.`` 组合而成
        """
        n = self.type + "." + self.detail_type
        if self.sub_type:
            n += "." + self.sub_type
        return n

    @property
    @overrides(BaseEvent)
    def self_id(self) -> str:
        """
        - 类型: ``str``
        - 说明: 机器人自身 ID
        """
        return str(self._raw_event["self_id"])

    @property
    @overrides(BaseEvent)
    def time(self) -> int:
        """
        - 类型: ``int``
        - 说明: 事件发生时间
        """
        return self._raw_event["time"]

    @property
    @overrides(BaseEvent)
    def type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件类型
        """
        return self._raw_event["post_type"]

    @type.setter
    @overrides(BaseEvent)
    def type(self, value) -> None:
        self._raw_event["post_type"] = value

    @property
    @overrides(BaseEvent)
    def detail_type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件详细类型
        """
        return self._raw_event[f"{self.type}_type"]

    @detail_type.setter
    @overrides(BaseEvent)
    def detail_type(self, value) -> None:
        self._raw_event[f"{self.type}_type"] = value

    @property
    @overrides(BaseEvent)
    def sub_type(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 事件子类型
        """
        return self._raw_event.get("sub_type")

    @sub_type.setter
    @overrides(BaseEvent)
    def sub_type(self, value) -> None:
        self._raw_event["sub_type"] = value

    @property
    @overrides(BaseEvent)
    def user_id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件主体 ID
        """
        return self._raw_event.get("user_id")

    @user_id.setter
    @overrides(BaseEvent)
    def user_id(self, value) -> None:
        self._raw_event["user_id"] = value

    @property
    @overrides(BaseEvent)
    def group_id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件主体群 ID
        """
        return self._raw_event.get("group_id")

    @group_id.setter
    @overrides(BaseEvent)
    def group_id(self, value) -> None:
        self._raw_event["group_id"] = value

    @property
    @overrides(BaseEvent)
    def to_me(self) -> Optional[bool]:
        """
        - 类型: ``Optional[bool]``
        - 说明: 消息是否与机器人相关
        """
        return self._raw_event.get("to_me")

    @to_me.setter
    @overrides(BaseEvent)
    def to_me(self, value) -> None:
        self._raw_event["to_me"] = value

    @property
    @overrides(BaseEvent)
    def message(self) -> Optional["Message"]:
        """
        - 类型: ``Optional[Message]``
        - 说明: 消息内容
        """
        return self._raw_event.get("message")

    @message.setter
    @overrides(BaseEvent)
    def message(self, value) -> None:
        self._raw_event["message"] = value

    @property
    @overrides(BaseEvent)
    def reply(self) -> Optional[dict]:
        """
        - 类型: ``Optional[dict]``
        - 说明: 回复消息详情
        """
        return self._raw_event.get("reply")

    @reply.setter
    @overrides(BaseEvent)
    def reply(self, value) -> None:
        self._raw_event["reply"] = value

    @property
    @overrides(BaseEvent)
    def raw_message(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 原始消息
        """
        return self._raw_event.get("raw_message")

    @raw_message.setter
    @overrides(BaseEvent)
    def raw_message(self, value) -> None:
        self._raw_event["raw_message"] = value

    @property
    @overrides(BaseEvent)
    def plain_text(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 纯文本消息内容
        """
        return self.message and self.message.extract_plain_text()

    @property
    @overrides(BaseEvent)
    def sender(self) -> Optional[dict]:
        """
        - 类型: ``Optional[dict]``
        - 说明: 消息发送者信息
        """
        return self._raw_event.get("sender")

    @sender.setter
    @overrides(BaseEvent)
    def sender(self, value) -> None:
        self._raw_event["sender"] = value
