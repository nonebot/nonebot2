---
sidebar_position: 6
description: nonebot.permission 模块
---

# nonebot.permission

本模块是 [Matcher.permission](./matcher.md#Matcher-permission) 的类型定义。

每个 [Matcher](./matcher.md#Matcher) 拥有一个 [Permission](#Permission) ，
其中是 `PermissionChecker` 的集合，只要有一个 `PermissionChecker` 检查结果为 `True` 时就会继续运行。

## _var_ `MESSAGE` {#MESSAGE}

- **类型:** nonebot.internal.permission.Permission

- **说明**

  匹配任意 `message` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 message type 的 Matcher。

## _var_ `NOTICE` {#NOTICE}

- **类型:** nonebot.internal.permission.Permission

- **说明**

  匹配任意 `notice` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 notice type 的 Matcher。

## _var_ `REQUEST` {#REQUEST}

- **类型:** nonebot.internal.permission.Permission

- **说明**

  匹配任意 `request` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 request type 的 Matcher。

## _var_ `METAEVENT` {#METAEVENT}

- **类型:** nonebot.internal.permission.Permission

- **说明**

  匹配任意 `meta_event` 类型事件

  仅在需要同时捕获不同类型事件时使用，优先使用 meta_event type 的 Matcher。

## _var_ `SUPERUSER` {#SUPERUSER}

- **类型:** nonebot.internal.permission.Permission

- **说明:** 匹配任意超级用户消息类型事件

## _def_ `USER(*users, perm=None)` {#USER}

- **说明**

  匹配当前事件属于指定会话

- **参数**

  - `*users` (str)

  - `perm` (nonebot.internal.permission.Permission | None): 需要同时满足的权限

  - `user`: 会话白名单

- **返回**

  - Unknown

## _class_ `User(users, perm=None)` {#User}

- **说明**

  检查当前事件是否属于指定会话

- **参数**

  - `users` (tuple[str, ...]): 会话 ID 元组

  - `perm` (nonebot.internal.permission.Permission | None): 需同时满足的权限

## _class_ `Permission(*checkers)` {#Permission}

- **说明**

  [Matcher](./matcher.md#Matcher) 权限类。

  当事件传递时，在 [Matcher](./matcher.md#Matcher) 运行前进行检查。

- **参数**

  - `*checkers` ((\*Any, \*\*Any) -> bool | Awaitable[bool] | [Dependent](./dependencies/index.md#Dependent)[bool]): PermissionChecker

- **用法**

  ```python
  Permission(async_function) | sync_function
  # 等价于
  Permission(async_function, sync_function)
  ```

### _async method_ `__call__(self, bot, event, stack=None, dependency_cache=None)` {#Permission-**call**}

- **说明**

  检查是否满足某个权限

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot): Bot 对象

  - `event` (nonebot.internal.adapter.event.Event): Event 对象

  - `stack` (contextlib.AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` (dict[(\*Any, \*\*Any) -> Any, Task[Any]] | None): 依赖缓存

- **返回**

  - bool

## _class_ `Message()` {#Message}

- **说明**

  检查是否为消息事件

## _class_ `Notice()` {#Notice}

- **说明**

  检查是否为通知事件

## _class_ `Request()` {#Request}

- **说明**

  检查是否为请求事件

## _class_ `MetaEvent()` {#MetaEvent}

- **说明**

  检查是否为元事件

## _class_ `SuperUser()` {#SuperUser}

- **说明**

  检查当前事件是否是消息事件且属于超级管理员
