---
sidebar_position: 2
description: nonebot.plugin.on 模块
---

# nonebot.plugin.on

本模块定义事件响应器便携定义函数。

## _def_ `on(type='', rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on}

- **说明**

  注册一个基础事件响应器，可自定义类型。

- **参数**

  - `type` (str): 事件响应器类型

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_metaevent(rule=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_metaevent}

- **说明**

  注册一个元事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_message(rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_message}

- **说明**

  注册一个消息事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_notice(rule=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_notice}

- **说明**

  注册一个通知事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_request(rule=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_request}

- **说明**

  注册一个请求事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_startswith(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_startswith}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_endswith(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_endswith}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息结尾内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_fullmatch(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_fullmatch}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息全匹配内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_keyword(keywords, rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_keyword}

- **说明**

  注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

- **参数**

  - `keywords` (set[str]): 关键词列表

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_command(cmd, rule=..., aliases=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_command}

- **说明**

  注册一个消息事件响应器，并且当消息以指定命令开头时响应。

  命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`\_

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_shell_command(cmd, rule=..., aliases=..., parser=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_shell_command}

- **说明**

  注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

  与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

  并将用户输入的原始参数列表保存在 `state["argv"]`, `parser` 处理的参数保存在 `state["args"]` 中

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_regex(pattern, flags=..., rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_regex}

- **说明**

  注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

  命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`\_

- **参数**

  - `pattern` (str): 正则表达式

  - `flags` (int | re.RegexFlag): 正则匹配标志

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _def_ `on_type(types, rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on_type}

- **说明**

  注册一个事件响应器，并且当事件为指定类型时响应。

- **参数**

  - `types` (Type[nonebot.internal.adapter.event.Event] | tuple[Type[nonebot.internal.adapter.event.Event]]): 事件类型

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _class_ `CommandGroup(cmd, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup}

- **参数**

  - `cmd` (str | tuple[str, ...])

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType)

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType)

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None)

  - `temp` (bool)

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType)

  - `priority` (int)

  - `block` (bool)

  - `state` (dict[Any, Any] | None)

### _method_ `command(self, cmd, *, rule=..., aliases=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup-command}

- **说明**

  注册一个新的命令。新参数将会覆盖命令组默认值

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `shell_command(self, cmd, *, rule=..., aliases=..., parser=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup-shell_command}

- **说明**

  注册一个新的 `shell_like` 命令。新参数将会覆盖命令组默认值

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

## _class_ `MatcherGroup(*, type=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup}

- **参数**

  - `type` (str)

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType)

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType)

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None)

  - `temp` (bool)

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType)

  - `priority` (int)

  - `block` (bool)

  - `state` (dict[Any, Any] | None)

### _method_ `on(self, *, type=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on}

- **说明**

  注册一个基础事件响应器，可自定义类型。

- **参数**

  - `type` (str): 事件响应器类型

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_command(self, cmd, aliases=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_command}

- **说明**

  注册一个消息事件响应器，并且当消息以指定命令开头时响应。

  命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`\_

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_endswith(self, msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_endswith}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息结尾内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_fullmatch(self, msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_fullmatch}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息全匹配内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_keyword(self, keywords, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_keyword}

- **说明**

  注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

- **参数**

  - `keywords` (set[str]): 关键词列表

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_message(self, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_message}

- **说明**

  注册一个消息事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_metaevent(self, *, rule=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_metaevent}

- **说明**

  注册一个元事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_notice(self, *, rule=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_notice}

- **说明**

  注册一个通知事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_regex(self, pattern, flags=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_regex}

- **说明**

  注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

  命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`\_

- **参数**

  - `pattern` (str): 正则表达式

  - `flags` (int | re.RegexFlag): 正则匹配标志

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_request(self, *, rule=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_request}

- **说明**

  注册一个请求事件响应器。

- **参数**

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_shell_command(self, cmd, aliases=..., parser=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_shell_command}

- **说明**

  注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

  与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

  并将用户输入的原始参数列表保存在 `state["argv"]`, `parser` 处理的参数保存在 `state["args"]` 中

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_startswith(self, msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_startswith}

- **说明**

  注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]

### _method_ `on_type(self, types, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on_type}

- **说明**

  注册一个事件响应器，并且当事件为指定类型时响应。

- **参数**

  - `types` (Type[nonebot.internal.adapter.event.Event] | tuple[Type[nonebot.internal.adapter.event.Event]]): 事件类型

  - `rule` (nonebot.internal.rule.Rule | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应规则

  - `permission` (nonebot.internal.permission.Permission | (*Any, \*\*Any) -> bool | (*Any, \*\*Any) -> Awaitable[bool] | NoneType): 事件响应权限

  - `handlers` (list[(*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any] | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime.datetime | datetime.timedelta | NoneType): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` (dict[Any, Any] | None): 默认 state

- **返回**

  - Type[nonebot.internal.matcher.Matcher]
