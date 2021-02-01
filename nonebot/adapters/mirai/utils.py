import re
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional, TypeVar

import httpx
from pydantic import Extra, ValidationError, validate_arguments

import nonebot.exception as exception
from nonebot.log import logger
from nonebot.utils import escape_tag, logger_wrapper

from .event import Event, GroupMessage
from .message import MessageSegment, MessageType

if TYPE_CHECKING:
    from .bot import Bot

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])
_AnyCallable = TypeVar("_AnyCallable", bound=Callable)


class Log:
    _log = logger_wrapper('MIRAI')

    @classmethod
    def info(cls, message: Any):
        cls._log('INFO', str(message))

    @classmethod
    def debug(cls, message: Any):
        cls._log('DEBUG', str(message))

    @classmethod
    def warn(cls, message: Any):
        cls._log('WARNING', str(message))

    @classmethod
    def error(cls, message: Any, exception: Optional[Exception] = None):
        cls._log('ERROR', str(message), exception=exception)


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
    """
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


async def check_tome(bot: "Bot", event: "Event") -> "Event":
    if not isinstance(event, GroupMessage):
        return event

    def _is_at(event: GroupMessage) -> bool:
        for segment in event.message_chain:
            segment: MessageSegment
            if segment.type != MessageType.AT:
                continue
            if segment.data['target'] == event.self_id:
                return True
        return False

    def _is_nick(event: GroupMessage) -> bool:
        text = event.get_plaintext()
        if not text:
            return False
        nick_regex = '|'.join(
            {i.strip() for i in bot.config.nickname if i.strip()})
        matched = re.search(rf"^({nick_regex})([\s,，]*|$)", text, re.IGNORECASE)
        if matched is None:
            return False
        Log.info(f'User is calling me {matched.group(1)}')
        return True

    def _is_reply(event: GroupMessage) -> bool:
        for segment in event.message_chain:
            segment: MessageSegment
            if segment.type != MessageType.QUOTE:
                continue
            if segment.data['senderId'] == event.self_id:
                return True
        return False

    event.to_me = any([_is_at(event), _is_reply(event), _is_nick(event)])
    return event
