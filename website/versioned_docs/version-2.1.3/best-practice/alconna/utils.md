---
sidebar_position: 6
description: 杂项
---

# 杂项

## 特殊装饰器

`nonebot_plugin_alconna` 提供 了一个 `funcommand` 装饰器，其用于将一个接受任意参数，
返回 `str` 或 `Message` 或 `MessageSegment` 的函数转换为命令响应器。

```python
from nonebot_plugin_alconna import funcommand

@funcommand()
async def echo(msg: str):
    return msg
```

其等同于

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match

echo = on_alconna(Alconna("echo", Args["msg", str]))

@echo.handle()
async def echo_exit(msg: Match[str] = AlconnaMatch("msg")):
    await echo.finish(msg.result)
```

## 特殊构造器

`nonebot_plugin_alconna` 提供了一个 `Command` 构造器，其基于 `arclet.alconna.tools` 中的 `AlconnaString`，
以类似 `Koishi` 中注册命令的方式来构建一个 AlconnaMatcher：

```python
from nonebot_plugin_alconna import Command, Arparma

book = (
    Command("book", "测试")
    .option("writer", "-w <id:int>")
    .option("writer", "--anonymous", {"id": 0})
    .usage("book [-w <id:int> | --anonymous]")
    .shortcut("测试", {"args": ["--anonymous"]})
    .build()
)

@book.handle()
async def _(arp: Arparma):
    await book.send(str(arp.options))
```

甚至，你可以设置 `action` 来设定响应行为：

```python
book = (
    Command("book", "测试")
    .option("writer", "-w <id:int>")
    .option("writer", "--anonymous", {"id": 0})
    .usage("book [-w <id:int> | --anonymous]")
    .shortcut("测试", {"args": ["--anonymous"]})
    .action(lambda options: str(options))  # 会自动通过 bot.send 发送
    .build()
)
```

## 中间件

在 `AlconnaMatch`, `AlconnaQuery` 或 `got_path` 中，你可以使用 `middleware` 参数来传入一个对返回值进行处理的函数，

```python {1, 9}
from nonebot_plugin_alconna import image_fetch

mask_cmd = on_alconna(
    Alconna("search", Args["img?", Image]),
)


@mask_cmd.handle()
async def mask_h(matcher: AlconnaMatcher, img: Match[bytes] = AlconnaMatch("img", image_fetch)):
    result = await search_img(img.result)
    await matcher.send(result.content)
```

其中，`image_fetch` 是一个中间件，其接受一个 `Image` 对象，并提取图片的二进制数据返回。
