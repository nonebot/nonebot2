---
sidebar_position: 2
description: nonebot.message 模块
---

# nonebot.message

本模块定义了事件处理主要流程。

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。

## _def_ `event_preprocessor(func)` {#event_preprocessor}

- **说明**

  事件预处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。

- **参数**

  - `func` ((*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any])

- **返回**

  - (\*Any, \*\*Any) -> Any | (\*Any, \*\*Any) -> Awaitable[Any]

## _def_ `event_postprocessor(func)` {#event_postprocessor}

- **说明**

  事件后处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。

- **参数**

  - `func` ((*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any])

- **返回**

  - (\*Any, \*\*Any) -> Any | (\*Any, \*\*Any) -> Awaitable[Any]

## _def_ `run_preprocessor(func)` {#run_preprocessor}

- **说明**

  运行预处理。装饰一个函数，使它在每次事件响应器运行前执行。

- **参数**

  - `func` ((*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any])

- **返回**

  - (\*Any, \*\*Any) -> Any | (\*Any, \*\*Any) -> Awaitable[Any]

## _def_ `run_postprocessor(func)` {#run_postprocessor}

- **说明**

  运行后处理。装饰一个函数，使它在每次事件响应器运行后执行。

- **参数**

  - `func` ((*Any, \*\*Any) -> Any | (*Any, \*\*Any) -> Awaitable[Any])

- **返回**

  - (\*Any, \*\*Any) -> Any | (\*Any, \*\*Any) -> Awaitable[Any]

## _async def_ `handle_event(bot, event)` {#handle_event}

- **说明**

  处理一个事件。调用该函数以实现分发事件。

- **参数**

  - `bot` (Bot): Bot 对象

  - `event` (Event): Event 对象

- **返回**

  - None

- **用法**

  ```python
  import asyncio
  asyncio.create_task(handle_event(bot, event))
  ```
