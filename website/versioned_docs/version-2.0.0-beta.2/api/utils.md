---
sidebar_position: 8
description: nonebot.utils 模块
---

# nonebot.utils

本模块包含了 NoneBot 的一些工具函数

## _def_ `escape_tag(s)` {#escape_tag}

- **说明**

  用于记录带颜色日志时转义 `<tag>` 类型特殊标签

  参考: [loguru color 标签](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

- **参数**

  - `s` (str): 需要转义的字符串

- **返回**

  - str

## _def_ `generic_check_issubclass(cls, class_or_tuple)` {#generic_check_issubclass}

- **说明**

  检查 cls 是否是 class_or_tuple 中的一个类型子类。

  特别的，如果 cls 是 `typing.Union` 或 `types.UnionType` 类型，
  则会检查其中的类型是否是 class_or_tuple 中的一个类型子类。（None 会被忽略）

- **参数**

  - `class_or_tuple` (Type[Any] | tuple[Type[Any], ...])

- **返回**

  - bool

## _def_ `is_coroutine_callable(call)` {#is_coroutine_callable}

- **说明**

  检查 call 是否是一个 callable 协程函数

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any)

- **返回**

  - bool

## _def_ `is_gen_callable(call)` {#is_gen_callable}

- **说明**

  检查 call 是否是一个生成器函数

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any)

- **返回**

  - bool

## _def_ `is_async_gen_callable(call)` {#is_async_gen_callable}

- **说明**

  检查 call 是否是一个异步生成器函数

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any)

- **返回**

  - bool

## _def_ `run_sync(call)` {#run_sync}

- **说明**

  一个用于包装 sync function 为 async function 的装饰器

- **参数**

  - `call` (((~ P)) -> (~ R)): 被装饰的同步函数

- **返回**

  - ((~ P)) -> Coroutine[NoneType, NoneType, (~ R)]

## _def_ `run_sync_ctx_manager(cm)` {#run_sync_ctx_manager}

- **说明**

  一个用于包装 sync context manager 为 async context manager 的执行函数

- **参数**

  - `cm` (ContextManager[(~ T)])

- **返回**

  - AsyncGenerator[(~ T), NoneType]

## _def_ `get_name(obj)` {#get_name}

- **说明**

  获取对象的名称

- **参数**

  - `obj` (Any)

- **返回**

  - str

## _class_ `DataclassEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)` {#DataclassEncoder}

- **说明**

  在 JSON 序列化 {re}`nonebot.adapters._message.Message` (List[Dataclass]) 时使用的 `JSONEncoder`

- **参数**

  - `skipkeys`

  - `ensure_ascii`

  - `check_circular`

  - `allow_nan`

  - `sort_keys`

  - `indent`

  - `separators`

  - `default`

### _method_ `default(self, o)` {#DataclassEncoder-default}

- **参数**

  - `o`

- **返回**

  - Unknown

## _def_ `logger_wrapper(logger_name)` {#logger_wrapper}

- **说明**

  用于打印 adapter 的日志。

- **参数**

  - `logger_name` (str): adapter 的名称

- **返回**

  - Unknown: 日志记录函数

    - level: 日志等级
    - message: 日志信息
    - exception: 异常信息
