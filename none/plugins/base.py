import asyncio

from none import on_command, CommandSession, permission as perm
from none.command import kill_current_session
from none.message import unescape, Message, handle_message


@on_command('echo')
async def echo(session: CommandSession):
    await session.send(session.get_optional('message') or session.current_arg)


@on_command('say', permission=perm.SUPERUSER)
async def _(session: CommandSession):
    await session.send(
        unescape(session.get_optional('message') or session.current_arg))


@on_command('switch', privileged=True)
async def _(session: CommandSession):
    kill_current_session(session.bot, session.ctx)

    msg = Message(session.current_arg)
    await session.send(msg)

    ctx = session.ctx.copy()
    ctx['message'] = msg
    asyncio.ensure_future(handle_message(session.bot, ctx))
