---
sidebar_position: 3

options:
  menu:
    weight: 62
    category: advanced
---

# 依赖注入

受 [`FastApi`](https://fastapi.tiangolo.com/tutorial/dependencies/) 启发，NoneBot 同样编写了一个简易的依赖注入模块，使得开发者可以通过事件处理函数参数的类型标注来自动注入依赖。

## 什么是依赖注入？

~~交给 mix 了~~

## 使用依赖注入

以下通过一个简单的例子来说明依赖注入的使用方法：

### 编写依赖函数

这里我们编写了一个简单的函数 `depend` 作为依赖函数

```python {7-9}
from nonebot.log import logger
from nonebot.dependencies import Depends
from nonebot import on_command, on_message

test = on_command("123")

def depend(state: dict):
    # do something with state
    return {**state, "depend": "depend"}

@test.handle()
async def _(x: dict = Depends(depend)):
    print(x)
```

它和普通的事件处理函数并无区别，同样可以接受 `bot`, `event` 等参数，你可以把它当作一个普通的事件处理函数但是去除了装饰器（并没有使用 `matcher.handle()` 等来进行装饰），并且它可以返回任何类型的值。

在这个例子中，依赖函数接受一个参数：

- `state: dict`：当前事件处理状态字典。

并且返回了一个 `state` 的复制以及一个附加的键值 `depend` 。

### Import `Depends`

```python {2}
from nonebot.log import logger
from nonebot.dependencies import Depends
from nonebot import on_command, on_message

test = on_command("123")

def depend(state: dict):
    # do something with state
    return {**state, "depend": "depend"}

@test.handle()
async def _(x: dict = Depends(depend)):
    print(x)
```

### 在事件处理函数里声明依赖函数

与 FastAPI 类似，你可以在函数中添加一个新的参数，并且使用 `Depends` 来声明它的依赖。

```python {12}
from nonebot.log import logger
from nonebot.dependencies import Depends
from nonebot import on_command, on_message

test = on_command("123")

def depend(state: dict):
    # do something with state
    return {**state, "depend": "depend"}

@test.handle()
async def _(x: dict = Depends(depend)):
    print(x)
```

你需要给 `Depends` 指定一个依赖函数，这个依赖函数的返回值会被作为 `x` 的值。

`Depends` 的首个参数即是依赖函数，或者其他 `Callable` 对象，在之后会对更多形式的依赖对象进行介绍。

:::tip
参数 `x` 的类型标注并不会影响事件处理函数的运行，类型检查并不会对依赖函数的返回值以及类型标注进行检查。
:::

当接收到事件时，NoneBot 会进行以下处理：

1. 查询缓存，如果缓存中有相应的值，则直接返回。
2. 准备依赖函数所需要的参数。
3. 调用依赖函数并获得返回值。
4. 将返回值存入缓存。
5. 将返回值作为事件处理函数中的参数值传入。

## 依赖缓存

## Class 作为依赖

## Generator 作为依赖
