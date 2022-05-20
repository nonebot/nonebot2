---
options:
  menu:
    weight: 40
    category: advanced
---

# 钩子函数

[钩子编程](https://zh.wikipedia.org/wiki/%E9%92%A9%E5%AD%90%E7%BC%96%E7%A8%8B)

> 钩子编程（hooking），也称作“挂钩”，是计算机程序设计术语，指通过拦截软件模块间的函数调用、消息传递、事件传递来修改或扩展操作系统、应用程序或其他软件组件的行为的各种技术。处理被拦截的函数调用、事件、消息的代码，被称为钩子（hook）。

在 NoneBot2 中有一系列预定义的钩子函数，分为两类：**全局钩子函数**和**事件钩子函数**，这些钩子函数可以用装饰器的形式来使用。

## 全局钩子函数

全局钩子函数是指 NoneBot2 针对其本身运行过程的钩子函数。

这些钩子函数是由其后端驱动 `Driver` 来运行的，故需要先获得全局 `Driver` 对象：

```python
from nonebot import get_driver


driver=get_driver()
```

共分为六种函数：

### 启动准备

这个钩子函数会在 NoneBot2 启动时运行。

```python
@driver.on_startup
async def do_something():
    pass
```

### 终止处理

这个钩子函数会在 NoneBot2 终止时运行。

```python
@driver.on_shutdown
async def do_something():
    pass
```

### Bot 连接处理

这个钩子函数会在 `Bot` 通过 websocket 连接到 NoneBot2 时运行。

```python
@driver.on_bot_connect
async def do_something(bot: Bot):
    pass
```

### bot 断开处理

这个钩子函数会在 `Bot` 断开与 NoneBot2 的 websocket 连接时运行。

```python
@driver.on_bot_disconnect
async def do_something(bot: Bot):
    pass
```

### bot api 调用钩子

这个钩子函数会在 `Bot` 调用 API 时运行。

```python
from nonebot.adapters import Bot

@Bot.on_calling_api
async def handle_api_call(bot: Bot, api: str, data: Dict[str, Any]):
    pass
```

### bot api 调用后钩子

这个钩子函数会在 `Bot` 调用 API 后运行。

```python
from nonebot.adapters import Bot

@Bot.on_called_api
async def handle_api_result(bot: Bot, exception: Optional[Exception], api: str, data: Dict[str, Any], result: Any):
    pass
```

## 事件钩子函数

这些钩子函数指的是影响 NoneBot2 进行**事件处理**的函数, 这些函数可以认为跟普通的事件处理函数一样，接受相应的参数。

:::tip 提示
关于**事件处理**的流程，可以在[这里](./README.md)查阅。
:::

:::warning

1.在事件处理钩子函数中，与 `matcher` 运行状态相关的函数将不可用，如 `matcher.finish()`

2.如果需要在事件处理钩子函数中打断整个对话的执行，请参考以下范例：

```python
from nonebot.exception import IgnoredException


@event_preprocessor
async def do_something():
    raise IgnoredException("reason")
```

:::

共分为四种函数：

### 事件预处理

这个钩子函数会在 `Event` 上报到 NoneBot2 时运行

```python
from nonebot.message import event_preprocessor

@event_preprocessor
async def do_something():
    pass
```

### 事件后处理

这个钩子函数会在 NoneBot2 处理 `Event` 后运行

```python
from nonebot.message import event_postprocessor

@event_postprocessor
async def do_something():
    pass
```

### 运行预处理

这个钩子函数会在 NoneBot2 运行 `matcher` 前运行。

```python
from nonebot.message import run_preprocessor

@run_preprocessor
async def do_something():
    pass
```

### 运行后处理

这个钩子函数会在 NoneBot2 运行 `matcher` 后运行。

```python
from nonebot.message import run_postprocessor

@run_postprocessor
async def do_something():
    pass
```
