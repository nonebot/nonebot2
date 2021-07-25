import re
import json
import asyncio
import dataclasses
from functools import wraps, partial
from typing import Any, Optional, Callable, Awaitable

from nonebot.log import logger
from nonebot.typing import overrides


def escape_tag(s: str) -> str:
    """
    :说明:

      用于记录带颜色日志时转义 ``<tag>`` 类型特殊标签

    :参数:

      * ``s: str``: 需要转义的字符串

    :返回:

      - ``str``
    """
    return re.sub(r"</?((?:[fb]g\s)?[^<>\s]*)>", r"\\\g<0>", s)


def run_sync(func: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    """
    :说明:

      一个用于包装 sync function 为 async function 的装饰器

    :参数:

      * ``func: Callable[..., Any]``: 被装饰的同步函数

    :返回:

      - ``Callable[..., Awaitable[Any]]``
    """

    @wraps(func)
    async def _wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


class DataclassEncoder(json.JSONEncoder):
    """
    :说明:

      在JSON序列化 ``Message`` (List[Dataclass]) 时使用的 ``JSONEncoder``
    """

    @overrides(json.JSONEncoder)
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def logger_wrapper(logger_name: str):
    """
    :说明:

    用于打印 adapter 的日志。

    :log 参数:

    * ``level: Literal['WARNING', 'DEBUG', 'INFO']``: 日志等级
    * ``message: str``: 日志信息
    * ``exception: Optional[Exception]``: 异常信息
    """

    def log(level: str, message: str, exception: Optional[Exception] = None):
        return logger.opt(colors=True, exception=exception).log(
            level, f"<m>{logger_name}</m> | " + message)

    return log
