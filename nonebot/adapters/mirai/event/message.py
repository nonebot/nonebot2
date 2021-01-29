from typing import TYPE_CHECKING

from pydantic import Field

from nonebot.typing import overrides

from ..message import MessageChain
from .base import Event, PrivateSenderInfo, SenderInfo


class MessageEvent(Event):
    message_chain: MessageChain = Field(alias='messageChain')
    sender: SenderInfo

    @overrides(Event)
    def get_message(self) -> MessageChain:
        return self.message_chain

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message_chain.__str__()

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(Event)
    def get_session_id(self) -> str:
        return self.get_user_id()


class GroupMessage(MessageEvent):
    pass


class FriendMessage(MessageEvent):
    sender: PrivateSenderInfo


class TempMessage(MessageEvent):
    pass
