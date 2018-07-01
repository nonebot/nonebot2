from typing import Dict, Any

from aiocqhttp import CQHttp
from aiocqhttp.message import MessageSegment

from .command import handle_command
from .natural_language import handle_natural_language
from .log import logger


async def handle_message(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    if ctx['message_type'] != 'private':
        # group or discuss
        ctx['to_me'] = False
        first_message_seg = ctx['message'][0]
        if first_message_seg == MessageSegment.at(ctx['self_id']):
            ctx['to_me'] = True
            del ctx['message'][0]
        if not ctx['message']:
            ctx['message'].append(MessageSegment.text(''))
    else:
        ctx['to_me'] = True

    handled = await handle_command(bot, ctx)
    if handled:
        logger.debug('Message is handled as command')
        return

    handled = await handle_natural_language(bot, ctx)
    if handled:
        logger.debug('Message is handled as natural language')
        return
