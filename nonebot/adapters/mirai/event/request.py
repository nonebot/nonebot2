from typing import TYPE_CHECKING
from typing_extensions import Literal

from pydantic import Field

from .base import Event

if TYPE_CHECKING:
    from ..bot import MiraiBot as Bot


class RequestEvent(Event):
    event_id: int = Field(alias='eventId')
    message: str
    nick: str


class NewFriendRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(0, alias='groupId')

    async def approve(self, bot: "Bot"):
        return await bot.api.post('/resp/newFriendRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0
                                  })

    async def reject(self,
                     bot: "Bot",
                     operate: Literal[1, 2] = 1,
                     message: str = ''):
        assert operate > 0
        return await bot.api.post('/resp/newFriendRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': operate,
                                      'message': message
                                  })


class MemberJoinRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')

    async def approve(self, bot: "Bot"):
        return await bot.api.post('/resp/memberJoinRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0
                                  })

    async def reject(self,
                     bot: "Bot",
                     operate: Literal[1, 2, 3, 4] = 1,
                     message: str = ''):
        assert operate > 0
        return await bot.api.post('/resp/memberJoinRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': operate,
                                      'message': message
                                  })


class BotInvitedJoinGroupRequestEvent(RequestEvent):
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')

    async def approve(self, bot: "Bot"):
        return await bot.api.post('/resp/botInvitedJoinGroupRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0
                                  })

    async def reject(self, bot: "Bot", message: str = ""):
        return await bot.api.post('/resp/botInvitedJoinGroupRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 1,
                                      'message': message
                                  })
