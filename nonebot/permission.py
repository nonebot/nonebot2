#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from nonebot.utils import run_sync
from nonebot.typing import Bot, Event, Union, NoReturn, Callable, Awaitable, PermissionChecker


class Permission:
    __slots__ = ("checkers",)

    def __init__(self, *checkers: Callable[[Bot, Event],
                                           Awaitable[bool]]) -> None:
        self.checkers = set(checkers)

    async def __call__(self, bot: Bot, event: Event) -> bool:
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *map(lambda c: c(bot, event), self.checkers))
        return any(results)

    def __and__(self, other) -> NoReturn:
        raise RuntimeError("And operation between Permissions is not allowed.")

    def __or__(self, other: Union["Permission",
                                  PermissionChecker]) -> "Permission":
        checkers = self.checkers.copy()
        if isinstance(other, Permission):
            checkers |= other.checkers
        elif asyncio.iscoroutinefunction(other):
            checkers.add(other)
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
NOTICE = Permission(_notice)
REQUEST = Permission(_request)
METAEVENT = Permission(_metaevent)


def USER(*user: int, perm: Permission = Permission()):

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
PRIVATE_FRIEND = Permission(_private_friend)
PRIVATE_GROUP = Permission(_private_group)
PRIVATE_OTHER = Permission(_private_other)


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
GROUP_MEMBER = Permission(_group_member)
GROUP_ADMIN = Permission(_group_admin)
GROUP_OWNER = Permission(_group_owner)


async def _superuser(bot: Bot, event: Event) -> bool:
    return event.type == "message" and event.user_id in bot.config.superusers


SUPERUSER = Permission(_superuser)
EVERYBODY = MESSAGE
