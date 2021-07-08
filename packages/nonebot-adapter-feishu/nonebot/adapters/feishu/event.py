import inspect
import json

from typing import Any, List, Literal, Optional, Type
from pygtrie import StringTrie
from pydantic import BaseModel, root_validator, Field

from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides

from .message import Message, MessageDeserializer


class EventHeader(BaseModel):
    event_id: str
    event_type: str
    create_time: str
    token: str
    app_id: str
    tenant_key: str


class Event(BaseEvent):
    """
    飞书协议事件。各事件字段参考 `飞书文档`_

    .. _飞书事件列表文档:
        https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list
    """
    __event__ = ""
    schema_: str = Field("", alias='schema')
    header: EventHeader
    event: Any

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.header.event_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.header.event_type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict())

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class UserId(BaseModel):
    union_id: str
    user_id: str
    open_id: str


class Sender(BaseModel):
    sender_id: UserId
    sender_type: str
    tenant_key: str


class Mention(BaseModel):
    key: str
    id: UserId
    name: str
    tenant_key: str


class EventMessage(BaseModel):
    message_id: str
    root_id: Optional[str]
    parent_id: Optional[str]
    create_time: str
    chat_id: str
    chat_type: str
    message_type: str
    content: Message
    mentions: Optional[List[Mention]]

    @root_validator(pre=True)
    def parse_message(cls, values: dict):
        values["content"] = MessageDeserializer(
            values["message_type"],
            json.loads(values["content"])).deserialize()
        return values


class GroupEventMessage(EventMessage):
    chat_type: Literal["group"]


class PrivateEventMessage(EventMessage):
    chat_type: Literal["p2p"]


class MessageEventDetail(BaseModel):
    sender: Sender
    message: EventMessage


class GroupMessageEventDetail(MessageEventDetail):
    message: GroupEventMessage


class PrivateMessageEventDetail(MessageEventDetail):
    message: PrivateEventMessage


class MessageEvent(Event):
    __event__ = "im.message.receive_v1"
    event: MessageEventDetail

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.event.message.chat_type}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return (
            f"{self.event.message.message_id} from {self.get_user_id()}"
            f"@[{self.event.message.chat_type}:{self.event.message.chat_id}]"
            f" {self.get_message()}")

    @overrides(Event)
    def get_message(self) -> Message:
        return self.event.message.content

    @overrides(Event)
    def get_plaintext(self) -> str:
        return str(self.get_message())

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.event.sender.sender_id.user_id

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.event.message.chat_type}_{self.event.message.chat_id}_{self.get_user_id()}"


class GroupMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.group"
    event: GroupMessageEventDetail


class PrivateMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.p2p"
    event: PrivateMessageEventDetail


class MessageReader(BaseModel):
    reader_id: UserId
    read_time: str
    tenant_key: str


class MessageReadEventDetail(BaseModel):
    reader: MessageReader
    message_id_list: List[str]


class MessageReadEvent(Event):
    __event__ = "im.message.message_read_v1"
    event: MessageReadEventDetail


class NoticeEvent(Event):
    ...


class MetaEvent(Event):
    ...


_t = StringTrie(separator=".")

# define `model` first to avoid globals changing while `for`
model = None
for model in globals().values():
    if not inspect.isclass(model) or not issubclass(model, Event):
        continue
    _t["." + model.__event__] = model


def get_event_model(event_name) -> List[Type[Event]]:
    """
    :说明:

      根据事件名获取对应 ``Event Model`` 及 ``FallBack Event Model`` 列表

    :返回:

      - ``List[Type[Event]]``
    """
    return [model.value for model in _t.prefixes("." + event_name)][::-1]
