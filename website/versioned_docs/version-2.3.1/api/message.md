---
sidebar_position: 2
description: nonebot.message 模块
---

# nonebot.message

本模块定义了事件处理主要流程。

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。

## _def_ `event_preprocessor(func)` {#event-preprocessor}

- **说明**

  事件预处理。

  装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。

- **参数**

  - `func` ([T_EventPreProcessor](typing.md#T-EventPreProcessor))

- **返回**

  - [T_EventPreProcessor](typing.md#T-EventPreProcessor)

## _def_ `event_postprocessor(func)` {#event-postprocessor}

- **说明**

  事件后处理。

  装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。

- **参数**

  - `func` ([T_EventPostProcessor](typing.md#T-EventPostProcessor))

- **返回**

  - [T_EventPostProcessor](typing.md#T-EventPostProcessor)

## _def_ `run_preprocessor(func)` {#run-preprocessor}

- **说明**

  运行预处理。

  装饰一个函数，使它在每次事件响应器运行前执行。

- **参数**

  - `func` ([T_RunPreProcessor](typing.md#T-RunPreProcessor))

- **返回**

  - [T_RunPreProcessor](typing.md#T-RunPreProcessor)

## _def_ `run_postprocessor(func)` {#run-postprocessor}

- **说明**

  运行后处理。

  装饰一个函数，使它在每次事件响应器运行后执行。

- **参数**

  - `func` ([T_RunPostProcessor](typing.md#T-RunPostProcessor))

- **返回**

  - [T_RunPostProcessor](typing.md#T-RunPostProcessor)

## _async def_ `check_and_run_matcher(Matcher, bot, event, state, stack=None, dependency_cache=None)` {#check-and-run-matcher}

- **说明:** 检查并运行事件响应器。

- **参数**

  - `Matcher` (type[[Matcher](matcher.md#Matcher)]): 事件响应器

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): Event 对象

  - `state` ([T_State](typing.md#T-State)): 会话状态

  - `stack` (AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None): 依赖缓存

- **返回**

  - None

## _async def_ `handle_event(bot, event)` {#handle-event}

- **说明:** 处理一个事件。调用该函数以实现分发事件。

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): Event 对象

- **返回**

  - None

- **用法**

  ```python
  import asyncio
  asyncio.create_task(handle_event(bot, event))
  ```
