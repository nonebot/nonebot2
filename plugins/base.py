from aiocqhttp.message import unescape

import none
from none import permissions as perm
from none.command import Session
from none.helpers import send


@none.on_command('echo')
async def echo(bot, ctx, session: Session):
    text = session.require_arg('text')
    await send(bot, session.ctx, text)


@echo.argparser
def _(session: Session):
    session.args['text'] = session.current_arg


@none.on_command('say', permission=perm.SUPERUSER)
async def _(bot, ctx, session: Session):
    await send(bot, session.ctx, unescape(session.current_arg))
