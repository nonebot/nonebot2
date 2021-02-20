from typing import Any, Optional

from pydantic import Field

from .base import Event, GroupChatInfo, GroupInfo, UserPermission


class NoticeEvent(Event):
    """通知事件基类"""
    pass


class MuteEvent(NoticeEvent):
    """禁言类事件基类"""
    operator: GroupChatInfo


class BotMuteEvent(MuteEvent):
    """Bot被禁言"""
    pass


class BotUnmuteEvent(MuteEvent):
    """Bot被取消禁言"""
    pass


class MemberMuteEvent(MuteEvent):
    """群成员被禁言事件（该成员不是Bot）"""
    duration_seconds: int = Field(alias='durationSeconds')
    member: GroupChatInfo
    operator: Optional[GroupChatInfo] = None


class MemberUnmuteEvent(MuteEvent):
    """群成员被取消禁言事件（该成员不是Bot）"""
    member: GroupChatInfo
    operator: Optional[GroupChatInfo] = None


class BotJoinGroupEvent(NoticeEvent):
    """Bot加入了一个新群"""
    group: GroupInfo


class BotLeaveEventActive(BotJoinGroupEvent):
    """Bot主动退出一个群"""
    pass


class BotLeaveEventKick(BotJoinGroupEvent):
    """Bot被踢出一个群"""
    pass


class MemberJoinEvent(NoticeEvent):
    """新人入群的事件"""
    member: GroupChatInfo


class MemberLeaveEventKick(MemberJoinEvent):
    """成员被踢出群（该成员不是Bot）"""
    operator: Optional[GroupChatInfo] = None


class MemberLeaveEventQuit(MemberJoinEvent):
    """成员主动离群（该成员不是Bot）"""
    pass


class FriendRecallEvent(NoticeEvent):
    """好友消息撤回"""
    author_id: int = Field(alias='authorId')
    message_id: int = Field(alias='messageId')
    time: int
    operator: int


class GroupRecallEvent(FriendRecallEvent):
    """群消息撤回"""
    group: GroupInfo
    operator: Optional[GroupChatInfo] = None


class GroupStateChangeEvent(NoticeEvent):
    """群变化事件基类"""
    origin: Any
    current: Any
    group: GroupInfo
    operator: Optional[GroupChatInfo] = None


class GroupNameChangeEvent(GroupStateChangeEvent):
    """某个群名改变"""
    origin: str
    current: str


class GroupEntranceAnnouncementChangeEvent(GroupStateChangeEvent):
    """某群入群公告改变"""
    origin: str
    current: str


class GroupMuteAllEvent(GroupStateChangeEvent):
    """全员禁言"""
    origin: bool
    current: bool


class GroupAllowAnonymousChatEvent(GroupStateChangeEvent):
    """匿名聊天"""
    origin: bool
    current: bool


class GroupAllowConfessTalkEvent(GroupStateChangeEvent):
    """坦白说"""
    origin: bool
    current: bool


class GroupAllowMemberInviteEvent(GroupStateChangeEvent):
    """允许群员邀请好友加群"""
    origin: bool
    current: bool


class MemberStateChangeEvent(NoticeEvent):
    """群成员变化事件基类"""
    member: GroupChatInfo
    operator: Optional[GroupChatInfo] = None


class MemberCardChangeEvent(MemberStateChangeEvent):
    """群名片改动"""
    origin: str
    current: str


class MemberSpecialTitleChangeEvent(MemberStateChangeEvent):
    """群头衔改动（只有群主有操作限权）"""
    origin: str
    current: str


class BotGroupPermissionChangeEvent(MemberStateChangeEvent):
    """Bot在群里的权限被改变"""
    origin: UserPermission
    current: UserPermission


class MemberPermissionChangeEvent(MemberStateChangeEvent):
    """成员权限改变的事件（该成员不是Bot）"""
    origin: UserPermission
    current: UserPermission
