---
sidebar_position: 5
description: 使用事件响应器操作，改变事件处理流程

options:
  menu:
    weight: 28
    category: guide
---

# 事件响应器操作

在事件处理流程中，我们可以使用事件响应器操作来进行一些交互或改变事件处理流程。

## send

向用户回复一条消息。回复的方式或途径由协议适配器自行实现。

可以是 `str`, {ref}`nonebot.adapters._message.Message`, {ref}`nonebot.adapters._message.MessageSegment` 或 {ref}`nonebot.adapters._template.MessageTemplate`。

这个操作等同于使用 `bot.send(event, message, **kwargs)` 但不需要自行传入 `event`。

```python {3}
@matcher.handle()
async def _():
    await matcher.send("Hello world!")
```

## finish

向用户回复一条消息（可选），并立即结束当前事件的整个处理流程。

参数与 [`send`](#send) 相同。

```python {3}
@matcher.handle()
async def _():
    await matcher.finish("Hello world!")
    # something never run
    ...
```

## pause

向用户回复一条消息（可选），并立即当前事件处理依赖并等待接收一个新的事件后进入下一个事件处理依赖。

类似于 `receive` 的行为但可以根据事件来决定是否接收新的事件。

```python {4}
@matcher.handle()
async def _():
    if serious:
        await matcher.pause("Confirm?")

@matcher.handle()
async def _():
    ...
```

## reject

向用户回复一条消息（可选），并立即当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

通常用于拒绝当前 `receive` 接收的事件或 `got` 接收的参数（如：不符合格式或标准）。

```python {4}
@matcher.got("arg")
async def _(arg: str = ArgPlainText()):
    if not is_valid(arg):
        await matcher.reject("Invalid arg!")
```

## reject_arg

向用户回复一条消息（可选），并立即当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

用于拒绝指定 `got` 接收的参数，通常在嵌套装饰器时使用。

```python {4}
@matcher.got("a")
@matcher.got("b")
async def _(a: str = ArgPlainText(), b: str = ArgPlainText()):
    if a not in b:
        await matcher.reject_arg("a", "Invalid a!")
```

## reject_receive

向用户回复一条消息（可选），并立即当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

用于拒绝指定 `receive` 接收的事件，通常在嵌套装饰器时使用。

```python {4}
@matcher.receive("a")
@matcher.receive("b")
async def _(a: Event = Received("a"), b: Event = Received("b")):
    if a.get_user_id() != b.get_user_id():
        await matcher.reject_receive("a")
```

## skip

立即结束当前事件处理依赖，进入下一个事件处理依赖。

通常在子依赖中使用，用于跳过当前事件处理依赖的执行。

```python {2}
async def dependency(matcher: Matcher):
    matcher.skip()


@matcher.handle()
async def _(sub=Depends(dependency)):
    # never run
    ...
```

## get_receive

获取一个 `receive` 接收的事件。

## set_receive

设置/覆盖一个 `receive` 接收的事件。

## get_last_receive

获取最近一次 `receive` 接收的事件。

## get_arg

获取一个 `got` 接收的参数。

## set_arg

设置/覆盖一个 `got` 接收的参数。

## stop_propagation

阻止事件向更低优先级的事件响应器传播。

```python
@foo.handle()
async def _(matcher: Matcher):
    matcher.stop_propagation()
```
