from aiocqhttp.message import unescape

import none
from none import permissions as perm
from none.command import CommandSession


@none.on_command('echo')
async def echo(session: CommandSession):
    await session.send(session.current_arg)


@none.on_command('say', permission=perm.SUPERUSER)
async def _(session: CommandSession):
    await session.send(unescape(session.current_arg))
