---
sidebar_position: 6
description: 快捷方式
---

# 快捷方式声明

针对 `Alconna` 编写对于入门开发者来说较为复杂的问题，本插件提供了一些快捷方式来简化开发者的工作。

## 装饰器构造器

本插件提供了一个 `funcommand` 装饰器, 其用于将一个接受任意参数， 返回 `str` 或 `Message` 或 `MessageSegment` 的函数转换为命令响应器：

```python
from nonebot_plugin_alconna import funcommand


@funcommand()
async def echo(msg: str):
    return msg
```

其等同于：

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match


echo = on_alconna(Alconna("echo", Args["msg", str]))

@echo.handle()
async def echo_exit(msg: Match[str] = AlconnaMatch("msg")):
    await echo.finish(msg.result)

```

相比于 `on_alconna`， `funcommand` 增加了三个参数 `name`, `prefixes` 和 `description`。

## 类 Koishi 构造器

本插件提供了一个 `Command` 构造器，其基于 `arclet.alconna.tools` 中的 `AlconnaString`， 以类似 `Koishi` 中注册命令的方式来构建一个 **AlconnaMatcher** ：

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

### 从文件加载

`Command` 支持读取 `json` 或 `yaml` 文件来加载命令：

```yml title="book.yml"
command: book
help: 测试
options:
  - name: writer
    opt: "-w <id:int>"
  - name: writer
    opt: "--anonymous"
    default:
      id: 1
usage: book [-w <id:int> | --anonymous]
shortcuts:
  - key: 测试
    args: ["--anonymous"]
actions:
  -
    params: ["options"]
    code: |
      return str(options)
```

```python title="加载"
from nonebot_plugin_alconna import command_from_yaml

book = command_from_yaml("book.yml")
```
