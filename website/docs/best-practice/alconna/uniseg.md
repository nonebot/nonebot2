---
sidebar_position: 5
description: 通用消息组件
---

# 通用消息组件

`uniseg` 模块属于 `nonebot-plugin-alconna` 的子插件，其提供了一套通用的消息组件，用于在 `nonebot-plugin-alconna` 下构建通用消息。

## 通用消息段

`nonebot-plugin-alconna.uniseg` 提供了类似 `MessageSegment` 的通用消息段，并可在 `Alconna` 下直接标注使用：

```python
class Segment:
    """基类标注"""

class Text(Segment):
    """Text对象, 表示一类文本元素"""
    text: str
    style: Optional[str]

class At(Segment):
    """At对象, 表示一类提醒某用户的元素"""
    type: Literal["user", "role", "channel"]
    target: str

class AtAll(Segment):
    """AtAll对象, 表示一类提醒所有人的元素"""

class Emoji(Segment):
    """Emoji对象, 表示一类表情元素"""
    id: str
    name: Optional[str]

class Media(Segment):
    url: Optional[str]
    id: Optional[str]
    path: Optional[str]
    raw: Optional[bytes]

class Image(Media):
    """Image对象, 表示一类图片元素"""

class Audio(Media):
    """Audio对象, 表示一类音频元素"""

class Voice(Media):
    """Voice对象, 表示一类语音元素"""

class Video(Media):
    """Video对象, 表示一类视频元素"""

class File(Segment):
    """File对象, 表示一类文件元素"""
    id: str
    name: Optional[str]

class Reply(Segment):
    """Reply对象，表示一类回复消息"""
    origin: Any
    id: str
    msg: Optional[Union[Message, str]]

class Card(Segment):
	type: Literal["xml", "json"]
	raw: str

class Other(Segment):
    """其他 Segment"""
```

来自各自适配器的消息序列都会经过这些通用消息段对应的标注转换，以达到跨平台接收消息的作用

## 通用消息序列

`nonebot-plugin-alconna.uniseg` 同时提供了一个类似于 `Message` 的 `UniMessage` 类型，其元素为经过通用标注转换后的通用消息段。

你可以通过提供的 `UniversalMessage` 或 `UniMsg` 依赖注入器来获取 `UniMessage`。

```python
from nonebot_plugin_alconna.uniseg import UniMsg, At, Reply

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

不仅如此，你还可以通过 `UniMessage` 的 `export` 方法来**跨平台发送消息**。

`UniMessage.export` 会通过传入的 `bot: Bot` 参数读取适配器信息，并使用对应的生成方法把通用消息转为适配器对应的消息序列：

```python
from nonebot import Bot, on_command
from nonebot_plugin_alconna.uniseg import Image, UniMessage

test = on_command("test")

@test.handle()
async def handle_test(bot: Bot):
    await test.send(await UniMessage(Image(path="path/to/img")).export(bot))
```

而在 `AlconnaMatcher` 下，`got`, `send`, `reject` 等可以发送消息的方法皆支持使用 `UniMessage`，不需要手动调用 export 方法：

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import Match, AlconnaMatcher, on_alconna
from nonebot_plugin_alconna.uniseg import At,  UniMessage

test_cmd = on_alconna(Alconna("test", Args["target?", At]))

@test_cmd.handle()
async def tt_h(matcher: AlconnaMatcher, target: Match[At]):
    if target.available:
        matcher.set_path_arg("target", target.result)

@test_cmd.got_path("target", prompt="请输入目标")
async def tt(target: At):
    await test_cmd.send(UniMessage([target, "\ndone."]))
```

### 获取消息纯文本

