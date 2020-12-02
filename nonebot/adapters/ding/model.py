from typing import List, Optional
from enum import Enum
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
    msgtype: str = None
    text: Optional[TextMessage] = None
    msgId: str
    # ms
    createAt: int = None
    conversationType: ConversationType = None
    conversationId: str = None
    conversationTitle: str = None
    senderId: str = None
    senderNick: str = None
    senderCorpId: str = None
    senderStaffId: str = None
    chatbotUserId: str = None
    chatbotCorpId: str = None
    atUsers: List[AtUsersItem] = None
    sessionWebhook: str = None
    # ms
    sessionWebhookExpiredTime: int = None
    isAdmin: bool = None
    isInAtList: bool = None
