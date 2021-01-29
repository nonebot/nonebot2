from typing import List, Dict
from typing_extensions import Literal

EventType = Literal["message", "notice", "request", "meta_event"]

_EVENT_CLASSIFY: Dict[EventType, List[str]] = {
    # XXX Reference: https://github.com/project-mirai/mirai-api-http/blob/v1.9.7/docs/EventType.md
    'meta_event': [
        'BotOnlineEvent', 'BotOfflineEventActive', 'BotOfflineEventForce',
        'BotOfflineEventDropped', 'BotReloginEvent'
    ],
    'notice': [
        'BotGroupPermissionChangeEvent', 'BotMuteEvent', 'BotUnmuteEvent',
        'BotJoinGroupEvent', 'BotLeaveEventActive', 'BotLeaveEventKick',
        'GroupRecallEvent', 'FriendRecallEvent', 'GroupNameChangeEvent',
        'GroupEntranceAnnouncementChangeEvent', 'GroupMuteAllEvent',
        'GroupAllowAnonymousChatEvent', 'GroupAllowConfessTalkEvent',
        'GroupAllowMemberInviteEvent', 'MemberJoinEvent',
        'MemberLeaveEventKick', 'MemberLeaveEventQuit', 'MemberCardChangeEvent',
        'MemberSpecialTitleChangeEvent', 'MemberPermissionChangeEvent',
        'MemberMuteEvent', 'MemberUnmuteEvent'
    ],
    'request': [
        'NewFriendRequestEvent', 'MemberJoinRequestEvent',
        'BotInvitedJoinGroupRequestEvent'
    ],
    'message': ['GroupMessage', 'FriendMessage', 'TempMessage']
}
EVENT_TYPES: Dict[str, EventType] = {}
for event_type, events in _EVENT_CLASSIFY.items():
    _EVENT_TYPES.update({k: event_type for k in events})  # type: ignore
