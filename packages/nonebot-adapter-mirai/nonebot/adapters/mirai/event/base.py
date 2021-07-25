import json
from enum import Enum
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Literal

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import Message as BaseMessage
from nonebot.log import logger
from nonebot.typing import overrides


class UserPermission(str, Enum):
    """
    :说明:

      用户权限枚举类

        * ``OWNER``: 群主
        * ``ADMINISTRATOR``: 群管理
        * ``MEMBER``: 普通群成员
    """
    OWNER = 'OWNER'
    ADMINISTRATOR = 'ADMINISTRATOR'
    MEMBER = 'MEMBER'


class GroupInfo(BaseModel):
    id: int
    name: str
    permission: UserPermission


class GroupChatInfo(BaseModel):
    id: int
    name: str = Field(alias='memberName')
    permission: UserPermission
    group: GroupInfo


class PrivateChatInfo(BaseModel):
    id: int
    nickname: str
    remark: str


class Event(BaseEvent):
    """
    mirai-api-http 协议事件，字段与 mirai-api-http 一致。各事件字段参考 `mirai-api-http 事件类型`_

    .. _mirai-api-http 事件类型:
        https://github.com/project-mirai/mirai-api-http/blob/master/docs/EventType.md
    """
    self_id: int
    type: str

    @classmethod
    def new(cls, data: Dict[str, Any]) -> "Event":
        """
        此事件类的工厂函数, 能够通过事件数据选择合适的子类进行序列化
        """
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

        while event_class and issubclass(event_class, Event):
            try:
                return event_class.parse_obj(data)
            except ValidationError as e:
                logger.info(
                    f'Failed to parse {data} to class {event_class.__name__}: '
                    f'{e.errors()!r}. Fallback to parent class.')
                event_class = event_class.__base__  # type: ignore

        raise ValueError(f'Failed to serialize {data}.')

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        from . import message, notice, request, meta
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
        return str(self.normalize_dict())

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
        """
        返回可以被json正常反序列化的结构体
        """
        return json.loads(self.json(**kwargs))
