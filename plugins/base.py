from aiocqhttp.message import unescape

import none
from none import permissions as perm
from none.helpers import send


@none.on_command('echo')
async def _(bot, ctx, session):
    await send(bot, ctx, session.arg)


@none.on_command('say', permission=perm.SUPERUSER)
async def _(bot, ctx, session):
    await send(bot, ctx, unescape(session.arg))