类似于 `Message.extract_plain_text()`，用于获取通用消息的纯文本。

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At
# 提取消息纯文本字符串
assert UniMessage(
    [At("user", "1234"), "text"]
).extract_plain_text() == "text"
```

### 遍历

通用消息序列继承自 `List[Segment]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:  # type: Segment
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
message.only(Text)
```

### 过滤、索引与切片

消息序列对列表的索引与切片进行了增强，在原有列表 `int` 索引与 `slice` 切片的基础上，支持 `type` 过滤索引与切片。

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At, Text, Reply

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
message[0:2] == UniMessage([Reply(...), Text("text1")])
# 类型过滤
message[At] == Message([At("user", "1234")])
# 类型索引
message[At, 0] == At("user", "1234")
# 类型切片
message[Text, 0:2] == UniMessage([Text("text1"), Text("text2")])
```

我们也可以通过消息序列的 `include`、`exclude` 方法进行类型过滤。

```python
message.include(Text, At)
message.exclude(Reply)
```

同样的，消息序列对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段。

```python
# 指定类型首个消息段索引
message.index(Text) == 1
# 指定类型消息段数量
message.count(Text) == 2
```

此外，消息序列添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段。

```python
# 获取指定类型指定个数的消息段
message.get(Text, 1) == UniMessage([Text("test1")])
```

### 拼接消息

`str`、`UniMessage`、`Segment` 对象之间可以直接相加，相加均会返回一个新的 `UniMessage` 对象。

```python
# 消息序列与消息段相加
UniMessage("text") + Text("text")
# 消息序列与字符串相加
UniMessage([Text("text")]) + "text"
# 消息序列与消息序列相加
UniMessage("text") + UniMessage([Text("text")])
# 字符串与消息序列相加
"text" + UniMessage([Text("text")])
# 消息段与消息段相加
Text("text") + Text("text")
# 消息段与字符串相加
Text("text") + "text"
# 消息段与消息序列相加
Text("text") + UniMessage([Text("text")])
# 字符串与消息段相加
"text" + Text("text")
```

如果需要在当前消息序列后直接拼接新的消息段，可以使用 `Message.append`、`Message.extend` 方法，或者使用自加。

```python
msg = UniMessage([Text("text")])
# 自加
msg += "text"
msg += Text("text")
msg += UniMessage([Text("text")])
# 附加
msg.append(Text("text"))
# 扩展
msg.extend([Text("text")])
```

### 使用消息模板

`UniMessage.template` 同样类似于 `Message.template`，可以用于格式化消息。大体用法参考 [消息模板](../../tutorial/message#使用消息模板)。

这里额外说明 `UniMessage.template` 的拓展控制符

相比 `Message`，UniMessage 对于 {:XXX} 做了另一类拓展。其能够识别例如 At(xxx, yyy) 或 Emoji(aaa, bbb)的字符串并执行

以 At(...) 为例：

```python title=使用通用消息段的拓展控制符
>>> from nonebot_plugin_alconna.uniseg import UniMessage
>>>  UniMessage.template("{:At(user, target)}").format(target="123")
UniMessage(At("user", "123"))
>>> UniMessage.template("{:At(type=user, target=id)}").format(id="123")
UniMessage(At("user", "123"))
>>> UniMessage.template("{:At(type=user, target=123)}").format()
UniMessage(At("user", "123"))
```

而在 `AlconnaMatcher` 中，{:XXX} 更进一步地提供了获取 `event` 和 `bot` 中的属性的功能

```python title=在 AlconnaMatcher 中使用通用消息段的拓展控制符
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import At, Match, UniMessage, AlconnaMatcher, on_alconna

test_cmd = on_alconna(Alconna("test", Args["target?", At]))

@test_cmd.handle()
async def tt_h(matcher: AlconnaMatcher, target: Match[At]):
    if target.available:
        matcher.set_path_arg("target", target.result)

@test_cmd.got_path(
    "target",
    prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请确认目标")
)
async def tt():
    await test_cmd.send(
      UniMessage.template("{:At(user, $event.get_user_id())} 已确认目标为 {target}")
    )
```
