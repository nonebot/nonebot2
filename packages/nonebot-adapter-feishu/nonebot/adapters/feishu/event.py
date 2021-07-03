from typing import List, Literal
from pydantic import BaseModel, root_validator

from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides

from .message import Message, MessageSegment


class Event(BaseEvent):
    """
    飞书协议事件。各事件字段参考 `飞书文档`_

    .. _飞书事件列表文档:
        https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list
    """
    app_id: int
    event_type: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.event_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.event_type

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


class MessageBody(BaseModel):
    message_id: str
    root_id: str
    parent_id: str
    create_time: str
    chat_id: str
    chat_type: str
    message_type: str
    content: Message
    mentions: List[Mention]

    plaintext: str

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        content = []
        for piece in values["content"]:
            for segment in piece:
                content.append(
                    MessageSegment(segment["tag"], segment.pop('name', segment)))

        values["content"] = Message(content)
        return values

    @root_validator
    def gen_plaintext(cls, values: dict):
        values["plaintext"] = str(values["content"])
        return values


class MessageEvent(Event):
    sender: Sender
    message: MessageBody

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{super().get_type()}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return (
            f"Message[{super().get_type()}]"
            f" {self.message.message_id} from {self.sender.sender_id.user_id}"
            f" {self.message.content}")

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message.content

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.plaintext

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.sender.sender_id.user_id

    @overrides(Event)
    def get_session_id(self) -> str:
        return self.sender.sender_id.user_id


class PrivateMessageEvent(MessageEvent):
    ...


class GroupMessageEvent(MessageEvent):
    ...


class NoticeEvent(Event):
    ...


class MetaEvent(Event):
    ...
