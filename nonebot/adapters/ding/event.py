from nonebot.adapters import BaseEvent
from nonebot.typing import Union, Optional

from .message import Message
from .model import MessageModel, ConversationType, TextMessage


class Event(BaseEvent):
    """
    钉钉 协议 Event 适配。继承属性参考 `BaseEvent <./#class-baseevent>`_ 。
    """

    def __init__(self, message: MessageModel):
        super().__init__(message)
        # 其实目前钉钉机器人只能接收到 text 类型的消息
        self._message = Message(getattr(message, message.msgtype or "text"))

    @property
    def raw_event(self) -> MessageModel:
        """原始上报消息"""
        return self._raw_event

    @property
    def id(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 消息 ID
        """
        return self.raw_event.msgId

    @property
    def name(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件名称，由 `type`.`detail_type` 组合而成
        """
        return self.type + "." + self.detail_type

    @property
    def self_id(self) -> str:
        """
        - 类型: ``str``
        - 说明: 机器人自身 ID
        """
        return str(self.raw_event.chatbotUserId)

    @property
    def time(self) -> int:
        """
        - 类型: ``int``
        - 说明: 消息的时间戳，单位 s
        """
        # 单位 ms -> s
        return int(self.raw_event.createAt / 1000)

    @property
    def type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件类型
        """
        return "message"

    @type.setter
    def type(self, value) -> None:
        pass

    @property
    def detail_type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件详细类型
        """
        return self.raw_event.conversationType.name

    @detail_type.setter
    def detail_type(self, value) -> None:
        if value == "private":
            self.raw_event.conversationType = ConversationType.private
        if value == "group":
            self.raw_event.conversationType = ConversationType.group

    @property
    def sub_type(self) -> None:
        """
        - 类型: ``None``
        - 说明: 钉钉适配器无事件子类型
        """
        return None

    @sub_type.setter
    def sub_type(self, value) -> None:
        pass

    @property
    def user_id(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 发送者 ID
        """
        return self.raw_event.senderId

    @user_id.setter
    def user_id(self, value) -> None:
        self.raw_event.senderId = value

    @property
    def group_id(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 事件主体群 ID
        """
        return self.raw_event.conversationId

    @group_id.setter
    def group_id(self, value) -> None:
        self.raw_event.conversationId = value

    @property
    def to_me(self) -> Optional[bool]:
        """
        - 类型: ``Optional[bool]``
        - 说明: 消息是否与机器人相关
        """
        return self.detail_type == "private" or self.raw_event.isInAtList

    @property
    def message(self) -> Optional["Message"]:
        """
        - 类型: ``Optional[Message]``
        - 说明: 消息内容
        """
        return self._message

    @message.setter
    def message(self, value) -> None:
        self._message = value

    @property
    def reply(self) -> None:
        """
        - 类型: ``None``
        - 说明: 回复消息详情
        """
        raise ValueError("暂不支持 reply")

    @property
    def raw_message(self) -> Optional[Union[TextMessage]]:
        """
        - 类型: ``Optional[str]``
        - 说明: 原始消息
        """
        return getattr(self.raw_event, self.raw_event.msgtype)

    @raw_message.setter
    def raw_message(self, value) -> None:
        setattr(self.raw_event, self.raw_event.msgtype, value)

    @property
    def plain_text(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 纯文本消息内容
        """
        return self.message and self.message.extract_plain_text().strip()

    @property
    def sender(self) -> Optional[dict]:
        """
        - 类型: ``Optional[dict]``
        - 说明: 消息发送者信息
        """
        result = {
            # 加密的发送者ID。
            "senderId": self.raw_event.senderId,
            # 发送者昵称。
            "senderNick": self.raw_event.senderNick,
            # 企业内部群有的发送者当前群的企业 corpId。
            "senderCorpId": self.raw_event.senderCorpId,
            # 企业内部群有的发送者在企业内的 userId。
            "senderStaffId": self.raw_event.senderStaffId,
            "role": "admin" if self.raw_event.isAdmin else "member"
        }
        return result

    @sender.setter
    def sender(self, value) -> None:

        def set_wrapper(name):
            if value.get(name):
                setattr(self.raw_event, name, value.get(name))

        set_wrapper("senderId")
        set_wrapper("senderNick")
        set_wrapper("senderCorpId")
        set_wrapper("senderStaffId")
