import re
import json
import asyncio
import inspect
import dataclasses
from functools import wraps, partial
from typing_extensions import ParamSpec
from contextlib import asynccontextmanager
from typing import (Any, TypeVar, Callable, Optional, Awaitable, AsyncGenerator,
                    ContextManager)

from nonebot.log import logger
from nonebot.typing import overrides

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


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


def is_coroutine_callable(func: Callable[..., Any]) -> bool:
    if inspect.isroutine(func):
        return inspect.iscoroutinefunction(func)
    if inspect.isclass(func):
        return False
    func_ = getattr(func, "__call__", None)
    return inspect.iscoroutinefunction(func_)


def is_gen_callable(func: Callable[..., Any]) -> bool:
    if inspect.isgeneratorfunction(func):
        return True
    func_ = getattr(func, "__call__", None)
    return inspect.isgeneratorfunction(func_)


def is_async_gen_callable(func: Callable[..., Any]) -> bool:
    if inspect.isasyncgenfunction(func):
        return True
    func_ = getattr(func, "__call__", None)
    return inspect.isasyncgenfunction(func_)


def run_sync(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """
    :说明:

      一个用于包装 sync function 为 async function 的装饰器

    :参数:

      * ``func: Callable[P, R]``: 被装饰的同步函数

    :返回:

      - ``Callable[P, Awaitable[R]]``
    """

    @wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


@asynccontextmanager
async def run_sync_ctx_manager(
    cm: ContextManager[T],) -> AsyncGenerator[T, None]:
    try:
        yield await run_sync(cm.__enter__)()
    except Exception as e:
        ok = await run_sync(cm.__exit__)(type(e), e, None)
        if not ok:
            raise e
    else:
        await run_sync(cm.__exit__)(None, None, None)


def get_name(obj: Any) -> str:
    if inspect.isfunction(obj) or inspect.isclass(obj):
        return obj.__name__
    return obj.__class__.__name__


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
            level, f"<m>{escape_tag(logger_name)}</m> | " + message)

    return log
