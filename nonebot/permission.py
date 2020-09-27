#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
权限
====

每个 ``Matcher`` 拥有一个 ``Permission`` ，其中是 **异步** ``PermissionChecker`` 的集合，只要有一个 ``PermissionChecker`` 检查结果为 ``True`` 时就会继续运行。

\:\:\:tip 提示
``PermissionChecker`` 既可以是 async function 也可以是 sync function
\:\:\:
"""

import asyncio

from nonebot.utils import run_sync
from nonebot.typing import Bot, Event, Union, NoReturn, Optional, Callable, Awaitable, PermissionChecker


class Permission:
    __slots__ = ("checkers",)

    def __init__(self, *checkers: Callable[[Bot, Event],
                                           Awaitable[bool]]) -> None:
        """
        :参数:
          * ``*checkers: Callable[[Bot, Event], Awaitable[bool]]``: **异步** PermissionChecker
        """
        self.checkers = set(checkers)
        """
        :说明:
          存储 ``PermissionChecker``
        :类型:
          * ``Set[Callable[[Bot, Event], Awaitable[bool]]]``
        """

    async def __call__(self, bot: Bot, event: Event) -> bool:
        """
        :说明:
          检查是否满足某个权限
        :参数:
          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
        :返回:
          - ``bool``
        """
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *map(lambda c: c(bot, event), self.checkers))
        return any(results)

    def __and__(self, other) -> NoReturn:
        raise RuntimeError("And operation between Permissions is not allowed.")

    def __or__(
        self, other: Optional[Union["Permission",
                                    PermissionChecker]]) -> "Permission":
        checkers = self.checkers.copy()
        if other is None:
            return self
        elif isinstance(other, Permission):
            checkers |= other.checkers
        elif asyncio.iscoroutinefunction(other):
            checkers.add(other)  # type: ignore
        else:
            checkers.add(run_sync(other))
        return Permission(*checkers)


async def _message(bot: Bot, event: Event) -> bool:
    return event.type == "message"


async def _notice(bot: Bot, event: Event) -> bool:
    return event.type == "notice"


async def _request(bot: Bot, event: Event) -> bool:
    return event.type == "request"


async def _metaevent(bot: Bot, event: Event) -> bool:
    return event.type == "meta_event"


MESSAGE = Permission(_message)
"""
- **说明**: 匹配任意 ``message`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 message type 的 Matcher。
"""
NOTICE = Permission(_notice)
"""
- **说明**: 匹配任意 ``notice`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 notice type 的 Matcher。
"""
REQUEST = Permission(_request)
"""
- **说明**: 匹配任意 ``request`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 request type 的 Matcher。
"""
METAEVENT = Permission(_metaevent)
"""
- **说明**: 匹配任意 ``meta_event`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 meta_event type 的 Matcher。
"""


def USER(*user: int, perm: Permission = Permission()):
    """
    :说明:
      在白名单内且满足 perm
    :参数:
      * ``*user: int``: 白名单
      * ``perm: Permission``: 需要同时满足的权限
    """

    async def _user(bot: Bot, event: Event) -> bool:
        return event.type == "message" and event.user_id in user and await perm(
            bot, event)

    return Permission(_user)


async def _private(bot: Bot, event: Event) -> bool:
    return event.type == "message" and event.detail_type == "private"


async def _private_friend(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "private" and
            event.sub_type == "friend")


async def _private_group(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "private" and
            event.sub_type == "group")


async def _private_other(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "private" and
            event.sub_type == "other")


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


async def _group(bot: Bot, event: Event) -> bool:
    return event.type == "message" and event.detail_type == "group"


async def _group_member(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "group" and
            event.sender.get("role") == "member")


async def _group_admin(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "group" and
            event.sender.get("role") == "admin")


async def _group_owner(bot: Bot, event: Event) -> bool:
    return (event.type == "message" and event.detail_type == "group" and
            event.sender.get("role") == "owner")


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


async def _superuser(bot: Bot, event: Event) -> bool:
    return event.type == "message" and event.user_id in bot.config.superusers


SUPERUSER = Permission(_superuser)
"""
- **说明**: 匹配任意超级用户消息类型事件
"""
EVERYBODY = MESSAGE
"""
- **说明**: 匹配任意消息类型事件
"""
