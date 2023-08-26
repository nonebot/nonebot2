---
sidebar_position: 5
description: 杂项
---

# 杂项

## 通用消息序列


除了之前提到的通用标注外，`nonebot_plugin_alconna` 还提供了一个类似于 `Message` 的 `UniMessage` 类型，其元素为经过通用标注转换后的 `Segment`。

你可以通过提供的 `UniversalMessage` 或 `UniMsg` 依赖注入器来获取 `UniMessage`。

```python
from nonebot_plugin_alconna import UniMsg, At, Reply

matcher = on_xxx(...)

@matcher.handle()
async def _(msg: UniMsg):
    reply = msg[Reply, 0]
    print(reply.origin)
    if msg.has(At):
        ats = msg.get(At)
        print(ats)
    ...
```


### 获取消息纯文本

类似于 `Message.extract_plain_text()`，用于获取通用消息的纯文本。

```python
from nonebot_plugin_alconna import UniMessage, At
# 提取消息纯文本字符串
assert UniMessage(
    [At("user", "1234"), "text"]
).extract_plain_text() == "text"
```

### 遍历

通用消息序列继承自 `List[Union[str, Segment]]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:  # type: Union[str, Segment]
    ...
```

### 检查消息段

我们可以通过 `in` 运算符或消息序列的 `has` 方法来：

```python
# 是否存在消息段
At("user", "1234") in message
# 是否存在指定类型的消息段
At in message
```

我们还可以使用 `only` 方法来检查消息中是否仅包含指定的消息段。

```python
# 是否都为 "test"
message.only("test")
# 是否仅包含指定类型的消息段
message.only(str)
```

### 过滤、索引与切片

消息序列对列表的索引与切片进行了增强，在原有列表 `int` 索引与 `slice` 切片的基础上，支持 `type` 过滤索引与切片。

```python
from nonebot_plugin_alconna import UniMessage, At, Reply

message = UniMessage(
    [
        Reply(...),
        "text1",
        At("user", "1234"),
        "text2"
    ]
)
# 索引
message[0] == Reply(...)
# 切片
message[0:2] == UniMessage([Reply(...), "text1"])
# 类型过滤
message[At] == Message([At("user", "1234")])
# 类型索引
message[At, 0] == At("user", "1234")
# 类型切片
message[str, 0:2] == UniMessage(["text1", "text2"])
```

我们也可以通过消息序列的 `include`、`exclude` 方法进行类型过滤。

```python
message.include(str, At)
message.exclude(Reply)
```

同样的，消息序列对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段。

```python
# 指定类型首个消息段索引
message.index(str) == 1
# 指定类型消息段数量
message.count(str) == 2
```

此外，消息序列添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段。

```python
# 获取指定类型指定个数的消息段
message.get(str, 1) == UniMessage(["test1"])
```

## 特殊装饰器

`nonebot_plugin_alconna` 提供 了一个 `funcommand` 装饰器, 其用于将一个接受任意参数，
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