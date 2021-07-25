from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from nonebot.typing import overrides

from ..message import MessageChain
from .base import Event, GroupChatInfo, PrivateChatInfo


class MessageSource(BaseModel):
    id: int
    time: datetime


class MessageEvent(Event):
    """消息事件基类"""
    message_chain: MessageChain = Field(alias='messageChain')
    source: Optional[MessageSource] = None
    sender: Any

    @overrides(Event)
    def get_message(self) -> MessageChain:
        return self.message_chain

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message_chain.extract_plain_text()

    @overrides(Event)
    def get_user_id(self) -> str:
        raise NotImplementedError

    @overrides(Event)
    def get_session_id(self) -> str:
        raise NotImplementedError


class GroupMessage(MessageEvent):
    """群消息事件"""
    sender: GroupChatInfo
    to_me: bool = False

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f'group_{self.sender.group.id}_' + self.get_user_id()

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return self.to_me


class FriendMessage(MessageEvent):
    """好友消息事件"""
    sender: PrivateChatInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return 'friend_' + self.get_user_id()

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True


class TempMessage(MessageEvent):
    """临时会话消息事件"""
    sender: GroupChatInfo

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f'temp_{self.sender.group.id}_' + self.get_user_id()

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True
