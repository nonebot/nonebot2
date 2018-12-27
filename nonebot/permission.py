from collections import namedtuple

from aiocache import cached

from . import NoneBot
from .exceptions import CQHttpError
from .typing import Context_T

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

_min_context_fields = (
    'self_id',
    'message_type',
    'sub_type',
    'user_id',
    'discuss_id',
    'group_id',
    'anonymous',
)

_MinContext = namedtuple('MinContext', _min_context_fields)


async def check_permission(bot: NoneBot, ctx: Context_T,
                           permission_required: int) -> bool:
    """
    Check if the context has the permission required.

    :param bot: NoneBot instance
    :param ctx: message context
    :param permission_required: permission required
    :return: the context has the permission
    """
    min_ctx_kwargs = {}
    for field in _min_context_fields:
        if field in ctx:
            min_ctx_kwargs[field] = ctx[field]
        else:
            min_ctx_kwargs[field] = None
    min_ctx = _MinContext(**min_ctx_kwargs)
    return await _check(bot, min_ctx, permission_required)


@cached(ttl=2 * 60)  # cache the result for 2 minute
async def _check(bot: NoneBot, min_ctx: _MinContext,
                 permission_required: int) -> bool:
    permission = 0
    if min_ctx.user_id in bot.config.SUPERUSERS:
        permission |= IS_SUPERUSER
    if min_ctx.message_type == 'private':
        if min_ctx.sub_type == 'friend':
            permission |= IS_PRIVATE_FRIEND
        elif min_ctx.sub_type == 'group':
            permission |= IS_PRIVATE_GROUP
        elif min_ctx.sub_type == 'discuss':
            permission |= IS_PRIVATE_DISCUSS
        elif min_ctx.sub_type == 'other':
            permission |= IS_PRIVATE_OTHER
    elif min_ctx.message_type == 'group':
        permission |= IS_GROUP_MEMBER
        if not min_ctx.anonymous:
            try:
                member_info = await bot.get_group_member_info(
                    self_id=min_ctx.self_id,
                    group_id=min_ctx.group_id,
                    user_id=min_ctx.user_id,
                    no_cache=True
                )
                if member_info:
                    if member_info['role'] == 'owner':
                        permission |= IS_GROUP_OWNER
                    elif member_info['role'] == 'admin':
                        permission |= IS_GROUP_ADMIN
            except CQHttpError:
                pass
    elif min_ctx.message_type == 'discuss':
        permission |= IS_DISCUSS

    return bool(permission & permission_required)
