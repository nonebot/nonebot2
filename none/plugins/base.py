from aiocqhttp.message import unescape

from none import on_command, CommandSession, permissions as perm


@on_command('echo')
async def echo(session: CommandSession):
    await session.send(session.current_arg)


@on_command('say', permission=perm.SUPERUSER)
async def _(session: CommandSession):
    await session.send(unescape(session.current_arg))
