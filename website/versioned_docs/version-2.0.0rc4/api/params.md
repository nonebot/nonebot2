---
sidebar_position: 4
description: nonebot.params 模块
---

# nonebot.params

本模块定义了依赖注入的各类参数。

## _def_ `Arg(key=None)` {#Arg}

- **说明:** `got` 的 Arg 参数消息

- **参数**

  - `key` (str | None)

- **返回**

  - Any

## _def_ `ArgStr(key=None)` {#ArgStr}

- **说明:** `got` 的 Arg 参数消息文本

- **参数**

  - `key` (str | None)

- **返回**

  - str

## _def_ `Depends(dependency=None, *, use_cache=True)` {#Depends}

- **说明:** 子依赖装饰器

- **参数**

  - `dependency` ([T_Handler](typing.md#T_Handler) | None): 依赖函数。默认为参数的类型注释。

  - `use_cache` (bool): 是否使用缓存。默认为 `True`。

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

  async def handler(param_name: Any = Depends(depend_func), gen: Any = Depends(depend_gen_func)):
      ...
  ```

## _class_ `ArgParam(<auto>)` {#ArgParam}

- **说明:** `got` 的 Arg 参数

- **参数**

  auto

## _class_ `BotParam(<auto>)` {#BotParam}

- **说明:** 参数

- **参数**

  auto

## _class_ `EventParam(<auto>)` {#EventParam}

- **说明:** 参数

- **参数**

  auto

## _class_ `StateParam(<auto>)` {#StateParam}

- **说明:** 事件处理状态参数

- **参数**

  auto

## _class_ `DependParam(<auto>)` {#DependParam}

- **说明:** 子依赖参数

- **参数**

  auto

## _def_ `ArgPlainText(key=None)` {#ArgPlainText}

- **说明:** `got` 的 Arg 参数消息纯文本

- **参数**

  - `key` (str | None)

- **返回**

  - str

## _class_ `DefaultParam(<auto>)` {#DefaultParam}

- **说明:** 默认值参数

- **参数**

  auto

## _class_ `MatcherParam(<auto>)` {#MatcherParam}

- **说明:** 事件响应器实例参数

- **参数**

  auto

## _class_ `ExceptionParam(<auto>)` {#ExceptionParam}

- **说明:** `run_postprocessor` 的异常参数

- **参数**

  auto

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

  - str

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
