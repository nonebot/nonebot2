import re
import json
import asyncio
import inspect
import dataclasses
from functools import wraps, partial
from contextlib import asynccontextmanager
from typing_extensions import ParamSpec, get_args, get_origin
from typing import (
    Any,
    Type,
    Tuple,
    Union,
    TypeVar,
    Callable,
    Optional,
    Awaitable,
    AsyncGenerator,
    ContextManager,
)

from nonebot.log import logger
from nonebot.typing import overrides

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


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


def generic_check_issubclass(
    cls: Any, class_or_tuple: Union[Type[Any], Tuple[Type[Any], ...]]
) -> bool:
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        origin = get_origin(cls)
        if origin is Union:
            for type_ in get_args(cls):
                if type_ is not type(None) and not generic_check_issubclass(
                    type_, class_or_tuple
                ):
                    return False
            return True
        elif origin:
            return issubclass(origin, class_or_tuple)
        return False


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(func_)


def is_gen_callable(call: Callable[..., Any]) -> bool:
    if inspect.isgeneratorfunction(call):
        return True
    func_ = getattr(call, "__call__", None)
    return inspect.isgeneratorfunction(func_)


def is_async_gen_callable(call: Callable[..., Any]) -> bool:
    if inspect.isasyncgenfunction(call):
        return True
    func_ = getattr(call, "__call__", None)
    return inspect.isasyncgenfunction(func_)


def run_sync(call: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """
    :说明:

      一个用于包装 sync function 为 async function 的装饰器

    :参数:

      * ``call: Callable[P, R]``: 被装饰的同步函数

    :返回:

      - ``Callable[P, Awaitable[R]]``
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


@asynccontextmanager
async def run_sync_ctx_manager(
    cm: ContextManager[T],
) -> AsyncGenerator[T, None]:
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

    * ``level: Literal["CRITICAL", "WARNING", "INFO", "DEBUG", "TRACE"]``: 日志等级
    * ``message: str``: 日志信息
    * ``exception: Optional[Exception]``: 异常信息
    """

    def log(level: str, message: str, exception: Optional[Exception] = None):
        logger.opt(colors=True, exception=exception).log(
            level, f"<m>{escape_tag(logger_name)}</m> | " + message
        )

    return log
