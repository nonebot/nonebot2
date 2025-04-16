# 通用消息组件

`uniseg` 模块属于 `nonebot-plugin-alconna` 的子插件。

通用消息组件内容较多，故分为了一个示例以及数个专题。

## 示例

### 导入

一般情况下，你只需要从 `nonebot_plugin_alconna.uniseg` 中导入 `UniMessage` 即可:

```python
from nonebot_plugin_alconna.uniseg import UniMessage
```

### 构建

你可以通过 `UniMessage` 上的快捷方法来链式构造消息:

```python
message = (
    UniMessage.text("hello world")
    .at("1234567890")
    .image(url="https://example.com/image.png")
)
```

也可以通过导入通用消息段来构建消息:

```python
from nonebot_plugin_alconna import Text, At, Image, UniMessage

message = UniMessage(
    [
        Text("hello world"),
        At("user", "1234567890"),
        Image(url="https://example.com/image.png"),
    ]
)
```

更深入一点，比如你想要发送一条包含多个按钮的消息，你可以这样做:

```python
from nonebot_plugin_alconna import Button, UniMessage

message = (
    UniMessage.text("hello world")
    .keyboard(
        Button("link1", url="https://example.com/1"),
        Button("link2", url="https://example.com/2"),
        Button("link3", url="https://example.com/3"),
        row=3,
    )
)
```

### 发送

你可以通过 `.send` 方法来发送消息:

```python
@matcher.handle()
async def _():
    message = UniMessage.text("hello world").image(url="https://example.com/image.png")
    await message.send()
    # 类似于 `matcher.finish`
    await message.finish()
```

你可以通过参数来让消息 @ 发送者:

```python
@matcher.handle()
async def _():
    message = UniMessage.text("hello world").image(url="https://example.com/image.png")
    await message.send(at_sender=True)
```

或者回复消息:

```python
@matcher.handle()
async def _():
    message = UniMessage.text("hello world").image(url="https://example.com/image.png")
    await message.send(reply_to=True)
```

### 撤回，编辑，表态

你可以通过 `message_recall`, `message_edit` 和 `message_reaction` 方法来撤回，编辑和表态消息事件。

```python
from nonebot_plugin_alconna import message_recall, message_edit, message_reaction

@matcher.handle()
async def _():
    await message_edit(UniMessage.text("hello world"))
    await message_reaction("👍")
    await message_recall()
```

你也可以对你自己发送的消息进行撤回，编辑和表态:

```python
@matcher.handle()
async def _():
    message = UniMessage.text("hello world").image(url="https://example.com/image.png")
    receipt = await message.send()
    await receipt.edit(UniMessage.text("hello world!"))
    await receipt.reaction("👍")
    await receipt.recall(delay=5)  # 5秒后撤回
```

### 处理消息

通过依赖注入，你可以在事件处理器中获取通用消息:

```python
from nonebot_plugin_alconna import UniMsg

@matcher.handle()
async def _(msg: UniMsg):
    ...
```

然后你可以通过 `UniMessage` 的方法来处理消息.

例如，你想知道消息中是否包含图片，你可以这样做:

```python
ans1 = Image in message
ans2 = message.has(Image)
ans3 = message.only(Image)
```

或者，提取所有的图片：

```python
imgs_1 = message[Image]
imgs_2 = message.get(Image)
imgs_3 = message.include(Image)
imgs_4 = message.select(Image)
imgs_5 = message.filter(lambda x: x.type == "image")
imgs_6 = message.tranform({"image": True})
```

而后，如果你想提取出所有的图片链接，你可以这样做:

```python
urls = imgs.map(lambda x: x.url)
```

如果你想知道消息是否符合某个前缀，你可以这样做:

```python
@matcher.handle()
async def _(msg: UniMsg):
    if msg.startswith("hello"):
        await matcher.finish("hello world")
    else:
        await matcher.finish("not hello world")
```

或者你想接着去除掉前缀:

```python
@matcher.handle()
async def _(msg: UniMsg):
    if msg.startswith("hello"):
        msg = msg.removeprefix("hello")
        await matcher.finish(msg)
    else:
        await matcher.finish("not hello world")
```

### 持久化

假设你在编写一个词库查询插件，你可以通过 `UniMessage.dump` 方法来将消息序列化为 JSON 格式:

```python
from nonebot_plugin_alconna import UniMsg

@matcher.handle()
async def _(msg: UniMsg):
    data: list[dict] = msg.dump()
    # 你可以将 data 存储到数据库或者 JSON 文件中
```

而后你可以通过 `UniMessage.load` 方法来将 JSON 格式的消息反序列化为 `UniMessage` 对象:

```python
from nonebot_plugin_alconna import UniMessage

@matcher.handle()
async def _():
    data = [
        {"type": "text", "text": "hello world"},
        {"type": "image", "url": "https://example.com/image.png"},
    ]
    message = UniMessage.load(data)
```
