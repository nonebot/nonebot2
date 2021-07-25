from typing import TYPE_CHECKING

from pydantic import Field
from typing_extensions import Literal

from .base import Event

if TYPE_CHECKING:
    from ..bot import Bot


class RequestEvent(Event):
    """请求事件基类"""
    event_id: int = Field(alias='eventId')
    message: str
    nick: str


class NewFriendRequestEvent(RequestEvent):
    """添加好友申请"""
    from_id: int = Field(alias='fromId')
    group_id: int = Field(0, alias='groupId')

    async def approve(self, bot: "Bot"):
        """
        :说明:

          通过此人的好友申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
        """
        return await bot.api.post('/resp/newFriendRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0,
                                      'message': ''
                                  })

    async def reject(self,
                     bot: "Bot",
                     operate: Literal[1, 2] = 1,
                     message: str = ''):
        """
        :说明:

          拒绝此人的好友申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
          * ``operate: Literal[1, 2]``: 响应的操作类型

            * ``1``: 拒绝添加好友
            * ``2``: 拒绝添加好友并添加黑名单，不再接收该用户的好友申请

          * ``message: str``: 回复的信息
        """
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
    """用户入群申请（Bot需要有管理员权限）"""
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')

    async def approve(self, bot: "Bot"):
        """
        :说明:

          通过此人的加群申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
        """
        return await bot.api.post('/resp/memberJoinRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0,
                                      'message': ''
                                  })

    async def reject(self,
                     bot: "Bot",
                     operate: Literal[1, 2, 3, 4] = 1,
                     message: str = ''):
        """
        :说明:

          拒绝(忽略)此人的加群申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
          * ``operate: Literal[1, 2, 3, 4]``: 响应的操作类型

            * ``1``: 拒绝入群
            * ``2``: 忽略请求
            * ``3``: 拒绝入群并添加黑名单，不再接收该用户的入群申请
            * ``4``: 忽略入群并添加黑名单，不再接收该用户的入群申请

          * ``message: str``: 回复的信息
        """
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
    """Bot被邀请入群申请"""
    from_id: int = Field(alias='fromId')
    group_id: int = Field(alias='groupId')
    group_name: str = Field(alias='groupName')

    async def approve(self, bot: "Bot"):
        """
        :说明:

          通过这份被邀请入群申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
        """
        return await bot.api.post('/resp/botInvitedJoinGroupRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 0,
                                      'message': ''
                                  })

    async def reject(self, bot: "Bot", message: str = ""):
        """
        :说明:

          拒绝这份被邀请入群申请

        :参数:

          * ``bot: Bot``: 当前的 ``Bot`` 对象
          * ``message: str``: 邀请消息
        """
        return await bot.api.post('/resp/botInvitedJoinGroupRequestEvent',
                                  params={
                                      'eventId': self.event_id,
                                      'groupId': self.group_id,
                                      'fromId': self.from_id,
                                      'operate': 1,
                                      'message': message
                                  })
