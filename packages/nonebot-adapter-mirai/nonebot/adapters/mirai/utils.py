import re
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional, TypeVar

import httpx
from pydantic import Extra, ValidationError, validate_arguments

import nonebot.exception as exception
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.utils import escape_tag, logger_wrapper

from .event import Event, GroupMessage, MessageEvent, MessageSource
from .message import MessageType, MessageSegment

if TYPE_CHECKING:
    from .bot import Bot

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])
_AnyCallable = TypeVar("_AnyCallable", bound=Callable)


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


class ActionFailed(exception.ActionFailed):
    """
    :说明:

      API 请求成功返回数据，但 API 操作失败。
    """

    def __init__(self, **kwargs):
        super().__init__('mirai')
        self.data = kwargs.copy()

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % ', '.join(
            map(lambda m: '%s=%r' % m, self.data.items()))


class InvalidArgument(exception.AdapterException):
    """
    :说明:

      调用API的参数出错
    """

    def __init__(self, **kwargs):
        super().__init__('mirai')


def catch_network_error(function: _AsyncCallable) -> _AsyncCallable:
    r"""
    :说明:

      捕捉函数抛出的httpx网络异常并释放 ``NetworkError`` 异常

      处理返回数据, 在code不为0时释放 ``ActionFailed`` 异常

    \:\:\: warning
    此装饰器只支持使用了httpx的异步函数
    \:\:\:
    """

    @wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            data = await function(*args, **kwargs)
        except httpx.HTTPError:
            raise exception.NetworkError('mirai')
        logger.opt(colors=True).debug('<b>Mirai API returned data:</b> '
                                      f'<y>{escape_tag(str(data))}</y>')
        if isinstance(data, dict):
            if data.get('code', 0) != 0:
                raise ActionFailed(**data)
        return data

    return wrapper  # type: ignore


def argument_validation(function: _AnyCallable) -> _AnyCallable:
    """
    :说明:

      通过函数签名中的类型注解来对传入参数进行运行时校验

      会在参数出错时释放 ``InvalidArgument`` 异常
    """
    function = validate_arguments(config={
        'arbitrary_types_allowed': True,
        'extra': Extra.forbid
    })(function)

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValidationError:
            raise InvalidArgument

    return wrapper  # type: ignore


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
