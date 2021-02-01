from functools import wraps
from typing import Callable, Coroutine, TypeVar

import httpx
from pydantic import ValidationError, validate_arguments, Extra

import nonebot.exception as exception
from nonebot.log import logger
from nonebot.utils import escape_tag

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])
_AnyCallable = TypeVar("_AnyCallable", bound=Callable)


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
