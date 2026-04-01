---
sidebar_position: 3
description: 会话状态信息

options:
  menu:
    - category: appendices
      weight: 40
---

# 会话状态

在事件处理流程中，和用户交互的过程即是会话。在会话中，我们可能需要记录一些信息，例如用户的重试次数等等，以便在会话中的不同阶段进行判断和处理。这些信息都可以存储于会话状态中。

NoneBot 中的会话状态是一个字典，可以通过类型 `T_State` 来获取。字典内可以存储任意类型的数据，但是要注意的是，NoneBot 本身会在会话状态中存储一些信息，因此不要使用 [NoneBot 使用的键名](../api/consts.md)。

```python
from nonebot.typing import T_State

@matcher.got("key", prompt="请输入密码")
async def _(state: T_State, key: str = ArgPlainText()):
    if key != "some password":
        try_count = state.get("try_count", 1)
        if try_count >= 3:
            await matcher.finish("密码错误次数过多")
        else:
            state["try_count"] = try_count + 1
            await matcher.reject("密码错误，请重新输入")
    await matcher.finish("密码正确")
```

会话状态的生命周期与事件处理流程相同，在期间的任何一个事件处理函数都可以进行读写。

```python
from nonebot.typing import T_State

@matcher.handle()
async def _(state: T_State):
    state["key"] = "value"

@matcher.handle()
async def _(state: T_State):
    await matcher.finish(state["key"])
```

会话状态还可以用于发送动态消息，消息模板在发送时会使用会话状态字典进行渲染。消息模板的使用方法已经在[消息处理](../tutorial/message.md#使用消息模板)中介绍过，这里不再赘述。

```python
from nonebot.typing import T_State
from nonebot.adapters import MessageTemplate

@matcher.handle()
async def _(state: T_State):
    state["username"] = "user"

@matcher.got("password", prompt=MessageTemplate("请输入 {username} 的密码"))
async def _():
    await matcher.finish(MessageTemplate("密码为 {password}"))
```
