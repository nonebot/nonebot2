import json
from enum import Enum
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Literal

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import Message as BaseMessage
from nonebot.log import logger
from nonebot.typing import overrides


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


class PrivateSenderInfo(BaseModel):
    id: int
    nickname: str
    remark: str


class Event(BaseEvent):
    type: str

    @classmethod
    def new(cls, data: Dict[str, Any]) -> "Event":
        type = data['type']

        def all_subclasses(cls: Type[Event]):
            return set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in all_subclasses(c)])

        event_class: Optional[Type[Event]] = None
        for subclass in all_subclasses(cls):
            if subclass.__name__ != type:
                continue
            event_class = subclass

        if event_class is None:
            return Event.parse_obj(data)

        while issubclass(event_class, Event):
            try:
                return event_class.parse_obj(data)
            except ValidationError as e:
                logger.info(
                    f'Failed to parse {data} to class {event_class.__name__}: {e}. '
                    'Fallback to parent class.')
                event_class = event_class.__base__

        raise ValueError(f'Failed to serialize {data}.')

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        from . import message, notice, request
        if isinstance(self, message.MessageEvent):
            return 'message'
        elif isinstance(self, notice.NoticeEvent):
            return 'notice'
        elif isinstance(self, request.RequestEvent):
            return 'request'
        else:
            return 'meta_event'

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

    def normalize_dict(self, **kwargs) -> Dict[str, Any]:
        return json.loads(self.json(**kwargs))
