---
sidebar_position: 8
description: nonebot.utils 模块
---

# nonebot.utils

本模块包含了 NoneBot 的一些工具函数

## _def_ `escape_tag(s)` {#escape-tag}

- **说明**

  用于记录带颜色日志时转义 `<tag>` 类型特殊标签

  参考: [loguru color 标签](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

- **参数**

  - `s` (str): 需要转义的字符串

- **返回**

  - str

## _def_ `generic_check_issubclass(cls, class_or_tuple)` {#generic-check-issubclass}

- **说明**

  检查 cls 是否是 class_or_tuple 中的一个类型子类。

  特别的：

  - 如果 cls 是 `typing.Union` 或 `types.UnionType` 类型，
    则会检查其中的所有类型是否是 class_or_tuple 中一个类型的子类或 None。
  - 如果 cls 是 `typing.TypeVar` 类型，
    则会检查其 `__bound__` 或 `__constraints__`
    是否是 class_or_tuple 中一个类型的子类或 None。

- **参数**

  - `cls` (Any)

  - `class_or_tuple` (type[Any] | tuple[type[Any], ...])

- **返回**

  - bool

## _def_ `is_coroutine_callable(call)` {#is-coroutine-callable}

- **说明:** 检查 call 是否是一个 callable 协程函数

- **参数**

  - `call` ((...) -> Any)

- **返回**

  - bool

## _def_ `is_gen_callable(call)` {#is-gen-callable}

- **说明:** 检查 call 是否是一个生成器函数

- **参数**

  - `call` ((...) -> Any)

- **返回**

  - bool

## _def_ `is_async_gen_callable(call)` {#is-async-gen-callable}

- **说明:** 检查 call 是否是一个异步生成器函数

- **参数**

  - `call` ((...) -> Any)

- **返回**

  - bool

## _def_ `run_sync(call)` {#run-sync}

- **说明:** 一个用于包装 sync function 为 async function 的装饰器

- **参数**

  - `call` ((P) -> R): 被装饰的同步函数

- **返回**

  - (P) -> Coroutine[None, None, R]

## _def_ `run_sync_ctx_manager(cm)` {#run-sync-ctx-manager}

- **说明:** 一个用于包装 sync context manager 为 async context manager 的执行函数

- **参数**

  - `cm` (ContextManager[T])

- **返回**

  - AsyncGenerator[T, None]

## _async def_ `run_coro_with_catch(coro, exc, return_on_err=None)` {#run-coro-with-catch}

- **说明:** 运行协程并当遇到指定异常时返回指定值。

- **重载**

  **1.** `(coro, exc, return_on_err=None) -> T | None`

  - **参数**

    - `coro` (Coroutine[Any, Any, T])

    - `exc` (tuple[type[Exception], ...])

    - `return_on_err` (None)

  - **返回**

    - T | None

  **2.** `(coro, exc, return_on_err) -> T | R`

  - **参数**

    - `coro` (Coroutine[Any, Any, T])

    - `exc` (tuple[type[Exception], ...])

    - `return_on_err` (R)

  - **返回**

    - T | R

- **参数**

  - `coro`: 要运行的协程

  - `exc`: 要捕获的异常

  - `return_on_err`: 当发生异常时返回的值

- **返回**

  协程的返回值或发生异常时的指定值

## _def_ `get_name(obj)` {#get-name}

- **说明:** 获取对象的名称

- **参数**

  - `obj` (Any)

- **返回**

  - str

## _def_ `path_to_module_name(path)` {#path-to-module-name}

- **说明:** 转换路径为模块名

- **参数**

  - `path` (Path)

- **返回**

  - str

## _def_ `resolve_dot_notation(obj_str, default_attr, default_prefix=None)` {#resolve-dot-notation}

- **说明:** 解析并导入点分表示法的对象

- **参数**

  - `obj_str` (str)

  - `default_attr` (str)

  - `default_prefix` (str | None)

- **返回**

  - Any

## _class_ `classproperty(func)` {#classproperty}

- **说明:** 类属性装饰器

- **参数**

  - `func` ((Any) -> T)

## _class_ `DataclassEncoder(<auto>)` {#DataclassEncoder}

- **说明:** 可以序列化 [Message](adapters/index.md#Message)(List[Dataclass]) 的 `JSONEncoder`

- **参数**

  auto

### _method_ `default(o)` {#DataclassEncoder-default}

- **参数**

  - `o`

- **返回**

  - untyped

## _def_ `logger_wrapper(logger_name)` {#logger-wrapper}

- **说明:** 用于打印 adapter 的日志。

- **参数**

  - `logger_name` (str): adapter 的名称

- **返回**

  - untyped: 日志记录函数

    日志记录函数的参数:

    - level: 日志等级
    - message: 日志信息
    - exception: 异常信息
