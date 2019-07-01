import asyncio
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


def on_natural_language(keywords: Union[Optional[Iterable], str, Callable] = None,
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
        if isinstance(keywords, str):
            keywords = (keywords,)
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
    """
    Deprecated.
    Use class IntentCommand instead.
    """
    confidence: float
    cmd_name: Union[str, CommandName_T]
    cmd_args: Optional[CommandArgs_T] = None

    def to_intent_command(self):
        return IntentCommand(confidence=self.confidence,
                             name=self.cmd_name,
                             args=self.cmd_args)


class IntentCommand(NamedTuple):
    """
    To represent a command that we think the user may be intended to call.
    """
    confidence: float
    name: Union[str, CommandName_T]
    args: Optional[CommandArgs_T] = None
    current_arg: str = ''


async def handle_natural_language(bot: NoneBot, ctx: Context_T) -> bool:
    """
    Handle a message as natural language.

    This function is typically called by "handle_message".

    :param bot: NoneBot instance
    :param ctx: message context
    :return: the message is handled as natural language
    """
    session = NLPSession(bot, ctx, str(ctx['message']))

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
        # wait for intent commands, and sort them by confidence
        intent_commands = []
        for fut in futures:
            try:
                res = await fut
                if isinstance(res, NLPResult):
                    intent_commands.append(res.to_intent_command())
                elif isinstance(res, IntentCommand):
                    intent_commands.append(res)
            except Exception as e:
                logger.error('An exception occurred while running '
                             'some natural language processor:')
                logger.exception(e)

        intent_commands.sort(key=lambda ic: ic.confidence, reverse=True)
        logger.debug(f'Intent commands: {intent_commands}')

        if intent_commands and intent_commands[0].confidence >= 60.0:
            # choose the intent command with highest confidence
            chosen_cmd = intent_commands[0]
            logger.debug(
                f'Intent command with highest confidence: {chosen_cmd}')
            return await call_command(
                bot, ctx, chosen_cmd.name,
                args=chosen_cmd.args,
                current_arg=chosen_cmd.current_arg,
                check_perm=False
            )
        else:
            logger.debug('No intent command has enough confidence')
    return False
