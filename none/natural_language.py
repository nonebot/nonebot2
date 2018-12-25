import asyncio
import re
from typing import Iterable, Optional, Callable, Union, NamedTuple

from . import NoneBot, permission as perm
from .command import call_command
from .log import logger
from .message import Message
from .session import BaseSession
from .typing import Context_T, CommandName_T, CommandArgs_T

_nl_processors = set()


class NLProcessor:
    __slots__ = ('func', 'keywords', 'permission',
                 'only_to_me', 'only_short_message',
                 'allow_empty_message')

    def __init__(self, *, func: Callable, keywords: Optional[Iterable],
                 permission: int, only_to_me: bool, only_short_message: bool,
                 allow_empty_message: bool):
        self.func = func
        self.keywords = keywords
        self.permission = permission
        self.only_to_me = only_to_me
        self.only_short_message = only_short_message
        self.allow_empty_message = allow_empty_message


def on_natural_language(keywords: Union[Optional[Iterable], Callable] = None,
                        *, permission: int = perm.EVERYBODY,
                        only_to_me: bool = True,
                        only_short_message: bool = True,
                        allow_empty_message: bool = False) -> Callable:
    """
    Decorator to register a function as a natural language processor.

    :param keywords: keywords to respond to, if None, respond to all messages
    :param permission: permission required by the processor
    :param only_to_me: only handle messages to me
    :param only_short_message: only handle short messages
    :param allow_empty_message: handle empty messages
    """

    def deco(func: Callable) -> Callable:
        nl_processor = NLProcessor(func=func, keywords=keywords,
                                   permission=permission,
                                   only_to_me=only_to_me,
                                   only_short_message=only_short_message,
                                   allow_empty_message=allow_empty_message)
        _nl_processors.add(nl_processor)
        return func

    if isinstance(keywords, Callable):
        # here "keywords" is the function to be decorated
        return on_natural_language()(keywords)
    else:
        return deco


class NLPSession(BaseSession):
    __slots__ = ('msg', 'msg_text', 'msg_images')

    def __init__(self, bot: NoneBot, ctx: Context_T, msg: str):
        super().__init__(bot, ctx)
        self.msg = msg
        tmp_msg = Message(msg)
        self.msg_text = tmp_msg.extract_plain_text()
        self.msg_images = [s.data['url'] for s in tmp_msg
                           if s.type == 'image' and 'url' in s.data]


class NLPResult(NamedTuple):
    confidence: float
    cmd_name: Union[str, CommandName_T]
    cmd_args: Optional[CommandArgs_T] = None


async def handle_natural_language(bot: NoneBot, ctx: Context_T) -> bool:
    """
    Handle a message as natural language.

    This function is typically called by "handle_message".

    :param bot: NoneBot instance
    :param ctx: message context
    :return: the message is handled as natural language
    """
    msg = str(ctx['message'])
    if bot.config.NICKNAME:
        # check if the user is calling me with my nickname
        if isinstance(bot.config.NICKNAME, str) or \
                not isinstance(bot.config.NICKNAME, Iterable):
            nicknames = (bot.config.NICKNAME,)
        else:
            nicknames = filter(lambda n: n, bot.config.NICKNAME)
        nickname_regex = '|'.join(nicknames)
        m = re.search(rf'^({nickname_regex})([\s,，]|$)', msg, re.IGNORECASE)
        if m:
            nickname = m.group(1)
            logger.debug(f'User is calling me {nickname}')
            ctx['to_me'] = True
            msg = msg[m.end():]

    session = NLPSession(bot, ctx, msg)

    # use msg_text here because CQ code "share" may be very long,
    # at the same time some plugins may want to handle it
    msg_text_length = len(session.msg_text)

    futures = []
    for p in _nl_processors:
        if not p.allow_empty_message and not session.msg:
            # don't allow empty msg, but it is one, so skip to next
            continue

        if p.only_short_message and \
                msg_text_length > bot.config.SHORT_MESSAGE_MAX_LENGTH:
            continue

        if p.only_to_me and not ctx['to_me']:
            continue

        should_run = await perm.check_permission(bot, ctx, p.permission)
        if should_run and p.keywords:
            for kw in p.keywords:
                if kw in session.msg_text:
                    break
            else:
                # no keyword matches
                should_run = False

        if should_run:
            futures.append(asyncio.ensure_future(p.func(session)))

    if futures:
        # wait for possible results, and sort them by confidence
        results = []
        for fut in futures:
            try:
                results.append(await fut)
            except Exception as e:
                logger.error('An exception occurred while running '
                             'some natural language processor:')
                logger.exception(e)
        results = sorted(filter(lambda r: r, results),
                         key=lambda r: r.confidence, reverse=True)
        logger.debug(f'NLP results: {results}')
        if results and results[0].confidence >= 60.0:
            # choose the result with highest confidence
            logger.debug(f'NLP result with highest confidence: {results[0]}')
            return await call_command(bot, ctx, results[0].cmd_name,
                                      args=results[0].cmd_args,
                                      check_perm=False)
        else:
            logger.debug('No NLP result having enough confidence')
    return False
