from collections import namedtuple

from aiocache import cached
from aiocqhttp import Event as CQEvent

from . import NoneBot
from .exceptions import CQHttpError

PRIVATE_FRIEND = 0x0001
PRIVATE_GROUP = 0x0002
PRIVATE_DISCUSS = 0x0004
PRIVATE_OTHER = 0x0008
PRIVATE = 0x000F
DISCUSS = 0x00F0
GROUP_MEMBER = 0x0100
GROUP_ADMIN = 0x0200
GROUP_OWNER = 0x0400
GROUP = 0x0F00
SUPERUSER = 0xF000
EVERYBODY = 0xFFFF

IS_NOBODY = 0x0000
IS_PRIVATE_FRIEND = PRIVATE_FRIEND
IS_PRIVATE_GROUP = PRIVATE_GROUP
IS_PRIVATE_DISCUSS = PRIVATE_DISCUSS
IS_PRIVATE_OTHER = PRIVATE_OTHER
IS_PRIVATE = PRIVATE
IS_DISCUSS = DISCUSS
IS_GROUP_MEMBER = GROUP_MEMBER
IS_GROUP_ADMIN = GROUP_MEMBER | GROUP_ADMIN
IS_GROUP_OWNER = GROUP_ADMIN | GROUP_OWNER
IS_GROUP = GROUP
IS_SUPERUSER = 0xFFFF

_min_event_fields = (
    'self_id',
    'message_type',
    'sub_type',
    'user_id',
    'discuss_id',
    'group_id',
    'anonymous',
)

_MinEvent = namedtuple('MinEvent', _min_event_fields)


async def check_permission(bot: NoneBot, event: CQEvent,
                           permission_required: int) -> bool:
    """
    Check if the event context has the permission required.

    :param bot: NoneBot instance
    :param event: message event
    :param permission_required: permission required
    :return: the context has the permission
    """
    min_event_kwargs = {}
    for field in _min_event_fields:
        if field in event:
            min_event_kwargs[field] = event[field]
        else:
            min_event_kwargs[field] = None
    min_event = _MinEvent(**min_event_kwargs)
    return await _check(bot, min_event, permission_required)


@cached(ttl=2 * 60)  # cache the result for 2 minute
async def _check(bot: NoneBot, min_event: _MinEvent,
                 permission_required: int) -> bool:
    permission = 0
    if min_event.user_id in bot.config.SUPERUSERS:
        permission |= IS_SUPERUSER
    if min_event.message_type == 'private':
        if min_event.sub_type == 'friend':
            permission |= IS_PRIVATE_FRIEND
        elif min_event.sub_type == 'group':
            permission |= IS_PRIVATE_GROUP
        elif min_event.sub_type == 'discuss':
            permission |= IS_PRIVATE_DISCUSS
        elif min_event.sub_type == 'other':
            permission |= IS_PRIVATE_OTHER
    elif min_event.message_type == 'group':
        permission |= IS_GROUP_MEMBER
        if not min_event.anonymous:
            try:
                member_info = await bot.get_group_member_info(
                    self_id=min_event.self_id,
                    group_id=min_event.group_id,
                    user_id=min_event.user_id,
                    no_cache=True
                )
                if member_info:
                    if member_info['role'] == 'owner':
                        permission |= IS_GROUP_OWNER
                    elif member_info['role'] == 'admin':
                        permission |= IS_GROUP_ADMIN
            except CQHttpError:
                pass
    elif min_event.message_type == 'discuss':
        permission |= IS_DISCUSS

    return bool(permission & permission_required)
