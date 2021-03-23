# 钩子函数

[`钩子编程`](https://zh.wikipedia.org/wiki/%E9%92%A9%E5%AD%90%E7%BC%96%E7%A8%8B)

> 钩子编程（hooking），也称作“挂钩”，是计算机程序设计术语，指通过拦截软件模块间的函数调用、消息传递、事件传递来修改或扩展操作系统、应用程序或其他软件组件的行为的各种技术。处理被拦截的函数调用、事件、消息的代码，被称为钩子（hook）。

在 `nonebot2` 中有一系列预定义的钩子函数，这些函数位于 [`nonebot.message`](https://v2.nonebot.dev/api/message.html) 模块下，我们可以以装饰器的形式利用这些函数，进行以下四种操作：

:::warning 注意
1.在钩子函数中，与 `matcher` 运行状态相关的函数将不可用，如 `matcher.finish()`

2.如果需要在钩子函数中打断整个对话的执行，请参考以下范例：
```python
from nonebot.exception import IgnoredException


@event_preprocessor
async def do_something(bot: Bot, event: Event, state: T_State):
    raise IgnoredException("reason")
```
:::

## 事件预处理

```python
from nonebot.message import event_preprocessor

@event_preprocessor
async def do_something(bot: Bot, event: Event, state: T_State):
    pass
```

## 事件后处理

```python
from nonebot.message import event_postprocessor

@event_postprocessor
async def do_something(bot: Bot, event: Event, state: T_State):
    pass
```

## 运行预处理

```python
from nonebot.message import run_preprocessor

@run_preprocessor
async def do_something(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    pass
```

## 运行后处理
```python
from nonebot.message import run_postprocessor

@run_postprocessor
async def do_something(matcher: Matcher, exception: Optional[Exception], bot: Bot, event: Event, state: T_State):
    pass
```