import re
from typing import TYPE_CHECKING, Any, Optional

from nonebot.message import handle_event
from nonebot.typing import overrides
from nonebot.utils import DataclassEncoder, escape_tag, logger_wrapper

from .event import Event, GroupMessage, MessageEvent, MessageSource
from .message import MessageSegment, MessageType

if TYPE_CHECKING:
    from .bot import Bot


class Log:

    @staticmethod
    def log(level: str, message: str, exception: Optional[Exception] = None):
        logger = logger_wrapper('MIRAI')
        message = '<e>' + escape_tag(message) + '</e>'
        logger(level=level.upper(), message=message, exception=exception)

    @classmethod
    def info(cls, message: Any):
        cls.log('INFO', str(message))

    @classmethod
    def debug(cls, message: Any):
        cls.log('DEBUG', str(message))

    @classmethod
    def warn(cls, message: Any):
        cls.log('WARNING', str(message))

    @classmethod
    def error(cls, message: Any, exception: Optional[Exception] = None):
        cls.log('ERROR', str(message), exception=exception)


def process_source(bot: "Bot", event: MessageEvent) -> MessageEvent:
    source = event.message_chain.extract_first(MessageType.SOURCE)
    if source is not None:
        event.source = MessageSource.parse_obj(source.data)
    return event


def process_at(bot: "Bot", event: GroupMessage) -> GroupMessage:
    at = event.message_chain.extract_first(MessageType.AT)
    if at is not None:
        if at.data['target'] == event.self_id:
            event.to_me = True
        else:
            event.message_chain.insert(0, at)
    if not event.message_chain:
        event.message_chain.append(MessageSegment.plain(''))
    return event


def process_nick(bot: "Bot", event: GroupMessage) -> GroupMessage:
    plain = event.message_chain.extract_first(MessageType.PLAIN)
    if plain is not None:
        text = str(plain)
        nick_regex = '|'.join(filter(lambda x: x, bot.config.nickname))
        matched = re.search(rf"^({nick_regex})([\s,，]*|$)", text, re.IGNORECASE)
        if matched is not None:
            event.to_me = True
            nickname = matched.group(1)
            Log.info(f'User is calling me {nickname}')
            plain.data['text'] = text[matched.end():]
        event.message_chain.insert(0, plain)
    return event


def process_reply(bot: "Bot", event: GroupMessage) -> GroupMessage:
    reply = event.message_chain.extract_first(MessageType.QUOTE)
    if reply is not None:
        if reply.data['senderId'] == event.self_id:
            event.to_me = True
        else:
            event.message_chain.insert(0, reply)
    return event


async def process_event(bot: "Bot", event: Event) -> None:
    if isinstance(event, MessageEvent):
        Log.debug(event.message_chain)
        event = process_source(bot, event)
        if isinstance(event, GroupMessage):
            event = process_nick(bot, event)
            event = process_at(bot, event)
            event = process_reply(bot, event)
    await handle_event(bot, event)


class MiraiDataclassEncoder(DataclassEncoder):

    @overrides(DataclassEncoder)
    def default(self, o):
        if isinstance(o, MessageSegment):
            return o.as_dict()
        return super().default(o)
