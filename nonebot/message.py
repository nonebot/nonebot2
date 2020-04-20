import re
import asyncio
from typing import Callable, Iterable

from aiocqhttp import Event as CQEvent
from aiocqhttp.message import escape, unescape, Message, MessageSegment

from . import NoneBot
from .log import logger
from .natural_language import handle_natural_language
from .command import handle_command, SwitchException
from .plugin import PluginManager

_message_preprocessors = set()


def message_preprocessor(func: Callable) -> Callable:
    _message_preprocessors.add(func)
    return func


class CanceledException(Exception):
    """
    Raised by message_preprocessor indicating that
    the bot should ignore the message
    """

    def __init__(self, reason):
        """
        :param reason: reason to ignore the message
        """
        self.reason = reason


async def handle_message(bot: NoneBot, event: CQEvent) -> None:
    _log_message(event)

    assert isinstance(event.message, Message)
    if not event.message:
        event.message.append(MessageSegment.text(''))  # type: ignore

    raw_to_me = event.get('to_me', False)
    _check_at_me(bot, event)
    _check_calling_me_nickname(bot, event)
    event['to_me'] = raw_to_me or event['to_me']

    coros = []
    plugin_manager = PluginManager()
    for preprocessor in _message_preprocessors:
        coros.append(preprocessor(bot, event, plugin_manager))
    if coros:
        try:
            await asyncio.gather(*coros)
        except CanceledException:
            logger.info(f'Message {event["message_id"]} is ignored')
            return

    while True:
        try:
            handled = await handle_command(bot, event,
                                           plugin_manager.cmd_manager)
            break
        except SwitchException as e:
            # we are sure that there is no session existing now
            event['message'] = e.new_message
            event['to_me'] = True
    if handled:
        logger.info(f'Message {event.message_id} is handled as a command')
        return

    handled = await handle_natural_language(bot, event,
                                            plugin_manager.nlp_manager)
    if handled:
        logger.info(f'Message {event.message_id} is handled '
                    f'as natural language')
        return


def _check_at_me(bot: NoneBot, event: CQEvent) -> None:
    if event.detail_type == 'private':
        event['to_me'] = True
    else:
        # group or discuss
        event['to_me'] = False
        at_me_seg = MessageSegment.at(event.self_id)

        # check the first segment
        first_msg_seg = event.message[0]
        if first_msg_seg == at_me_seg:
            event['to_me'] = True
            del event.message[0]

        if not event['to_me']:
            # check the last segment
            i = -1
            last_msg_seg = event.message[i]
            if last_msg_seg.type == 'text' and \
                    not last_msg_seg.data['text'].strip() and \
                    len(event.message) >= 2:
                i -= 1
                last_msg_seg = event.message[i]

            if last_msg_seg == at_me_seg:
                event['to_me'] = True
                del event.message[i:]

        if not event.message:
            event.message.append(MessageSegment.text(''))


def _check_calling_me_nickname(bot: NoneBot, event: CQEvent) -> None:
    first_msg_seg = event.message[0]
    if first_msg_seg.type != 'text':
        return

    first_text = first_msg_seg.data['text']

    if bot.config.NICKNAME:
        # check if the user is calling me with my nickname
        if isinstance(bot.config.NICKNAME, str) or \
                not isinstance(bot.config.NICKNAME, Iterable):
            nicknames = (bot.config.NICKNAME,)
        else:
            nicknames = filter(lambda n: n, bot.config.NICKNAME)
        nickname_regex = '|'.join(nicknames)
        m = re.search(rf'^({nickname_regex})([\s,，]*|$)', first_text,
                      re.IGNORECASE)
        if m:
            nickname = m.group(1)
            logger.debug(f'User is calling me {nickname}')
            event['to_me'] = True
            first_msg_seg.data['text'] = first_text[m.end():]


def _log_message(event: CQEvent) -> None:
    msg_from = str(event.user_id)
    if event.detail_type == 'group':
        msg_from += f'@[群:{event.group_id}]'
    elif event.detail_type == 'discuss':
        msg_from += f'@[讨论组:{event.discuss_id}]'
    logger.info(f'Self: {event.self_id}, '
                f'Message {event.message_id} from {msg_from}: '
                f'{repr(str(event.message))}')
