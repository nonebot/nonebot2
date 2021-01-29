from enum import Enum

from pydantic import BaseModel, Field
from typing_extensions import Literal

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import Message as BaseMessage
from nonebot.typing import overrides

from .constants import EVENT_TYPES


class SenderPermission(str, Enum):
    OWNER = 'OWNER'
    ADMINISTRATOR = 'ADMINISTRATOR'
    MEMBER = 'MEMBER'


class SenderGroup(BaseModel):
    id: int
    name: str
    permission: SenderPermission


class SenderInfo(BaseModel):
    id: int
    name: str = Field(alias='memberName')
    permission: SenderPermission
    group: SenderGroup


class Event(BaseEvent):
    type: str

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return EVENT_TYPES.get(self.type, 'meta_event')

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict())

    @overrides(BaseEvent)
    def get_message(self) -> BaseMessage:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False
