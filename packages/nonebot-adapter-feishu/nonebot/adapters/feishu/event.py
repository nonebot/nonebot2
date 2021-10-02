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
    resource_id: Optional[str]
    user_list: Optional[List[dict]]


class Event(BaseEvent):
    """
    飞书协议事件。各事件字段参考 `飞书文档`_

    .. _飞书文档:
        https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list
    """

    __event__ = ""
    schema_: str = Field("", alias="schema")
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
            values["message_type"],
            json.loads(values["content"]),
            values.get("mentions"),
        ).deserialize()
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
            f" {self.get_message()}"
        )

    @overrides(Event)
    def get_message(self) -> Message:
        return self.event.message.content

    @overrides(Event)
    def get_plaintext(self) -> str:
        return str(self.get_message())

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.event.sender.sender_id.open_id

    def get_all_user_id(self) -> UserId:
        return self.event.sender.sender_id

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
        return self.header.event_type

    @overrides(Event)
    def get_event_description(self) -> str:
        return str(self.dict())

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


class AvatarInfo(BaseModel):
    avatar_72: str
    avatar_240: str
    avatar_640: str
    avatar_origin: str


class UserStatus(BaseModel):
    is_frozen: bool
    is_resigned: bool
    is_activated: bool


class UserOrder(BaseModel):
    department_id: str
    user_order: int
    department_order: int


class UserCustomAttrValue(BaseModel):
    text: str
    url: str
    pc_url: str


class UserCustomAttr(BaseModel):
    type: str
    id: str
    value: UserCustomAttrValue


class ContactUser(BaseModel):
    open_id: str
    user_id: str
    name: str
    en_name: str
    email: str
    mobile: str
    gender: int
    avatar: AvatarInfo
    status: UserStatus
    department_ids: Optional[List[str]]
    leader_user_id: str
    city: str
    country: str
    work_station: str
    join_time: int
    employee_no: str
    employee_type: int
    orders: Optional[List[UserOrder]]
    custom_attrs: List[UserCustomAttr]


class OldContactUser(BaseModel):
    department_ids: List[str]
    open_id: str


class ContactUserUpdatedEventDetail(BaseModel):
    object: ContactUser
    old_object: ContactUser


class ContactUserUpdatedEvent(NoticeEvent):
    __event__ = "contact.user.updated_v3"
    event: ContactUserUpdatedEventDetail


class ContactUserDeletedEventDetail(NoticeEvent):
    object: ContactUser
    old_object: OldContactUser


class ContactUserDeletedEvent(NoticeEvent):
    __event__ = "contact.user.deleted_v3"
    event: ContactUserDeletedEventDetail


class ContactUserCreatedEventDetail(BaseModel):
    object: ContactUser


class ContactUserCreatedEvent(NoticeEvent):
    __event__ = "contact.user.created_v3"
    event: ContactUserCreatedEventDetail


class ContactDepartmentStatus(BaseModel):
    is_deleted: bool


class ContactDepartment(BaseModel):
    name: str
    parent_department_id: str
    department_id: str
    open_department_id: str
    leader_user_id: str
    chat_id: str
    order: int
    status: ContactDepartmentStatus


class ContactDepartmentUpdatedEventDetail(BaseModel):
    object: ContactDepartment
    old_object: ContactDepartment


class ContactDepartmentUpdatedEvent(NoticeEvent):
    __event__ = "contact.department.updated_v3"
    event: ContactDepartmentUpdatedEventDetail


class OldContactDepartment(BaseModel):
    status: ContactDepartmentStatus
    open_department_id: str


class ContactDepartmentDeletedEventDetail(NoticeEvent):
    object: ContactDepartment
    old_object: OldContactDepartment


class ContactDepartmentDeletedEvent(NoticeEvent):
    __event__ = "contact.department.deleted_v3"
    event: ContactDepartmentDeletedEventDetail


class ContactDepartmentCreatedEventDetail(BaseModel):
    object: ContactDepartment


class ContactDepartmentCreatedEvent(NoticeEvent):
    __event__ = "contact.department.created_v3"
    event: ContactDepartmentCreatedEventDetail


class CalendarAclScope(BaseModel):
    type: str
    user_id: str


class CalendarAclCreatedEventDetail(BaseModel):
    acl_id: str
    role: str
    scope: CalendarAclScope


class CalendarAclCreatedEvent(NoticeEvent):
    __event__ = "calendar.calendar.acl.created_v4"
    event: CalendarAclCreatedEventDetail


class CalendarAclDeletedEventDetail(BaseModel):
    acl_id: str
    role: str
    scope: CalendarAclScope


class CalendarAclDeletedEvent(NoticeEvent):
    __event__ = "calendar.calendar.acl.deleted_v4"
    event: CalendarAclDeletedEventDetail


class CalendarChangedEvent(NoticeEvent):
    __event__ = "calendar.calendar.changed_v4"
    event: dict


class CalendarEventChangedEventDetail(BaseModel):
    calendar_id: str


class CalendarEventChangedEvent(NoticeEvent):
    __event__ = "calendar.calendar.event.changed_v4"
    event: CalendarEventChangedEventDetail


class DriveFileReadEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id_list: List[UserId]


class DriveFileReadEvent(NoticeEvent):
    __event__ = "drive.file.read_v1"
    event: DriveFileReadEventDetail


class DriveFileTitleUpdatedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFileTitleUpdatedEvent(NoticeEvent):
    __event__ = "drive.file.title_updated_v1"
    event: DriveFileTitleUpdatedEventDetail


class DriveFilePermissionMemberAddedEventDetail(BaseModel):
    chat_list: List[str]
    file_token: str
    file_type: str
    operator_id: UserId
    user_list: List[UserId]


class DriveFilePermissionMemberAddedEvent(NoticeEvent):
    __event__ = "drive.file.permission_member_added_v1"
    event: DriveFilePermissionMemberAddedEventDetail


class DriveFilePermissionMemberRemovedEventDetail(BaseModel):
    chat_list: List[str]
    file_token: str
    file_type: str
    operator_id: UserId
    user_list: List[UserId]


class DriveFilePermissionMemberRemovedEvent(NoticeEvent):
    __event__ = "drive.file.permission_member_removed_v1"
    event: DriveFilePermissionMemberRemovedEventDetail


class DriveFileTrashedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFileTrashedEvent(NoticeEvent):
    __event__ = "drive.file.trashed_v1"
    event: DriveFileTrashedEventDetail


class DriveFileDeletedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFileDeletedEvent(NoticeEvent):
    __event__ = "drive.file.deleted_v1"
    event: DriveFileDeletedEventDetail


class DriveFileEditedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id_list: List[UserId]
    subscriber_id_list: List[UserId]


class DriveFileEditedEvent(NoticeEvent):
    __event__ = "drive.file.edit_v1"
    event: DriveFileEditedEventDetail


class MeetingRoomCreatedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomCreatedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.created_v1"
    event: MeetingRoomCreatedEventDetail


class MeetingRoomUpdatedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomUpdatedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.updated_v1"
    event: MeetingRoomUpdatedEventDetail


class MeetingRoomDeletedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomDeletedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.deleted_v1"
    event: MeetingRoomDeletedEventDetail


class MeetingRoomStatusChangedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomStatusChangedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.status_changed_v1"
    event: MeetingRoomStatusChangedEventDetail


class MeetingUser(BaseModel):
    id: UserId
    user_role: Optional[int]
    user_type: Optional[int]


class Meeting(BaseModel):
    id: str
    topic: str
    meeting_no: str
    start_time: Optional[str]
    end_time: Optional[str]
    host_user: Optional[MeetingUser]
    owner: MeetingUser


class VCMeetingStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.meeting_started_v1"
    event: VCMeetingStartedEventDetail


class VCMeetingEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.meeting_ended_v1"
    event: VCMeetingEndedEventDetail


class VCMeetingJoinedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingJoinedEvent(NoticeEvent):
    __event__ = "vc.meeting.join_meeting_v1"
    event: VCMeetingJoinedEventDetail


class VCMeetingLeftEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser
    leave_reason: int


class VCMeetingLeftEvent(NoticeEvent):
    __event__ = "vc.meeting.leave_meeting_v1"
    event: VCMeetingLeftEventDetail


class VCMeetingRecordingStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingRecordingStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_started_v1"
    event: VCMeetingRecordingStartedEventDetail


class VCMeetingRecordingEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingRecordingEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_ended_v1"
    event: VCMeetingRecordingEndedEventDetail


class VCMeetingRecordingReadyEventDetail(BaseModel):
    meeting: Meeting
    url: str
    duration: str


class VCMeetingRecordingReadyEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_ready_v1"
    event: VCMeetingRecordingReadyEventDetail


class VCMeetingShareStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingShareStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.share_started_v1"
    event: VCMeetingShareStartedEventDetail


class VCMeetingShareEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingShareEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.share_ended_v1"
    event: VCMeetingShareEndedEventDetail


class AttendanceUserFlowCreatedEventDetail(BaseModel):
    bssid: str
    check_time: str
    comment: str
    employee_id: str
    employee_no: str
    is_field: bool
    is_wifi: bool
    latitude: float
    location_name: str
    longitude: float
    photo_urls: Optional[List[str]]
    record_id: str
    ssid: str
    type: int


class AttendanceUserFlowCreatedEvent(NoticeEvent):
    __event__ = "attendance.user_flow.created_v1"
    event: AttendanceUserFlowCreatedEventDetail


class AttendanceUserTaskStatusDiff(BaseModel):
    before_status: str
    before_supplement: str
    current_status: str
    current_supplement: str
    index: int
    work_type: str


class AttendanceUserTaskUpdatedEventDetail(BaseModel):
    date: int
    employee_id: str
    employee_no: str
    group_id: str
    shift_id: str
    status_changes: List[AttendanceUserTaskStatusDiff]
    task_id: str
    time_zone: str


class AttendanceUserTaskUpdatedEvent(NoticeEvent):
    __event__ = "attendance.user_task.updated_v1"
    event: AttendanceUserTaskUpdatedEventDetail


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
