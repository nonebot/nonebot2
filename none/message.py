import asyncio
from typing import Callable

from aiocqhttp.message import *

from . import NoneBot
from .command import handle_command, SwitchException
from .log import logger
from .natural_language import handle_natural_language
from .typing import Context_T

_message_preprocessors = set()


def message_preprocessor(func: Callable) -> Callable:
    _message_preprocessors.add(func)
    return func


async def handle_message(bot: NoneBot, ctx: Context_T) -> None:
    _log_message(ctx)

    coros = []
    for processor in _message_preprocessors:
        coros.append(processor(bot, ctx))
    if coros:
        await asyncio.wait(coros)

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

    while True:
        try:
            handled = await handle_command(bot, ctx)
            break
        except SwitchException as e:
            # we are sure that there is no session existing now
            ctx['message'] = e.new_ctx_message
            ctx['to_me'] = True
    if handled:
        logger.info(f'Message {ctx["message_id"]} is handled as a command')
        return

    handled = await handle_natural_language(bot, ctx)
    if handled:
        logger.info(f'Message {ctx["message_id"]} is handled '
                    f'as natural language')
        return


def _log_message(ctx: Context_T) -> None:
    msg_from = f'{ctx["user_id"]}'
    if ctx['message_type'] == 'group':
        msg_from += f'@[群:{ctx["group_id"]}]'
    elif ctx['message_type'] == 'discuss':
        msg_from += f'@[讨论组:{ctx["discuss_id"]}]'
    logger.info(f'Message {ctx["message_id"]} from {msg_from}: '
                f'{ctx["message"]}')
