from typing import Dict, Any

from aiocqhttp import CQHttp
from aiocqhttp.message import MessageSegment

from . import logger
from .command import on_command, handle_command

__all__ = [
    'on_command',
]


async def handle_message(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    if ctx['message_type'] != 'private':
        # group or discuss
        first_message_seg = ctx['message'][0]
        if first_message_seg != MessageSegment.at(ctx['self_id']):
            return
        del ctx['message'][0]
        if not ctx['message']:
            ctx['message'].append(MessageSegment.text(''))

    handled = await handle_command(bot, ctx)
    if handled:
        logger.debug('Message is handled as a command')
        return
    else:
        await bot.send(ctx, '你在说什么我看不懂诶')


async def handle_notice(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    pass


async def handle_request(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    pass
