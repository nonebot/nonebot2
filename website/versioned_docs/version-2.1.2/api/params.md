---
sidebar_position: 4
description: nonebot.params 模块
---

# nonebot.params

本模块定义了依赖注入的各类参数。

## _def_ `Arg(key=None)` {#Arg}

- **说明:** Arg 参数消息

- **参数**

  - `key` (str | None)

- **返回**

  - Any

## _def_ `ArgStr(key=None)` {#ArgStr}

- **说明:** Arg 参数消息文本

- **参数**

  - `key` (str | None)

- **返回**

  - str

## _def_ `Depends(dependency=None, *, use_cache=True, validate=False)` {#Depends}

- **说明:** 子依赖装饰器

- **参数**

  - `dependency` ([T_Handler](typing.md#T-Handler) | None): 依赖函数。默认为参数的类型注释。

  - `use_cache` (bool): 是否使用缓存。默认为 `True`。

  - `validate` (bool | FieldInfo): 是否使用 Pydantic 类型校验。默认为 `False`。

- **返回**

  - Any

- **用法**

  ```python
  def depend_func() -> Any:
      return ...

  def depend_gen_func():
      try:
          yield ...
      finally:
          ...

  async def handler(
      param_name: Any = Depends(depend_func),
      gen: Any = Depends(depend_gen_func),
  ):
      ...
  ```

## _class_ `ArgParam(*args, validate=False, **kwargs)` {#ArgParam}

- **说明**

  Arg 注入参数

  本注入解析事件响应器操作 `got` 所获取的参数。

  可以通过 `Arg`、`ArgStr`、`ArgPlainText` 等函数参数 `key` 指定获取的参数，
  留空则会根据参数名称获取。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `BotParam(*args, validate=False, **kwargs)` {#BotParam}

- **说明**

  注入参数。

  本注入解析所有类型为且仅为 [Bot](adapters/index.md#Bot) 及其子类或 `None` 的参数。

  为保证兼容性，本注入还会解析名为 `bot` 且没有类型注解的参数。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `EventParam(*args, validate=False, **kwargs)` {#EventParam}

- **说明**

  注入参数

  本注入解析所有类型为且仅为 [Event](adapters/index.md#Event) 及其子类或 `None` 的参数。

  为保证兼容性，本注入还会解析名为 `event` 且没有类型注解的参数。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `StateParam(*args, validate=False, **kwargs)` {#StateParam}

- **说明**

  事件处理状态注入参数

  本注入解析所有类型为 `T_State` 的参数。

  为保证兼容性，本注入还会解析名为 `state` 且没有类型注解的参数。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `DependParam(*args, validate=False, **kwargs)` {#DependParam}

- **说明**

  子依赖注入参数。

  本注入解析所有子依赖注入，然后将它们的返回值作为参数值传递给父依赖。

  本注入应该具有最高优先级，因此应该在其他参数之前检查。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _def_ `ArgPlainText(key=None)` {#ArgPlainText}

- **说明:** Arg 参数消息纯文本

- **参数**

  - `key` (str | None)

- **返回**

  - str

## _class_ `DefaultParam(*args, validate=False, **kwargs)` {#DefaultParam}

- **说明**

  默认值注入参数

  本注入解析所有剩余未能解析且具有默认值的参数。

  本注入参数应该具有最低优先级，因此应该在所有其他注入参数之后使用。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `MatcherParam(*args, validate=False, **kwargs)` {#MatcherParam}

- **说明**

  事件响应器实例注入参数

  本注入解析所有类型为且仅为 [Matcher](matcher.md#Matcher) 及其子类或 `None` 的参数。

  为保证兼容性，本注入还会解析名为 `matcher` 且没有类型注解的参数。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `ExceptionParam(*args, validate=False, **kwargs)` {#ExceptionParam}

- **说明**

  的异常注入参数

  本注入解析所有类型为 `Exception` 或 `None` 的参数。

  为保证兼容性，本注入还会解析名为 `exception` 且没有类型注解的参数。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _def_ `EventType()` {#EventType}

- **说明:** 类型参数

- **参数**

  empty

- **返回**

  - str

## _def_ `EventMessage()` {#EventMessage}

- **说明:** 消息参数

- **参数**

  empty

- **返回**

  - Any

## _def_ `EventPlainText()` {#EventPlainText}

- **说明:** 纯文本消息参数

- **参数**

  empty

- **返回**

  - str

## _def_ `EventToMe()` {#EventToMe}

- **说明:** `to_me` 参数

- **参数**

  empty

- **返回**

  - bool

## _def_ `Command()` {#Command}

- **说明:** 消息命令元组

- **参数**

  empty

- **返回**

  - tuple[str, ...]

## _def_ `RawCommand()` {#RawCommand}

- **说明:** 消息命令文本

- **参数**

  empty

- **返回**

  - str

## _def_ `CommandArg()` {#CommandArg}

- **说明:** 消息命令参数

- **参数**

  empty

- **返回**

  - Any

## _def_ `CommandStart()` {#CommandStart}

- **说明:** 消息命令开头

- **参数**

  empty

- **返回**

  - str

## _def_ `CommandWhitespace()` {#CommandWhitespace}

- **说明:** 消息命令与参数之间的空白

- **参数**

  empty

- **返回**

  - str

## _def_ `ShellCommandArgs()` {#ShellCommandArgs}

- **说明:** shell 命令解析后的参数字典

- **参数**

  empty

- **返回**

  - Any

## _def_ `ShellCommandArgv()` {#ShellCommandArgv}

- **说明:** shell 命令原始参数列表

- **参数**

  empty

- **返回**

  - Any

## _def_ `RegexMatched()` {#RegexMatched}

- **说明:** 正则匹配结果

- **参数**

  empty

- **返回**

  - Match[str]

## _def_ `RegexStr()` {#RegexStr}

- **说明:** 正则匹配结果文本

- **参数**

  empty

- **返回**

  - str

## _def_ `RegexGroup()` {#RegexGroup}

- **说明:** 正则匹配结果 group 元组

- **参数**

  empty

- **返回**

  - tuple[Any, ...]

## _def_ `RegexDict()` {#RegexDict}

- **说明:** 正则匹配结果 group 字典

- **参数**

  empty

- **返回**

  - dict[str, Any]

## _def_ `Startswith()` {#Startswith}

- **说明:** 响应触发前缀

- **参数**

  empty

- **返回**

  - str

## _def_ `Endswith()` {#Endswith}

- **说明:** 响应触发后缀

- **参数**

  empty

- **返回**

  - str

## _def_ `Fullmatch()` {#Fullmatch}

- **说明:** 响应触发完整消息

- **参数**

  empty

- **返回**

  - str

## _def_ `Keyword()` {#Keyword}

- **说明:** 响应触发关键字

- **参数**

  empty

- **返回**

  - str

## _def_ `Received(id=None, default=None)` {#Received}

- **说明:** `receive` 事件参数

- **参数**

  - `id` (str | None)

  - `default` (Any)

- **返回**

  - Any

## _def_ `LastReceived(default=None)` {#LastReceived}

- **说明:** `last_receive` 事件参数

- **参数**

  - `default` (Any)

- **返回**

  - Any
