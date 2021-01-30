from typing import Any

from pydantic import Field

from nonebot.typing import overrides

from ..message import MessageChain
from .base import Event, PrivateSenderInfo, SenderInfo


class MessageEvent(Event):
    message_chain: MessageChain = Field(alias='messageChain')
    sender: Any

    @overrides(Event)
    def get_message(self) -> MessageChain:
        return self.message_chain

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message_chain.__str__()

    @overrides(Event)
    def get_user_id(self) -> str:
        raise NotImplementedError

    @overrides(Event)
    def get_session_id(self) -> str:
        raise NotImplementedError


class GroupMessage(MessageEvent):
    sender: SenderInfo

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f'group_{self.sender.group.id}_' + self.get_user_id()


class FriendMessage(MessageEvent):
    sender: PrivateSenderInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides
    def get_session_id(self) -> str:
        return 'friend_' + self.get_user_id()


class TempMessage(MessageEvent):
    sender: SenderInfo

    @overrides
    def get_session_id(self) -> str:
        return f'temp_{self.sender.group.id}_' + self.get_user_id()
