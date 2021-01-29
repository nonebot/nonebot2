from typing import Optional, Any

from pydantic import Field

from .base import Event, SenderGroup, SenderInfo, SenderPermission


class BaseNoticeEvent(Event):
    pass


class BaseMuteEvent(BaseNoticeEvent):
    operator: SenderInfo


class BotMuteEvent(BaseMuteEvent):
    pass


class BotUnmuteEvent(BaseMuteEvent):
    pass


class MemberMuteEvent(BaseMuteEvent):
    duration_seconds: int = Field(alias='durationSeconds')
    member: SenderInfo
    operator: Optional[SenderInfo] = None


class MemberUnmuteEvent(BaseMuteEvent):
    member: SenderInfo
    operator: Optional[SenderInfo] = None


class BotJoinGroupEvent(BaseNoticeEvent):
    group: SenderGroup


class BotLeaveEventActive(BotJoinGroupEvent):
    pass


class BotLeaveEventKick(BotJoinGroupEvent):
    pass


class MemberJoinEvent(BaseNoticeEvent):
    member: SenderInfo


class MemberLeaveEventQuit(MemberJoinEvent):
    pass


class MemberLeaveEventKick(MemberJoinEvent):
    operator: Optional[SenderInfo] = None


class FriendRecallEvent(BaseNoticeEvent):
    author_id: int = Field(alias='authorId')
    message_id: int = Field(alias='messageId')
    time: int
    operator: int


class GroupRecallEvent(FriendRecallEvent):
    group: SenderGroup
    operator: Optional[SenderInfo] = None


class GroupStateChangeEvent(BaseNoticeEvent):
    origin: Any
    current: Any
    group: SenderGroup
    operator: Optional[SenderInfo] = None


class GroupNameChangeEvent(GroupStateChangeEvent):
    origin: str
    current: str


class GroupEntranceAnnouncementChangeEvent(GroupStateChangeEvent):
    origin: str
    current: str


class GroupMuteAllEvent(GroupStateChangeEvent):
    origin: bool
    current: bool


class GroupAllowAnonymousChatEvent(GroupStateChangeEvent):
    origin: bool
    current: bool


class GroupAllowConfessTalkEvent(GroupStateChangeEvent):
    origin: bool
    current: bool


class GroupAllowMemberInviteEvent(GroupStateChangeEvent):
    origin: bool
    current: bool


class MemberStateChangeEvent(BaseNoticeEvent):
    member: SenderInfo
    operator: Optional[SenderInfo] = None


class MemberCardChangeEvent(MemberStateChangeEvent):
    origin: str
    current: str


class MemberSpecialTitleChangeEvent(MemberStateChangeEvent):
    origin: str
    current: str


class BotGroupPermissionChangeEvent(MemberStateChangeEvent):
    origin: SenderPermission
    current: SenderPermission


class MemberPermissionChangeEvent(MemberStateChangeEvent):
    origin: SenderPermission
    current: SenderPermission
