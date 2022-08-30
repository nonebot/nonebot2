"""本模块包含了 NoneBot 的一些工具函数

FrontMatter:
    sidebar_position: 8
    description: nonebot.utils 模块
"""

import re
import json
import asyncio
import inspect
import dataclasses
from pathlib import Path
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
    Coroutine,
    AsyncGenerator,
    ContextManager,
    overload,
)

from pydantic.typing import is_union, is_none_type

from nonebot.log import logger
from nonebot.typing import overrides

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def escape_tag(s: str) -> str:
    """用于记录带颜色日志时转义 `<tag>` 类型特殊标签

    参考: [loguru color 标签](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

    参数:
        s: 需要转义的字符串
    """
    return re.sub(r"</?((?:[fb]g\s)?[^<>\s]*)>", r"\\\g<0>", s)


def generic_check_issubclass(
    cls: Any, class_or_tuple: Union[Type[Any], Tuple[Type[Any], ...]]
) -> bool:
    """检查 cls 是否是 class_or_tuple 中的一个类型子类。

    特别的，如果 cls 是 `typing.Union` 或 `types.UnionType` 类型，
    则会检查其中的类型是否是 class_or_tuple 中的一个类型子类。（None 会被忽略）
    """
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        origin = get_origin(cls)
        if is_union(origin):
            return all(
                is_none_type(type_) or generic_check_issubclass(type_, class_or_tuple)
                for type_ in get_args(cls)
            )
        elif origin:
            return issubclass(origin, class_or_tuple)
        return False


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    """检查 call 是否是一个 callable 协程函数"""
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(func_)


def is_gen_callable(call: Callable[..., Any]) -> bool:
    """检查 call 是否是一个生成器函数"""
    if inspect.isgeneratorfunction(call):
        return True
    func_ = getattr(call, "__call__", None)
    return inspect.isgeneratorfunction(func_)


def is_async_gen_callable(call: Callable[..., Any]) -> bool:
    """检查 call 是否是一个异步生成器函数"""
    if inspect.isasyncgenfunction(call):
        return True
    func_ = getattr(call, "__call__", None)
    return inspect.isasyncgenfunction(func_)


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
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
    """一个用于包装 sync context manager 为 async context manager 的执行函数"""
    try:
        yield await run_sync(cm.__enter__)()
    except Exception as e:
        ok = await run_sync(cm.__exit__)(type(e), e, None)
        if not ok:
            raise e
    else:
        await run_sync(cm.__exit__)(None, None, None)


@overload
async def run_coro_with_catch(
    coro: Coroutine[Any, Any, T],
    exc: Tuple[Type[Exception], ...],
) -> Union[T, None]:
    ...


@overload
async def run_coro_with_catch(
    coro: Coroutine[Any, Any, T],
    exc: Tuple[Type[Exception], ...],
    return_on_err: R,
) -> Union[T, R]:
    ...


async def run_coro_with_catch(
    coro: Coroutine[Any, Any, T],
    exc: Tuple[Type[Exception], ...],
    return_on_err: Optional[R] = None,
) -> Optional[Union[T, R]]:
    try:
        return await coro
    except exc:
        return return_on_err


def get_name(obj: Any) -> str:
    """获取对象的名称"""
    if inspect.isfunction(obj) or inspect.isclass(obj):
        return obj.__name__
    return obj.__class__.__name__


def path_to_module_name(path: Path) -> str:
    rel_path = path.resolve().relative_to(Path(".").resolve())
    if rel_path.stem == "__init__":
        return ".".join(rel_path.parts[:-1])
    else:
        return ".".join(rel_path.parts[:-1] + (rel_path.stem,))


class DataclassEncoder(json.JSONEncoder):
    """在JSON序列化 {re}`nonebot.adapters._message.Message` (List[Dataclass]) 时使用的 `JSONEncoder`"""

    @overrides(json.JSONEncoder)
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return {f.name: getattr(o, f.name) for f in dataclasses.fields(o)}
        return super().default(o)


def logger_wrapper(logger_name: str):
    """用于打印 adapter 的日志。

    参数:
        logger_name: adapter 的名称

    返回:
        日志记录函数

            - level: 日志等级
            - message: 日志信息
            - exception: 异常信息
    """

    def log(level: str, message: str, exception: Optional[Exception] = None):
        logger.opt(colors=True, exception=exception).log(
            level, f"<m>{escape_tag(logger_name)}</m> | {message}"
        )

    return log
