from typing import TYPE_CHECKING

from nonebot.permission import Permission

from .event import PrivateMessageEvent, GroupMessageEvent

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event


async def _private(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, PrivateMessageEvent)


async def _private_friend(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, PrivateMessageEvent) and event.sub_type == "friend"


async def _private_group(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, PrivateMessageEvent) and event.sub_type == "group"


async def _private_other(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, PrivateMessageEvent) and event.sub_type == "other"


PRIVATE = Permission(_private)
"""
- **说明**: 匹配任意私聊消息类型事件
"""
PRIVATE_FRIEND = Permission(_private_friend)
"""
- **说明**: 匹配任意好友私聊消息类型事件
"""
PRIVATE_GROUP = Permission(_private_group)
"""
- **说明**: 匹配任意群临时私聊消息类型事件
"""
PRIVATE_OTHER = Permission(_private_other)
"""
- **说明**: 匹配任意其他私聊消息类型事件
"""


async def _group(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessageEvent)


async def _group_member(bot: "Bot", event: "Event") -> bool:
    return isinstance(event,
                      GroupMessageEvent) and event.sender.role == "member"


async def _group_admin(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessageEvent) and event.sender.role == "admin"


async def _group_owner(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessageEvent) and event.sender.role == "owner"


GROUP = Permission(_group)
"""
- **说明**: 匹配任意群聊消息类型事件
"""
GROUP_MEMBER = Permission(_group_member)
"""
- **说明**: 匹配任意群员群聊消息类型事件

\:\:\:warning 警告
该权限通过 event.sender 进行判断且不包含管理员以及群主！
\:\:\:
"""
GROUP_ADMIN = Permission(_group_admin)
"""
- **说明**: 匹配任意群管理员群聊消息类型事件
"""
GROUP_OWNER = Permission(_group_owner)
"""
- **说明**: 匹配任意群主群聊消息类型事件
"""

__all__ = [
    "PRIVATE", "PRIVATE_FRIEND", "PRIVATE_GROUP", "PRIVATE_OTHER", "GROUP",
    "GROUP_MEMBER", "GROUP_ADMIN", "GROUP_OWNER"
]
