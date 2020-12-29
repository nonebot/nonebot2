from enum import Enum
from typing import List, Optional
from typing_extensions import Literal

from pydantic import BaseModel

from nonebot.utils import escape_tag
from nonebot.typing import overrides
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):
    """
    钉钉 协议 Event 适配。各事件字段参考 `钉钉文档`_

    .. _钉钉文档:
        https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p
    """

    chatbotUserId: str

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no type!")

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
    msgtype: str
    text: TextMessage
    msgId: str
    createAt: int  # ms
    conversationType: ConversationType
    conversationId: str
    senderId: str
    senderNick: str
    senderCorpId: str
    sessionWebhook: str
    sessionWebhookExpiredTime: int
    isAdmin: bool

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "message"

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.conversationType.name}"

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return f'Message[{self.msgtype}] {self.msgId} from {self.senderId} "{self.text.content}"'

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        return self.text.content

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        return self.senderId

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        return self.senderId


class PrivateMessageEvent(MessageEvent):
    chatbotCorpId: str
    senderStaffId: Optional[str]
    conversationType: ConversationType = ConversationType.private


class GroupMessageEvent(MessageEvent):
    atUsers: List[AtUsersItem]
    conversationType: ConversationType = ConversationType.group
    conversationTitle: str
    isInAtList: bool

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return self.isInAtList
