import asyncio
import re
from collections import namedtuple
from typing import Dict, Any, Iterable, Optional, Callable, Union

from aiocqhttp.message import Message

from . import NoneBot, permission as perm
from .command import call_command
from .log import logger
from .session import BaseSession

_nl_processors = set()


class NLProcessor:
    __slots__ = ('func', 'keywords', 'permission', 'only_to_me')

    def __init__(self, *, func: Callable, keywords: Optional[Iterable],
                 permission: int, only_to_me: bool):
        self.func = func
        self.keywords = keywords
        self.permission = permission
        self.only_to_me = only_to_me


def on_natural_language(keywords: Union[Optional[Iterable], Callable] = None,
                        *, permission: int = perm.EVERYBODY,
                        only_to_me: bool = True) -> Callable:
    """
    Decorator to register a function as a natural language processor.

    :param keywords: keywords to respond, if None, respond to all messages
    :param permission: permission required by the processor
    :param only_to_me: only handle messages to me
    """

    def deco(func: Callable) -> Callable:
        nl_processor = NLProcessor(func=func, keywords=keywords,
                                   permission=permission,
                                   only_to_me=only_to_me)
        _nl_processors.add(nl_processor)
        return func

    if isinstance(keywords, Callable):
        # here "keywords" is the function to be decorated
        return on_natural_language()(keywords)
    else:
        return deco


class NLPSession(BaseSession):
    __slots__ = ('msg', 'msg_text', 'msg_images')

    def __init__(self, bot: NoneBot, ctx: Dict[str, Any], msg: str):
        super().__init__(bot, ctx)
        self.msg = msg
        tmp_msg = Message(msg)
        self.msg_text = tmp_msg.extract_plain_text()
        self.msg_images = [s.data['url'] for s in tmp_msg
                           if s.type == 'image' and 'url' in s.data]


NLPResult = namedtuple('NLPResult', (
    'confidence',
    'cmd_name',
    'cmd_args',
))


async def handle_natural_language(bot: NoneBot, ctx: Dict[str, Any]) -> bool:
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
        if not isinstance(bot.config.NICKNAME, Iterable):
            # noinspection PyUnusedLocal
            nicknames = (bot.config.NICKNAME,)
        else:
            # noinspection PyUnusedLocal
            nicknames = filter(lambda n: n, bot.config.NICKNAME)
        m = re.search(rf'^({"|".join(nicknames)})[\s,，]+', msg, re.IGNORECASE)
        if m:
            logger.debug(f'User is calling me {m.group(1)}')
            ctx['to_me'] = True
            msg = msg[m.end():]

    session = NLPSession(bot, ctx, msg)

    coros = []
    for p in _nl_processors:
        should_run = await perm.check_permission(bot, ctx, p.permission)
        if should_run and p.keywords:
            for kw in p.keywords:
                if kw in session.msg_text:
                    break
            else:
                # no keyword matches
                should_run = False
        if should_run and p.only_to_me and not ctx['to_me']:
            should_run = False

        if should_run:
            coros.append(p.func(session))

    if coros:
        # wait for possible results, and sort them by confidence
        results = sorted(filter(lambda r: r, await asyncio.gather(*coros)),
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
