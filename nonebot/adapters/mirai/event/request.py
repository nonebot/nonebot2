from pydantic import Field

from .base import Event


class RequestEvent(Event):
    event_id: int = Field(alias='eventId')
    message: str
    nick: str


class NewFriendRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(0, alias='groupId')


class MemberJoinRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')


class BotInvitedJoinGroupRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')
