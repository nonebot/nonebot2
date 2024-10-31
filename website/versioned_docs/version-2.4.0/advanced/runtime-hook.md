---
sidebar_position: 8
description: 在特定的生命周期中执行代码

options:
  menu:
    - category: advanced
      weight: 90
---

# 钩子函数

> [钩子编程](https://zh.wikipedia.org/wiki/%E9%92%A9%E5%AD%90%E7%BC%96%E7%A8%8B)（hooking），也称作“挂钩”，是计算机程序设计术语，指通过拦截软件模块间的函数调用、消息传递、事件传递来修改或扩展操作系统、应用程序或其他软件组件的行为的各种技术。处理被拦截的函数调用、事件、消息的代码，被称为钩子（hook）。

在 NoneBot 中有一系列预定义的钩子函数，可以分为两类：**全局钩子函数**和**事件处理钩子函数**，这些钩子函数可以用装饰器的形式来使用。

## 全局钩子函数

全局钩子函数是指 NoneBot 针对其本身运行过程的钩子函数。

这些钩子函数是由驱动器来运行的，故需要先[获得全局驱动器](./driver.md#获取驱动器)。

### 启动准备

这个钩子函数会在 NoneBot 启动时运行。很多时候，我们并不希望在模块被导入时就执行一些耗时操作，如：连接数据库，这时候我们可以在这个钩子函数中进行这些操作。

```python
from nonebot import get_driver

driver = get_driver()

@driver.on_startup
async def do_something():
    pass
```

### 终止处理

这个钩子函数会在 NoneBot 终止时运行。我们可以在这个钩子函数中进行一些清理工作，如：关闭数据库连接。

```python
from nonebot import get_driver

driver = get_driver()

@driver.on_shutdown
async def do_something():
    pass
```

### Bot 连接处理

这个钩子函数会在任何协议适配器连接 `Bot` 对象至 NoneBot 时运行。支持依赖注入，可以直接注入 `Bot` 对象。

```python
from nonebot import get_driver

driver = get_driver()

@driver.on_bot_connect
async def do_something(bot: Bot):
    pass
```

### Bot 断开处理

这个钩子函数会在 `Bot` 断开与 NoneBot 的连接时运行。支持依赖注入，可以直接注入 `Bot` 对象。

```python
from nonebot import get_driver

driver = get_driver()

@driver.on_bot_disconnect
async def do_something(bot: Bot):
    pass
```

## 事件处理钩子函数

这些钩子函数指的是影响 NoneBot 进行**事件处理**的函数, 这些函数可以跟普通的事件处理函数一样接受相应的参数。

### 事件预处理

这个钩子函数会在 NoneBot 接收到新的事件时运行。支持依赖注入，可以注入 `Bot` 对象、事件、会话状态。在这个钩子函数内抛出 `nonebot.exception.IgnoredException` 会使 NoneBot 忽略该事件。

```python
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor

@event_preprocessor
async def do_something(event: Event):
    if not event.is_tome():
        raise IgnoredException("some reason")
```

### 事件后处理

这个钩子函数会在 NoneBot 处理事件完成后运行。支持依赖注入，可以注入 `Bot` 对象、事件、会话状态。

```python
from nonebot.message import event_postprocessor

@event_postprocessor
async def do_something(event: Event):
    pass
```

### 运行预处理

这个钩子函数会在 NoneBot 运行事件响应器前运行。支持依赖注入，可以注入 `Bot` 对象、事件、事件响应器、会话状态。在这个钩子函数内抛出 `nonebot.exception.IgnoredException` 也会使 NoneBot 忽略本次运行。

```python
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

@run_preprocessor
async def do_something(event: Event, matcher: Matcher):
    if not event.is_tome():
        raise IgnoredException("some reason")
```

### 运行后处理

这个钩子函数会在 NoneBot 运行事件响应器后运行。支持依赖注入，可以注入 `Bot` 对象、事件、事件响应器、会话状态、运行中产生的异常。

```python
from nonebot.message import run_postprocessor

@run_postprocessor
async def do_something(event: Event, matcher: Matcher, exception: Optional[Exception]):
    pass
```

### 平台接口调用钩子

这个钩子函数会在 `Bot` 对象调用平台接口时运行。在这个钩子函数中，我们可以通过引起 `MockApiException` 异常来阻止 `Bot` 对象调用平台接口并返回指定的结果。

```python
from nonebot.adapters import Bot
from nonebot.exception import MockApiException

@Bot.on_calling_api
async def handle_api_call(bot: Bot, api: str, data: Dict[str, Any]):
    if api == "send_msg":
        raise MockApiException(result={"message_id": 123})
```

### 平台接口调用后钩子

这个钩子函数会在 `Bot` 对象调用平台接口后运行。在这个钩子函数中，我们可以通过引起 `MockApiException` 异常来忽略平台接口返回的结果并返回指定的结果。

```python
from nonebot.adapters import Bot
from nonebot.exception import MockApiException

@Bot.on_called_api
async def handle_api_result(
    bot: Bot, exception: Optional[Exception], api: str, data: Dict[str, Any], result: Any
):
    if not exception and api == "send_msg":
        raise MockApiException(result={**result, "message_id": 123})
```
