from enum import Enum
from typing import List, Optional
from typing_extensions import Literal

from pydantic import BaseModel, root_validator

from nonebot.typing import overrides
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    """
    钉钉协议事件。各事件字段参考 `钉钉文档`_

    .. _钉钉文档:
        https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p
    """

    chatbotUserId: str

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        raise ValueError("Event has no name!")

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        raise ValueError("Event has no description!")

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return True


class TextMessage(BaseModel):
    content: str


class AtUsersItem(BaseModel):
    dingtalkId: str
    staffId: Optional[str]


class ConversationType(str, Enum):
    private = "1"
    group = "2"


class MessageEvent(Event):
    """消息事件"""
    msgtype: str
    text: TextMessage
    msgId: str
    createAt: int  # ms
    conversationType: ConversationType
    conversationId: str
    senderId: str
    senderNick: str
    senderCorpId: Optional[str]
    sessionWebhook: str
    sessionWebhookExpiredTime: int
    isAdmin: bool

    message: Message

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        assert "msgtype" in values, "msgtype must be specified"
        # 其实目前钉钉机器人只能接收到 text 类型的消息
        assert values[
            "msgtype"] in values, f"{values['msgtype']} must be specified"
        content = values[values['msgtype']]['content']
        # 如果是被 @，第一个字符将会为空格，移除特殊情况
        if content[0] == ' ':
            content = content[1:]
        values["message"] = content
        return values

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.conversationType.name}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.msgtype}] {self.msgId} from {self.senderId} "{self.text.content}"'

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.text.content

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.senderId

    @overrides(Event)
    def get_session_id(self) -> str:
        return self.senderId


class PrivateMessageEvent(MessageEvent):
    """私聊消息事件"""
    chatbotCorpId: str
    senderStaffId: Optional[str]
    conversationType: ConversationType = ConversationType.private


class GroupMessageEvent(MessageEvent):
    """群消息事件"""
    atUsers: List[AtUsersItem]
    conversationType: ConversationType = ConversationType.group
    conversationTitle: str
    isInAtList: bool

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return self.isInAtList

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.conversationId}_{self.senderId}"
