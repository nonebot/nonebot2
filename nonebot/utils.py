"""本模块包含了 NoneBot 的一些工具函数

FrontMatter:
    mdx:
        format: md
    sidebar_position: 8
    description: nonebot.utils 模块
"""

from collections import deque
from collections.abc import AsyncGenerator, Coroutine, Generator, Mapping, Sequence
import contextlib
from contextlib import AbstractContextManager, asynccontextmanager
import dataclasses
from functools import partial, wraps
import importlib
import inspect
import json
from pathlib import Path
import re
from typing import Any, Callable, Generic, Optional, TypeVar, Union, overload
from typing_extensions import ParamSpec, get_args, get_origin, override

import anyio
import anyio.to_thread
from exceptiongroup import BaseExceptionGroup, catch
from pydantic import BaseModel

from nonebot.log import logger
from nonebot.typing import (
    all_literal_values,
    is_none_type,
    origin_is_literal,
    origin_is_union,
    type_has_args,
)

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
E = TypeVar("E", bound=BaseException)


def escape_tag(s: str) -> str:
    """用于记录带颜色日志时转义 `<tag>` 类型特殊标签

    参考: [loguru color 标签](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

    参数:
        s: 需要转义的字符串
    """
    return re.sub(r"</?((?:[fb]g\s)?[^<>\s]*)>", r"\\\g<0>", s)


def deep_update(
    mapping: dict[K, Any], *updating_mappings: dict[K, Any]
) -> dict[K, Any]:
    """深度更新合并字典"""
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if (
                k in updated_mapping
                and isinstance(updated_mapping[k], dict)
                and isinstance(v, dict)
            ):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping


def lenient_issubclass(
    cls: Any, class_or_tuple: Union[type[Any], tuple[type[Any], ...]]
) -> bool:
    """检查 cls 是否是 class_or_tuple 中的一个类型子类并忽略类型错误。"""
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        return False


def generic_check_issubclass(
    cls: Any, class_or_tuple: Union[type[Any], tuple[type[Any], ...]]
) -> bool:
    """检查 cls 是否是 class_or_tuple 中的一个类型子类。

    特别的：

    - 如果 cls 是 `typing.TypeVar` 类型，
      则会检查其 `__bound__` 或 `__constraints__`
      是否是 class_or_tuple 中一个类型的子类或 None。
    - 如果 cls 是 `typing.Union` 或 `types.UnionType` 类型，
      则会检查其中的所有类型是否是 class_or_tuple 中一个类型的子类或 None。
    - 如果 cls 是 `typing.Literal` 类型，
      则会检查其中的所有值是否是 class_or_tuple 中一个类型的实例。
    - 如果 cls 是 `typing.List`、`typing.Dict` 等泛型类型，
      则会检查其原始类型是否是 class_or_tuple 中一个类型的子类。
    """
    # if the target is a TypeVar, we check it first
    if isinstance(cls, TypeVar):
        if cls.__constraints__:
            return all(
                is_none_type(type_) or generic_check_issubclass(type_, class_or_tuple)
                for type_ in cls.__constraints__
            )
        elif cls.__bound__:
            return generic_check_issubclass(cls.__bound__, class_or_tuple)
        return False
    # elif the target is not a generic type, we check it directly
    elif not type_has_args(cls):
        with contextlib.suppress(TypeError):
            return issubclass(cls, class_or_tuple)

    origin = get_origin(cls)
    if origin_is_union(origin):
        return all(
            is_none_type(type_) or generic_check_issubclass(type_, class_or_tuple)
            for type_ in get_args(cls)
        )
    elif origin_is_literal(origin):
        return all(
            is_none_type(value) or isinstance(value, class_or_tuple)
            for value in all_literal_values(cls)
        )
    # ensure generic List, Dict can be checked
    elif origin:
        # avoid class check error (typing.Final, typing.ClassVar, etc...)
        try:
            return issubclass(origin, class_or_tuple)
        except TypeError:
            return False
    return False


