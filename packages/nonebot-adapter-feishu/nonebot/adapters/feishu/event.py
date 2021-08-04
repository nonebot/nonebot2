import inspect
import json
from typing import Any, Dict, List, Literal, Optional, Type

from pydantic import BaseModel, Field, root_validator
from pygtrie import StringTrie

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

    .. _飞书文档:
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


class ReplySender(BaseModel):
    id: str
    id_type: str
    sender_type: str
    tenant_key: str


class Mention(BaseModel):
    key: str
    id: UserId
    name: str
    tenant_key: str


class ReplyMention(BaseModel):
    id: str
    id_type: str
    key: str
    name: str
    tenant_key: str


class MessageBody(BaseModel):
    content: str


class Reply(BaseModel):
    message_id: str
    root_id: Optional[str]
    parent_id: Optional[str]
    msg_type: str
    create_time: str
    update_time: str
    deleted: bool
    updated: bool
    chat_id: str
    sender: ReplySender
    body: MessageBody
    mentions: List[ReplyMention]
    upper_message_id: Optional[str]

    class Config:
        extra = "allow"


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
            values["message_type"], json.loads(values["content"]),
            values.get("mentions")).deserialize()
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

    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """
    reply: Optional[Reply]

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice"]:
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
        return self.event.sender.sender_id.open_id

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.event.message.chat_type}_{self.event.message.chat_id}_{self.get_user_id()}"


class GroupMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.group"
    event: GroupMessageEventDetail


class PrivateMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.p2p"
    event: PrivateMessageEventDetail


class NoticeEvent(Event):
    event: Dict[str, Any]

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        raise ValueError("Event has no name!")

    @overrides(Event)
    def get_event_description(self) -> str:
        raise ValueError("Event has no description!")

    @overrides(Event)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(Event)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @overrides(Event)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @overrides(Event)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")


class MessageReader(BaseModel):
    reader_id: UserId
    read_time: str
    tenant_key: str


class MessageReadEventDetail(BaseModel):
    reader: MessageReader
    message_id_list: List[str]


class MessageReadEvent(NoticeEvent):
    __event__ = "im.message.message_read_v1"
    event: MessageReadEventDetail


class GroupDisbandedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class GroupDisbandedEvent(NoticeEvent):
    __event__ = "im.chat.disbanded_v1"
    event: GroupDisbandedEventDetail


class I18nNames(BaseModel):
    zh_cn: str
    en_us: str
    ja_jp: str


class ChatChange(BaseModel):
    avatar: str
    name: str
    description: str
    i18n_names: I18nNames
    add_member_permission: str
    share_card_permission: str
    at_all_permission: str
    edit_permission: str
    membership_approval: str
    join_message_visibility: str
    leave_message_visibility: str
    moderation_permission: str
    owner_id: UserId


class EventModerator(BaseModel):
    tenant_key: str
    user_id: UserId


class ModeratorList(BaseModel):
    added_member_list: EventModerator
    removed_member_list: EventModerator


class GroupConfigUpdatedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    after_change: ChatChange
    before_change: ChatChange
    moderator_list: ModeratorList


class GroupConfigUpdatedEvent(NoticeEvent):
    __event__ = "im.chat.updated_v1"
    event: GroupConfigUpdatedEventDetail


class GroupMemberBotAddedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class GroupMemberBotAddedEvent(NoticeEvent):
    __event__ = "im.chat.member.bot.added_v1"
    event: GroupMemberBotAddedEventDetail


class GroupMemberBotDeletedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class GroupMemberBotDeletedEvent(NoticeEvent):
    __event__ = "im.chat.member.bot.deleted_v1"
    event: GroupMemberBotDeletedEventDetail


class ChatMemberUser(BaseModel):
    name: str
    tenant_key: str
    user_id: UserId


class GroupMemberUserAddedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: List[ChatMemberUser]


class GroupMemberUserAddedEvent(NoticeEvent):
    __event__ = "im.chat.member.user.added_v1"
    event: GroupMemberUserAddedEventDetail


class GroupMemberUserWithdrawnEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: List[ChatMemberUser]


class GroupMemberUserWithdrawnEvent(NoticeEvent):
    __event__ = "im.chat.member.user.withdrawn_v1"
    event: GroupMemberUserWithdrawnEventDetail


class GroupMemberUserDeletedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: List[ChatMemberUser]


class GroupMemberUserDeletedEvent(NoticeEvent):
    __event__ = "im.chat.member.user.deleted_v1"
    event: GroupMemberUserDeletedEventDetail


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
