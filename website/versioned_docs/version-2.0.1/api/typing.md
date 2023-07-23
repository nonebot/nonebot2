---
sidebar_position: 11
description: nonebot.typing 模块
---

# nonebot.typing

本模块定义了 NoneBot 模块中共享的一些类型。

使用 Python 的 Type Hint 语法，
参考 [`PEP 484`](https://www.python.org/dev/peps/pep-0484/),
[`PEP 526`](https://www.python.org/dev/peps/pep-0526/) 和
[`typing`](https://docs.python.org/3/library/typing.html)。

## _def_ `overrides(InterfaceClass)` {#overrides}

- **说明:** 标记一个方法为父类 interface 的 implement

- **参数**

  - `InterfaceClass` (object)

- **返回**

  - untyped

## _var_ `T_State` {#T-State}

- **类型:** dict[Any, Any]

- **说明:** 事件处理状态 State 类型

## _var_ `T_BotConnectionHook` {#T-BotConnectionHook}

- **类型:** \_DependentCallable[Any]

- **说明**

  Bot 连接建立时钩子函数

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_BotDisconnectionHook` {#T-BotDisconnectionHook}

- **类型:** \_DependentCallable[Any]

- **说明**

  Bot 连接断开时钩子函数

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_CallingAPIHook` {#T-CallingAPIHook}

- **类型:** ([Bot](adapters/index.md#Bot), str, dict[str, Any]) -> Awaitable[Any]

- **说明:** `bot.call_api` 钩子函数

## _var_ `T_CalledAPIHook` {#T-CalledAPIHook}

- **类型:** ([Bot](adapters/index.md#Bot), Exception | None, str, dict[str, Any], Any) -> Awaitable[Any]

- **说明:** `bot.call_api` 后执行的函数，参数分别为 bot, exception, api, data, result

## _var_ `T_EventPreProcessor` {#T-EventPreProcessor}

- **类型:** \_DependentCallable[Any]

- **说明**

  事件预处理函数 EventPreProcessor 类型

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_EventPostProcessor` {#T-EventPostProcessor}

- **类型:** \_DependentCallable[Any]

- **说明**

  事件预处理函数 EventPostProcessor 类型

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_RunPreProcessor` {#T-RunPreProcessor}

- **类型:** \_DependentCallable[Any]

- **说明**

  事件响应器运行前预处理函数 RunPreProcessor 类型

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - MatcherParam: Matcher 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_RunPostProcessor` {#T-RunPostProcessor}

- **类型:** \_DependentCallable[Any]

- **说明**

  事件响应器运行后后处理函数 RunPostProcessor 类型

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - MatcherParam: Matcher 对象
  - ExceptionParam: 异常对象（可能为 None）
  - DefaultParam: 带有默认值的参数

## _var_ `T_RuleChecker` {#T-RuleChecker}

- **类型:** \_DependentCallable[bool]

- **说明**

  RuleChecker 即判断是否响应事件的处理函数。

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_PermissionChecker` {#T-PermissionChecker}

- **类型:** \_DependentCallable[bool]

- **说明**

  PermissionChecker 即判断事件是否满足权限的处理函数。

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_Handler` {#T-Handler}

- **类型:** \_DependentCallable[Any]

- **说明:** Handler 处理函数。

## _var_ `T_TypeUpdater` {#T-TypeUpdater}

- **类型:** \_DependentCallable[str]

- **说明**

  TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。 默认会更新为 `message`。

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - MatcherParam: Matcher 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_PermissionUpdater` {#T-PermissionUpdater}

- **类型:** \_DependentCallable[[Permission](permission.md#Permission)]

- **说明**

  PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。 默认会更新为当前事件的触发对象。

  依赖参数:

  - DependParam: 子依赖参数
  - BotParam: Bot 对象
  - EventParam: Event 对象
  - StateParam: State 对象
  - MatcherParam: Matcher 对象
  - DefaultParam: 带有默认值的参数

## _var_ `T_DependencyCache` {#T-DependencyCache}

- **类型:** dict[\_DependentCallable[Any], Task[Any]]

- **说明:** 依赖缓存, 用于存储依赖函数的返回值
