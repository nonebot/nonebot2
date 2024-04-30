---
sidebar_position: 5
description: nonebot.rule 模块
---

# nonebot.rule

本模块是 [Matcher.rule](matcher.md#Matcher-rule) 的类型定义。

每个[事件响应器](matcher.md#Matcher)拥有一个
[Rule](#Rule)，其中是 `RuleChecker` 的集合。
只有当所有 `RuleChecker` 检查结果为 `True` 时继续运行。

## _class_ `Rule(*checkers)` {#Rule}

- **说明**

  规则类。

  当事件传递时，在 [Matcher](matcher.md#Matcher) 运行前进行检查。

- **参数**

  - `*checkers` ([T_RuleChecker](typing.md#T-RuleChecker) | [Dependent](dependencies/index.md#Dependent)[bool]): RuleChecker

- **用法**

  ```python
  Rule(async_function) & sync_function
  # 等价于
  Rule(async_function, sync_function)
  ```

### _instance-var_ `checkers` {#Rule-checkers}

- **类型:** set[[Dependent](dependencies/index.md#Dependent)[bool]]

- **说明:** 存储 `RuleChecker`

### _async method_ `__call__(bot, event, state, stack=None, dependency_cache=None)` {#Rule---call--}

- **说明:** 检查是否符合所有规则

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): Event 对象

  - `state` ([T_State](typing.md#T-State)): 当前 State

  - `stack` (AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None): 依赖缓存

- **返回**

  - bool

## _class_ `CMD_RESULT(<auto>)` {#CMD-RESULT}

- **参数**

  auto

## _class_ `TRIE_VALUE(<auto>)` {#TRIE-VALUE}

- **说明:** TRIE_VALUE(command_start, command)

- **参数**

  auto

## _class_ `StartswithRule(msg, ignorecase=False)` {#StartswithRule}

- **说明:** 检查消息纯文本是否以指定字符串开头。

- **参数**

  - `msg` (tuple[str, ...]): 指定消息开头字符串元组

  - `ignorecase` (bool): 是否忽略大小写

## _def_ `startswith(msg, ignorecase=False)` {#startswith}

- **说明:** 匹配消息纯文本开头。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头字符串元组

  - `ignorecase` (bool): 是否忽略大小写

- **返回**

  - [Rule](#Rule)

## _class_ `EndswithRule(msg, ignorecase=False)` {#EndswithRule}

- **说明:** 检查消息纯文本是否以指定字符串结尾。

- **参数**

  - `msg` (tuple[str, ...]): 指定消息结尾字符串元组

  - `ignorecase` (bool): 是否忽略大小写

## _def_ `endswith(msg, ignorecase=False)` {#endswith}

- **说明:** 匹配消息纯文本结尾。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头字符串元组

  - `ignorecase` (bool): 是否忽略大小写

- **返回**

  - [Rule](#Rule)

## _class_ `FullmatchRule(msg, ignorecase=False)` {#FullmatchRule}

- **说明:** 检查消息纯文本是否与指定字符串全匹配。

- **参数**

  - `msg` (tuple[str, ...]): 指定消息全匹配字符串元组

  - `ignorecase` (bool): 是否忽略大小写

## _def_ `fullmatch(msg, ignorecase=False)` {#fullmatch}

- **说明:** 完全匹配消息。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息全匹配字符串元组

  - `ignorecase` (bool): 是否忽略大小写

- **返回**

  - [Rule](#Rule)

## _class_ `KeywordsRule(*keywords)` {#KeywordsRule}

- **说明:** 检查消息纯文本是否包含指定关键字。

- **参数**

  - `*keywords` (str): 指定关键字元组

## _def_ `keyword(*keywords)` {#keyword}

- **说明:** 匹配消息纯文本关键词。

- **参数**

  - `*keywords` (str): 指定关键字元组

- **返回**

  - [Rule](#Rule)

## _class_ `CommandRule(cmds, force_whitespace=None)` {#CommandRule}

- **说明:** 检查消息是否为指定命令。

- **参数**

  - `cmds` (list[tuple[str, ...]]): 指定命令元组列表

  - `force_whitespace` (str | bool | None): 是否强制命令后必须有指定空白符

## _def_ `command(*cmds, force_whitespace=None)` {#command}

- **说明**

  匹配消息命令。

  根据配置里提供的 [`command_start`](config.md#Config-command-start),
  [`command_sep`](config.md#Config-command-sep) 判断消息是否为命令。

  可以通过 [Command](params.md#Command) 获取匹配成功的命令（例: `("test",)`），
  通过 [RawCommand](params.md#RawCommand) 获取匹配成功的原始命令文本（例: `"/test"`），
  通过 [CommandArg](params.md#CommandArg) 获取匹配成功的命令参数。

- **参数**

  - `*cmds` (str | tuple[str, ...]): 命令文本或命令元组

  - `force_whitespace` (str | bool | None): 是否强制命令后必须有指定空白符

- **返回**

  - [Rule](#Rule)

- **用法**

  使用默认 `command_start`, `command_sep` 配置情况下：

  命令 `("test",)` 可以匹配: `/test` 开头的消息
  命令 `("test", "sub")` 可以匹配: `/test.sub` 开头的消息

:::tip 提示
命令内容与后续消息间无需空格!
:::

## _class_ `ArgumentParser(<auto>)` {#ArgumentParser}

- **说明**

  `shell_like` 命令参数解析器，解析出错时不会退出程序。

  支持 [Message](adapters/index.md#Message) 富文本解析。

- **参数**

  auto

- **用法**

  用法与 `argparse.ArgumentParser` 相同，
  参考文档: [argparse](https://docs.python.org/3/library/argparse.html)

### _method_ `parse_known_args(args=None, namespace=None)` {#ArgumentParser-parse-known-args}

- **重载**

  **1.** `(args=None, namespace=None) -> tuple[Namespace, list[str | MessageSegment]]`

  - **参数**

    - `args` (Sequence[str | [MessageSegment](adapters/index.md#MessageSegment)] | None)

    - `namespace` (None)

  - **返回**

    - tuple[Namespace, list[str | [MessageSegment](adapters/index.md#MessageSegment)]]

  **2.** `(args, namespace) -> tuple[T, list[str | MessageSegment]]`

  - **参数**

    - `args` (Sequence[str | [MessageSegment](adapters/index.md#MessageSegment)] | None)

    - `namespace` (T)

  - **返回**

    - tuple[T, list[str | [MessageSegment](adapters/index.md#MessageSegment)]]

  **3.** `(*, namespace) -> tuple[T, list[str | MessageSegment]]`

  - **参数**

    - `namespace` (T)

  - **返回**

    - tuple[T, list[str | [MessageSegment](adapters/index.md#MessageSegment)]]

## _class_ `ShellCommandRule(cmds, parser)` {#ShellCommandRule}

- **说明:** 检查消息是否为指定 shell 命令。

- **参数**

  - `cmds` (list[tuple[str, ...]]): 指定命令元组列表

  - `parser` (ArgumentParser | None): 可选参数解析器

## _def_ `shell_command(*cmds, parser=None)` {#shell-command}

- **说明**

  匹配 `shell_like` 形式的消息命令。

  根据配置里提供的 [`command_start`](config.md#Config-command-start),
  [`command_sep`](config.md#Config-command-sep) 判断消息是否为命令。

  可以通过 [Command](params.md#Command) 获取匹配成功的命令
  （例: `("test",)`），
  通过 [RawCommand](params.md#RawCommand) 获取匹配成功的原始命令文本
  （例: `"/test"`），
  通过 [ShellCommandArgv](params.md#ShellCommandArgv) 获取解析前的参数列表
  （例: `["arg", "-h"]`），
  通过 [ShellCommandArgs](params.md#ShellCommandArgs) 获取解析后的参数字典
  （例: `{"arg": "arg", "h": True}`）。

  :::caution 警告
  如果参数解析失败，则通过 [ShellCommandArgs](params.md#ShellCommandArgs)
  获取的将是 [ParserExit](exception.md#ParserExit) 异常。
  :::

- **参数**

  - `*cmds` (str | tuple[str, ...]): 命令文本或命令元组

  - `parser` (ArgumentParser | None): [ArgumentParser](#ArgumentParser) 对象

- **返回**

  - [Rule](#Rule)

- **用法**

  使用默认 `command_start`, `command_sep` 配置，更多示例参考
  [argparse](https://docs.python.org/3/library/argparse.html) 标准库文档。

  ```python
  from nonebot.rule import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("-a", action="store_true")

  rule = shell_command("ls", parser=parser)
  ```

:::tip 提示
命令内容与后续消息间无需空格!
:::

## _class_ `RegexRule(regex, flags=0)` {#RegexRule}

- **说明:** 检查消息字符串是否符合指定正则表达式。

- **参数**

  - `regex` (str): 正则表达式

  - `flags` (int): 正则表达式标记

## _def_ `regex(regex, flags=0)` {#regex}

- **说明**

  匹配符合正则表达式的消息字符串。

  可以通过 [RegexStr](params.md#RegexStr) 获取匹配成功的字符串，
  通过 [RegexGroup](params.md#RegexGroup) 获取匹配成功的 group 元组，
  通过 [RegexDict](params.md#RegexDict) 获取匹配成功的 group 字典。

- **参数**

  - `regex` (str): 正则表达式

  - `flags` (int | re.RegexFlag): 正则表达式标记

- **返回**

  - [Rule](#Rule)

:::tip 提示
正则表达式匹配使用 search 而非 match，如需从头匹配请使用 `r"^xxx"` 来确保匹配开头
:::
:::tip 提示
正则表达式匹配使用 `EventMessage` 的 `str` 字符串，
而非 `EventMessage` 的 `PlainText` 纯文本字符串
:::

## _class_ `ToMeRule(<auto>)` {#ToMeRule}

- **说明:** 检查事件是否与机器人有关。

- **参数**

  auto

## _def_ `to_me()` {#to-me}

- **说明:** 匹配与机器人有关的事件。

- **参数**

  empty

- **返回**

  - [Rule](#Rule)

## _class_ `IsTypeRule(*types)` {#IsTypeRule}

- **说明:** 检查事件类型是否为指定类型。

- **参数**

  - `*types` (type[[Event](adapters/index.md#Event)])

## _def_ `is_type(*types)` {#is-type}

- **说明:** 匹配事件类型。

- **参数**

  - `*types` (type[[Event](adapters/index.md#Event)]): 事件类型

- **返回**

  - [Rule](#Rule)
