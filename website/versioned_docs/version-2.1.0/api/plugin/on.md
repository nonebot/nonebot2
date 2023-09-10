---
sidebar_position: 2
description: nonebot.plugin.on 模块
---

# nonebot.plugin.on

本模块定义事件响应器便携定义函数。

## _def_ `store_matcher(matcher)` {#store-matcher}

- **说明:** 存储一个事件响应器到插件。

- **参数**

  - `matcher` (type[[Matcher](../matcher.md#Matcher)]): 事件响应器

- **返回**

  - None

## _def_ `get_matcher_plugin(depth=...)` {#get-matcher-plugin}

- **说明**

  获取事件响应器定义所在插件。

  **Deprecated**, 请使用 [get_matcher_source](#get-matcher-source) 获取信息。

- **参数**

  - `depth` (int): 调用栈深度

- **返回**

  - [Plugin](plugin.md#Plugin) | None

## _def_ `get_matcher_module(depth=...)` {#get-matcher-module}

- **说明**

  获取事件响应器定义所在模块。

  **Deprecated**, 请使用 [get_matcher_source](#get-matcher-source) 获取信息。

- **参数**

  - `depth` (int): 调用栈深度

- **返回**

  - ModuleType | None

## _def_ `get_matcher_source(depth=...)` {#get-matcher-source}

- **说明:** 获取事件响应器定义所在源码信息。

- **参数**

  - `depth` (int): 调用栈深度

- **返回**

  - MatcherSource | None

## _def_ `on(type="", rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on}

- **说明:** 注册一个基础事件响应器，可自定义类型。

- **参数**

  - `type` (str): 事件响应器类型

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_metaevent(rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-metaevent}

- **说明:** 注册一个元事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_message(rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-message}

- **说明:** 注册一个消息事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_notice(rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-notice}

- **说明:** 注册一个通知事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_request(rule=..., permission=..., *, handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-request}

- **说明:** 注册一个请求事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_startswith(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-startswith}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_endswith(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-endswith}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息结尾内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_fullmatch(msg, rule=..., ignorecase=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-fullmatch}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息全匹配内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `ignorecase` (bool): 是否忽略大小写

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_keyword(keywords, rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-keyword}

- **说明:** 注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

- **参数**

  - `keywords` (set[str]): 关键词列表

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_command(cmd, rule=..., aliases=..., force_whitespace=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-command}

- **说明**

  注册一个消息事件响应器，并且当消息以指定命令开头时响应。

  命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`\_

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `force_whitespace` (str | bool | None): 是否强制命令后必须有指定空白符

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_shell_command(cmd, rule=..., aliases=..., parser=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-shell-command}

- **说明**

  注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

  与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

  可以通过 [ShellCommandArgv](../params.md#ShellCommandArgv) 获取原始参数列表，
  通过 [ShellCommandArgs](../params.md#ShellCommandArgs) 获取解析后的参数字典。

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_regex(pattern, flags=..., rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-regex}

- **说明**

  注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

  命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`\_

- **参数**

  - `pattern` (str): 正则表达式

  - `flags` (int | re.RegexFlag): 正则匹配标志

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _def_ `on_type(types, rule=..., *, permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#on-type}

- **说明:** 注册一个事件响应器，并且当事件为指定类型时响应。

- **参数**

  - `types` (type[[Event](../adapters/index.md#Event)] | tuple[type[[Event](../adapters/index.md#Event)], ...]): 事件类型

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _class_ `CommandGroup(cmd, prefix_aliases=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup}

- **参数**

  - `cmd` (str | tuple[str, ...])

  - `prefix_aliases` (bool)

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None)

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None)

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None)

  - `temp` (bool)

  - `expire_time` (datetime | timedelta | None)

  - `priority` (int)

  - `block` (bool)

  - `state` ([T_State](../typing.md#T-State) | None)

### _method_ `command(cmd, *, rule=..., aliases=..., force_whitespace=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup-command}

- **说明:** 注册一个新的命令。新参数将会覆盖命令组默认值

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `force_whitespace` (str | bool | None): 是否强制命令后必须有指定空白符

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `shell_command(cmd, *, rule=..., aliases=..., parser=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#CommandGroup-shell-command}

- **说明:** 注册一个新的 `shell_like` 命令。新参数将会覆盖命令组默认值

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

## _class_ `MatcherGroup(*, type=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup}

- **参数**

  - `type` (str)

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None)

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None)

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None)

  - `temp` (bool)

  - `expire_time` (datetime | timedelta | None)

  - `priority` (int)

  - `block` (bool)

  - `state` ([T_State](../typing.md#T-State) | None)

### _method_ `on(*, type=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on}

- **说明:** 注册一个基础事件响应器，可自定义类型。

- **参数**

  - `type` (str): 事件响应器类型

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_metaevent(*, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-metaevent}

- **说明:** 注册一个元事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_message(*, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-message}

- **说明:** 注册一个消息事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_notice(*, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-notice}

- **说明:** 注册一个通知事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_request(*, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-request}

- **说明:** 注册一个请求事件响应器。

- **参数**

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_startswith(msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-startswith}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息开头内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_endswith(msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-endswith}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息结尾内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_fullmatch(msg, *, ignorecase=..., rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-fullmatch}

- **说明:** 注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

- **参数**

  - `msg` (str | tuple[str, ...]): 指定消息全匹配内容

  - `ignorecase` (bool): 是否忽略大小写

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_keyword(keywords, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-keyword}

- **说明:** 注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

- **参数**

  - `keywords` (set[str]): 关键词列表

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_command(cmd, aliases=..., force_whitespace=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-command}

- **说明**

  注册一个消息事件响应器，并且当消息以指定命令开头时响应。

  命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`\_

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `force_whitespace` (str | bool | None): 是否强制命令后必须有指定空白符

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_shell_command(cmd, aliases=..., parser=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-shell-command}

- **说明**

  注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

  与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

  可以通过 [ShellCommandArgv](../params.md#ShellCommandArgv) 获取原始参数列表，
  通过 [ShellCommandArgs](../params.md#ShellCommandArgs) 获取解析后的参数字典。

- **参数**

  - `cmd` (str | tuple[str, ...]): 指定命令内容

  - `aliases` (set[str | tuple[str, ...]] | None): 命令别名

  - `parser` ([ArgumentParser](../rule.md#ArgumentParser) | None): `nonebot.rule.ArgumentParser` 对象

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_regex(pattern, flags=..., *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-regex}

- **说明**

  注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

  命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`\_

- **参数**

  - `pattern` (str): 正则表达式

  - `flags` (int | re.RegexFlag): 正则匹配标志

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]

### _method_ `on_type(types, *, rule=..., permission=..., handlers=..., temp=..., expire_time=..., priority=..., block=..., state=...)` {#MatcherGroup-on-type}

- **说明:** 注册一个事件响应器，并且当事件为指定类型时响应。

- **参数**

  - `types` (type[[Event](../adapters/index.md#Event)] | tuple[type[[Event](../adapters/index.md#Event)]]): 事件类型

  - `rule` ([Rule](../rule.md#Rule) | [T_RuleChecker](../typing.md#T-RuleChecker) | None): 事件响应规则

  - `permission` ([Permission](../permission.md#Permission) | [T_PermissionChecker](../typing.md#T-PermissionChecker) | None): 事件响应权限

  - `handlers` (list[[T_Handler](../typing.md#T-Handler) | [Dependent](../dependencies/index.md#Dependent)] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器（仅执行一次）

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `priority` (int): 事件响应器优先级

  - `block` (bool): 是否阻止事件向更低优先级传递

  - `state` ([T_State](../typing.md#T-State) | None): 默认 state

- **返回**

  - type[[Matcher](../matcher.md#Matcher)]
