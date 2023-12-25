---
sidebar_position: 6
description: nonebot.permission 模块
---

# nonebot.permission

本模块是 [Matcher.permission](matcher.md#Matcher-permission) 的类型定义。

每个[事件响应器](matcher.md#Matcher)
拥有一个 [Permission](#Permission)，其中是 `PermissionChecker` 的集合。
只要有一个 `PermissionChecker` 检查结果为 `True` 时就会继续运行。

## _def_ `USER(*users, perm=None)` {#USER}

- **说明**

  匹配当前事件属于指定会话。

  如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有检查函数的会话 ID 限制。

- **参数**

  - `*users` (str)

  - `perm` (Permission | None): 需要同时满足的权限

  - `user`: 会话白名单

- **返回**

  - untyped

## _class_ `User(users, perm=None)` {#User}

- **说明:** 检查当前事件是否属于指定会话。

- **参数**

  - `users` (tuple[str, ...]): 会话 ID 元组

  - `perm` (Permission | None): 需同时满足的权限

### _classmethod_ `from_event(event, perm=None)` {#User-from-event}

- **说明**

  从事件中获取会话 ID。

  如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有的会话 ID 限制。

- **参数**

  - `event` ([Event](adapters/index.md#Event)): Event 对象

  - `perm` (Permission | None): 需同时满足的权限

- **返回**

  - Self

### _classmethod_ `from_permission(*users, perm=None)` {#User-from-permission}

- **说明**

  指定会话与权限。

  如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有的会话 ID 限制。

- **参数**

  - `*users` (str): 会话白名单

  - `perm` (Permission | None): 需同时满足的权限

- **返回**

  - Self

## _class_ `Permission(*checkers)` {#Permission}

- **说明**

  权限类。

  当事件传递时，在 [Matcher](matcher.md#Matcher) 运行前进行检查。

- **参数**

  - `*checkers` ([T_PermissionChecker](typing.md#T-PermissionChecker) | [Dependent](dependencies/index.md#Dependent)[bool]): PermissionChecker

- **用法**

  ```python
  Permission(async_function) | sync_function
  # 等价于
  Permission(async_function, sync_function)
  ```

### _instance-var_ `checkers` {#Permission-checkers}

- **类型:** set[[Dependent](dependencies/index.md#Dependent)[bool]]

- **说明:** 存储 `PermissionChecker`

### _async method_ `__call__(bot, event, stack=None, dependency_cache=None)` {#Permission---call--}

- **说明:** 检查是否满足某个权限。

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): Event 对象

  - `stack` (AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None): 依赖缓存

- **返回**

  - bool

## _class_ `Message(<auto>)` {#Message}

- **说明:** 检查是否为消息事件

- **参数**

  auto

## _class_ `Notice(<auto>)` {#Notice}

- **说明:** 检查是否为通知事件

- **参数**

  auto

## _class_ `Request(<auto>)` {#Request}

- **说明:** 检查是否为请求事件

- **参数**

  auto

## _class_ `MetaEvent(<auto>)` {#MetaEvent}

- **说明:** 检查是否为元事件

- **参数**

  auto

## _var_ `MESSAGE` {#MESSAGE}

- **类型:** [Permission](#Permission)

- **说明**

  匹配任意 `message` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 message type 的 Matcher。

## _var_ `NOTICE` {#NOTICE}

- **类型:** [Permission](#Permission)

- **说明**

  匹配任意 `notice` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 notice type 的 Matcher。

## _var_ `REQUEST` {#REQUEST}

- **类型:** [Permission](#Permission)

- **说明**

  匹配任意 `request` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 request type 的 Matcher。

## _var_ `METAEVENT` {#METAEVENT}

- **类型:** [Permission](#Permission)

- **说明**

  匹配任意 `meta_event` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 meta_event type 的 Matcher。

## _class_ `SuperUser(<auto>)` {#SuperUser}

- **说明:** 检查当前事件是否是消息事件且属于超级管理员

- **参数**

  auto

## _var_ `SUPERUSER` {#SUPERUSER}

- **类型:** [Permission](#Permission)

- **说明:** 匹配任意超级用户事件
