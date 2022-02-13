---
sidebar_position: 1
description: 依赖注入简介

options:
  menu:
    weight: 60
    category: advanced
---

# 简介

受 [FastAPI](https://fastapi.tiangolo.com/tutorial/dependencies/) 启发，NoneBot 同样编写了一个简易的依赖注入模块，使得开发者可以通过事件处理函数参数的类型标注来自动注入依赖。

## 什么是依赖注入？

[依赖注入](https://zh.wikipedia.org/wiki/%E4%BE%9D%E8%B5%96%E6%B3%A8%E5%85%A5)

> 在软件工程中，**依赖注入**（dependency injection）的意思为，给予调用方它所需要的事物。 “依赖”是指可被方法调用的事物。依赖注入形式下，调用方不再直接使用“依赖”，取而代之是“注入” 。“注入”是指将“依赖”传递给调用方的过程。在“注入”之后，调用方才会调用该“依赖。 传递依赖给调用方，而不是让让调用方直接获得依赖，这个是该设计的根本需求。

依赖注入往往起到了分离依赖和调用方的作用，这样一方面能让代码更为整洁可读，一方面可以提升代码的复用性。

## 使用依赖注入

以下通过一个简单的例子来说明依赖注入的使用方法：

```python
from nonebot.log import logger
from nonebot.params import Depends # 1.引用 Depends
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import MessageEvent

test = on_command("123")

async def depend(event: MessageEvent): # 2.编写依赖函数
    return {"uid": event.get_user_id(), "nickname": event.sender.nickname}

@test.handle()
async def _(x: dict = Depends(depend)): # 3.在事件处理函数里声明依赖项
    print(x["uid"], x["nickname"])
```

如注释所言，可以用三步来说明依赖注入的使用过程：

1. 引用 `Depends` 。

2. 编写依赖函数。依赖函数和普通的事件处理函数并无区别，同样可以接收 `bot`, `event`, `state` 等参数，你可以把它当作一个普通的事件处理函数，但是去除了装饰器（没有使用 `matcher.handle()` 等来装饰），并且可以返回任何类型的值。

   在这里我们接受了 `event`，并以 `onebot` 的 `MessageEvent` 作为类型标注，返回一个新的字典，包括 `uid` 和 `nickname` 两个键值。

3. 在事件处理函数中声明依赖项。依赖项必须要 `Depends` 包裹依赖函数作为默认值。

:::tip
一般来说，参数 `x` 的类型标注并不会影响事件处理函数的运行，类型检查并不会对依赖函数的返回值以及类型标注进行检查。
:::

虽然声明依赖项的方式和其他参数如 `bot`, `event` 并无二样，但他的参数有一些限制，必须是**可调用对象**，函数自然是可调用对象，类和生成器也是，我们会在接下来的小节说明。

一般来说，当接收到事件时，`NoneBot2` 会进行以下处理：

1. 准备依赖函数所需要的参数。
2. 调用依赖函数并获得返回值。
3. 将返回值作为事件处理函数中的参数值传入。

## 依赖缓存

在使用 `Depends` 包裹依赖函数时，有一个参数 `use_cache` ，它默认为 `True` ，这个参数会决定 `Nonebot2` 在依赖注入的处理中是否使用缓存。

当使用缓存时，依赖注入会这样处理：

1. 查询缓存，如果缓存中有相应的值，则直接返回。
2. 准备依赖函数所需要的参数。
3. 调用依赖函数并获得返回值。
4. 将返回值存入缓存。
5. 将返回值作为事件处理函数中的参数值传入。

## 同步支持

我们在编写依赖函数时，可以简单地用同步函数，`NoneBot2` 的内部流程会进行处理：

```python
from nonebot.log import logger
from nonebot.params import Depends # 1.引用 Depends
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import MessageEvent

test = on_command("123")

def depend(event: MessageEvent): # 2.编写同步依赖函数
    return {"uid": event.get_user_id(), "nickname": event.sender.nickname}

@test.handle()
async def _(x: dict = Depends(depend)): # 3.在事件处理函数里声明依赖项
    print(x["uid"], x["nickname"])
```

## Class 作为依赖

我们可以看下面的代码段：

```python
class A():
    def __init__(self):
        pass
a = A()
```

在我们实例化类 `A` 的时候，其实我们就在**调用**它，类本身也是一个**可调用对象**，所以类可以被 `Depends` 包裹成为依赖项。

因此我们对第一节的代码段做一下改造：

```python
from nonebot.log import logger
from nonebot.params import Depends # 1.引用 Depends
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent

test = on_command("123")

class DependClass: # 2.编写依赖类
    def __init__(self, event: MessageEvent):
    	self.uid = event.get_user_id()
    	self.nickname = event.sender.nickname

@test.handle()
async def _(x: DependClass = Depends(DependClass)): # 3.在事件处理函数里声明依赖项
    print(x.uid, x.nickname)
```

依然可以用三步说明如何用类作为依赖项：

1. 引用 `Depends` 。

2. 编写依赖类。类的 `__init__` 函数可以接收 `bot`, `event`, `state` 等参数，在这里我们接受了`event`，并以 `onebot` 的 `MessageEvent` 作为类型标注。

3. 在事件处理函数中声明依赖项。当用类作为依赖项时，它会是一个对应的实例，在这里 `x` 就是 `DependClass` 实例。

### 另一种依赖项声明方式

当使用类作为依赖项时，`Depends` 的参数可以为空，`NoneBot2` 会根据参数的类型标注进行推断并进行依赖注入。

```python
@test.handle()
async def _(x: DependClass = Depends()): # 在事件处理函数里声明依赖项
    print(x.uid, x.nickname)
```

## Generator Function 作为依赖

与 `FastAPI` 一样，`NoneBot2` 的依赖注入支持依赖项在事件处理结束后进行一些额外的工作，比如数据库 session 或者网络 IO 的关闭，互斥锁的解锁等等。

要实现上述功能，我们可以用生成器函数作为依赖项，我们用 `yield` 语句取代 `return` 语句，并在 `yield` 之后进行额外的工作。

我们可以看下述代码段, 使用 `httpx.AsyncClient` 异步网络 IO：

```python
import httpx
from nonebot.log import logger
from nonebot.params import Depends # 1.引用 Depends
from nonebot import on_command

test = on_command("123")

async def get_client(): # 2.编写异步生成器函数
    async with httpx.AsyncClient() as client:
        yield client
    print("调用结束")


@test.handle()
async def _(x: httpx.AsyncClient = Depends(get_client)): # 3.在事件处理函数里声明依赖项
    resp = await x.get("https://v2.nonebot.dev")
    # do something
```

我们用 `yield` 代码段作为生成器函数的“返回”，在事件处理函数里用返回出来的 `client` 做自己需要的工作。在 `NoneBot2` 结束事件处理时，会执行 `yield` 之后的代码。

:::warning 
`yield` 语句只能写一次，否则会引发异常。
如果对此有疑问并想探究原因，可以看 [contextmanager](https://docs.python.org/zh-cn/3/library/contextlib.html#contextlib.contextmanager) 和 [asynccontextmanager](https://docs.python.org/zh-cn/3/library/contextlib.html#contextlib.asynccontextmanager) 文档，实际上，`Nonebot2` 的内部就使用了这两个装饰器。
:::

:::tips 
生成器是 `Python` 高级特性，如果你对此处文档感到疑惑那说明暂时你还用不上这个功能。
:::

## 高阶用法：创造可调用对象作为依赖
在 `Python` 的里，类的 `__call__` 方法会让类的实例变成**可调用对象**，我们可以利用这个魔法方法做一个简单的尝试：

```python
from typing import Type
from nonebot.log import logger
from nonebot.params import Depends # 1.引用 Depends
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

test = on_command("123")

class EventChecker: # 2.编写需要的类
    def __init__(self, EventClass: Type[MessageEvent]):
    	self.event_class = EventClass
    	
    def __call__(self, event: MessageEvent) -> bool:
    	return isinstance(event, self.event_class)

checker = EventChecker(GroupMessageEvent) # 3.将类实例化

@test.handle()
async def _(x: bool  = Depends(checker)): # 4.在事件处理函数里声明依赖项
    if x:
        print("这是群聊消息")
    else:
        print("这不是群聊消息")
```

这是判断 `onebot` 的消息事件是不是群聊消息事件的一个例子，我们可以用四步来说明这个例子：

1. 引用 `Depends` 。

2. 编写依赖类。类的 `__init__` 函数接收参数 `EventClass`，它将接收事件类本身。类的 `__call__` 函数将接受消息事件对象，并返回一个 `bool` 类型的判定结果。

3. 将类实例化。我们传入群聊消息事件作为参数实例化 `checker` 。

4. 在事件处理函数里声明依赖项。`NoneBot2` 将会调用 `checker` 的 `__call__` 方法，返回给参数 `x` 相应的判断结果。

:::tips 
魔法方法 `__call__` 是 `Python` 高级特性，如果你对此处文档感到疑惑那说明暂时你还用不上这个功能。
:::