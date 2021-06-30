from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from .message import Message


class Event(BaseEvent):

    def get_type(self) -> str:
        raise NotImplementedError

    def get_event_name(self) -> str:
        raise NotImplementedError

    def get_event_description(self) -> str:
        return str(self.dict())

    def get_message(self) -> Message:
        raise NotImplementedError

    def get_plaintext(self) -> str:
        raise NotImplementedError

    def get_user_id(self) -> str:
        raise NotImplementedError

    def get_session_id(self) -> str:
        raise NotImplementedError

    def is_tome(self) -> bool:
        return False
