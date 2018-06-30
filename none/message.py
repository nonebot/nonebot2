from typing import Dict, Any

from aiocqhttp import CQHttp
from aiocqhttp.message import MessageSegment

from .command import handle_command
from .log import logger
from .helpers import send


async def handle_message(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    # TODO: 支持让插件自己选择是否响应没有 at 的消息
    if ctx['message_type'] != 'private':
        # group or discuss
        ctx['to_me'] = False
        indexes_to_remove = []
        for i, seg in enumerate(ctx['message']):
            if seg == MessageSegment.at(ctx['self_id']):
                ctx['to_me'] = True
                indexes_to_remove.append(i)
        for i in reversed(indexes_to_remove):
            del ctx['message'][i]
        if not ctx['message']:
            ctx['message'].append(MessageSegment.text(''))
    else:
        ctx['to_me'] = True

    handled = await handle_command(bot, ctx)
    if handled:
        logger.debug('Message is handled as a command')
        return
    elif ctx['to_me']:
        await send(bot, ctx, '你在说什么我看不懂诶')

    # TODO: NLP