def type_is_complex(type_: type[Any]) -> bool:
    """检查 type_ 是否是复杂类型"""
    origin = get_origin(type_)
    return _type_is_complex_inner(type_) or _type_is_complex_inner(origin)


def _type_is_complex_inner(type_: Optional[type[Any]]) -> bool:
    if lenient_issubclass(type_, (str, bytes)):
        return False

    return lenient_issubclass(
        type_, (BaseModel, Mapping, Sequence, tuple, set, frozenset, deque)
    ) or dataclasses.is_dataclass(type_)


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
        return await anyio.to_thread.run_sync(
            partial(call, *args, **kwargs), abandon_on_cancel=True
        )

    return _wrapper


@asynccontextmanager
async def run_sync_ctx_manager(
    cm: AbstractContextManager[T],
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
    exc: tuple[type[Exception], ...],
    return_on_err: None = None,
) -> Union[T, None]: ...


@overload
async def run_coro_with_catch(
    coro: Coroutine[Any, Any, T],
    exc: tuple[type[Exception], ...],
    return_on_err: R,
) -> Union[T, R]: ...


async def run_coro_with_catch(
    coro: Coroutine[Any, Any, T],
    exc: tuple[type[Exception], ...],
    return_on_err: Optional[R] = None,
) -> Optional[Union[T, R]]:
    """运行协程并当遇到指定异常时返回指定值。

    参数:
        coro: 要运行的协程
        exc: 要捕获的异常
        return_on_err: 当发生异常时返回的值

    返回:
        协程的返回值或发生异常时的指定值
    """

    with catch({exc: lambda exc_group: None}):
        return await coro

    return return_on_err


async def run_coro_with_shield(coro: Coroutine[Any, Any, T]) -> T:
    """运行协程并在取消时屏蔽取消异常。

    参数:
        coro: 要运行的协程

    返回:
        协程的返回值
    """

    with anyio.CancelScope(shield=True):
        return await coro

    raise RuntimeError("This should not happen")


def flatten_exception_group(
    exc_group: BaseExceptionGroup[E],
) -> Generator[E, None, None]:
    for exc in exc_group.exceptions:
        if isinstance(exc, BaseExceptionGroup):
            yield from flatten_exception_group(exc)
        else:
            yield exc


def get_name(obj: Any) -> str:
    """获取对象的名称"""
    if inspect.isfunction(obj) or inspect.isclass(obj):
        return obj.__name__
    return obj.__class__.__name__


def path_to_module_name(path: Path) -> str:
    """转换路径为模块名"""
    rel_path = path.resolve().relative_to(Path.cwd().resolve())
    if rel_path.stem == "__init__":
        return ".".join(rel_path.parts[:-1])
    else:
        return ".".join((*rel_path.parts[:-1], rel_path.stem))


def resolve_dot_notation(
    obj_str: str, default_attr: str, default_prefix: Optional[str] = None
) -> Any:
    """解析并导入点分表示法的对象"""
    modulename, _, cls = obj_str.partition(":")
    if default_prefix is not None and modulename.startswith("~"):
        modulename = default_prefix + modulename[1:]
    module = importlib.import_module(modulename)
    if not cls:
        return getattr(module, default_attr)
    instance = module
    for attr_str in cls.split("."):
        instance = getattr(instance, attr_str)
    return instance


class classproperty(Generic[T]):
    """类属性装饰器"""

    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func

    def __get__(self, instance: Any, owner: Optional[type[Any]] = None) -> T:
        return self.func(type(instance) if owner is None else owner)


class DataclassEncoder(json.JSONEncoder):
    """可以序列化 {ref}`nonebot.adapters.Message`(List[Dataclass]) 的 `JSONEncoder`"""

    @override
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

        日志记录函数的参数:

        - level: 日志等级
        - message: 日志信息
        - exception: 异常信息
    """

    def log(level: str, message: str, exception: Optional[Exception] = None):
        logger.opt(colors=True, exception=exception).log(
            level, f"<m>{escape_tag(logger_name)}</m> | {message}"
        )

    return log
