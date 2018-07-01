from aiocqhttp.message import unescape

from none import on_command, CommandSession, permission as perm


@on_command('echo', only_to_me=False)
async def echo(session: CommandSession):
    await session.send(session.args.get('message') or session.current_arg)


@on_command('say', permission=perm.SUPERUSER, only_to_me=False)
async def _(session: CommandSession):
    await session.send(
        unescape(session.args.get('message') or session.current_arg))
