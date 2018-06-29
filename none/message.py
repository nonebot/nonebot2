from typing import Dict, Any

from aiocqhttp import CQHttp
from aiocqhttp.message import MessageSegment

from .command import handle_command
from .log import logger


async def handle_message(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    # TODO: 支持让插件自己选择是否响应没有 at 的消息
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
