from typing import Dict, Any

from aiocqhttp.message import MessageSegment

from . import NoneBot
from .command import handle_command
from .log import logger
from .natural_language import handle_natural_language


async def handle_message(bot: NoneBot, ctx: Dict[str, Any]) -> None:
    _log_message(ctx)

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
        logger.info(f'Message {ctx["message_id"]} is handled as a command')
        return

    handled = await handle_natural_language(bot, ctx)
    if handled:
        logger.info(f'Message {ctx["message_id"]} is handled '
                    f'as natural language')
        return


def _log_message(ctx: Dict[str, Any]) -> None:
    msg_from = f'{ctx["user_id"]}'
    if ctx['message_type'] == 'group':
        msg_from += f'@[群:{ctx["group_id"]}]'
    elif ctx['message_type'] == 'discuss':
        msg_from += f'@[讨论组:{ctx["discuss_id"]}]'
    logger.info(f'Message {ctx["message_id"]} from {msg_from}: '
                f'{ctx["message"]}')
