from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Headers(BaseModel):
    sign: str
    token: str
    # ms
    timestamp: int


class TextMessage(BaseModel):
    content: str


class AtUsersItem(BaseModel):
    dingtalkId: str
    staffId: Optional[str]


class ConversationType(str, Enum):
    private = '1'
    group = '2'


class MessageModel(BaseModel):
    chatbotUserId: str = None
    conversationId: str = None
    conversationType: ConversationType = None
    # ms
    createAt: int = None
    isAdmin: bool = None
    msgId: str = None
    msgtype: str = None
    senderCorpId: str = None
    senderId: str = None
    senderNick: str = None
    sessionWebhook: str = None
    # ms
    sessionWebhookExpiredTime: int = None
    text: Optional[TextMessage] = None


class PrivateMessageModel(MessageModel):
    chatbotCorpId: str = None
    conversationType: ConversationType = ConversationType.private
    senderStaffId: str = None


class GroupMessageModel(MessageModel):
    atUsers: List[AtUsersItem] = None
    conversationType: ConversationType = ConversationType.group
    conversationTitle: str = None
    isInAtList: bool = None
