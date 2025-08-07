---
sidebar_position: 7
description: 处理消息序列与消息段

options:
  menu:
    - category: tutorial
      weight: 90
---

# 处理消息

在不同平台中，一条消息可能会有承载有各种不同的表现形式，它可能是一段纯文本、一张图片、一段语音、一篇富文本文章，也有可能是多种类型的组合等等。

在 NoneBot 中，为确保消息的正常处理与跨平台兼容性，采用了扁平化的消息序列形式，即 `Message` 对象。消息序列是 NoneBot 中的消息载体，无论是接收还是发送的消息，都采用消息序列的形式进行处理。

## 认识消息类型

### 消息序列 `Message`

在 NoneBot 中，消息序列 `Message` 的主要作用是用于表达“一串消息”。由于消息序列继承自 `List[MessageSegment]`，所以 `Message` 的本质是由若干消息段所组成的序列。因此，消息序列的使用方法与 `List` 有很多相似之处，例如切片、索引、拼接等。

在上一节的[使用依赖注入](./event-data.mdx#使用依赖注入)中，我们已经通过依赖注入 `CommandArg()` 获取了命令的参数，它的类型即是消息序列。我们使用了消息序列的 `extract_plain_text()` 方法来获取消息序列中的纯文本内容。

### 消息段 `MessageSegment`

顾名思义，消息段 `MessageSegment` 是一段消息。由于消息序列的本质是由若干消息段所组成的序列，消息段可以被认为是构成消息序列的最小单位。简单来说，消息序列类似于一个自然段，而消息段则是组成自然段的一句话。同时，作为特殊消息载体的存在，绝大多数的平台都有着**独特的消息类型**，这些独特的内容均需要由对应的**协议适配器**所提供，以适应不同平台中的消息模式。**这也意味着，你需要导入对应的协议适配器中的消息序列和消息段后才能使用其特殊的工厂方法。**

:::caution 注意
消息段的类型是由协议适配器提供的，因此你需要参考协议适配器的文档并导入对应的消息段后才能使用其特殊的消息类型。

在上一节的[使用依赖注入](./event-data.mdx#使用依赖注入)中，我们导入的为 `nonebot.adapters.Message` 抽象基类，因此我们无法使用平台特有的消息类型。仅能使用 `str` 作为纯文本消息回复。
:::

## 使用消息序列

:::caution 注意
在以下的示例中，为了更好的理解多种类型的消息组成方式，我们将使用 `Console` 协议适配器来演示消息序列的使用方法。在实际使用中，你需要确保你使用的**消息序列类型**与你所要发送的**平台类型**一致。
:::

通常情况下，适配器在接收到消息时，会将消息转换为消息序列，可以通过依赖注入 [`EventMessage`](../advanced/dependency.mdx#eventmessage)，或者使用 `event.get_message()` 获取。

由于消息序列是 `List[MessageSegment]` 的子类，所以你总是可以用和操作 `List` 类似的方式来处理消息序列。例如：

```python
>>> from nonebot.adapters.console import Message, MessageSegment
>>> message = Message([
    MessageSegment(type="text", data={"text":"hello"}),
    MessageSegment(type="markdown", data={"markup":"**world**"}),
])
>>> for segment in message:
...     print(segment.type, segment.data)
...
text {'text': 'hello'}
markdown {'markup': '**world**'}
>>> len(message)
2
```

### 构造消息序列

在使用事件响应器操作发送消息时，既可以使用 `str` 作为消息，也可以使用 `Message`、`MessageSegment` 或者 `MessageTemplate`。那么，我们就需要先构造一个消息序列。消息序列可以通过多种方式构造：

#### 直接构造

`Message` 类可以直接实例化，支持 `str`、`MessageSegment`、`Iterable[MessageSegment]` 或适配器自定义类型的参数。

```python
from nonebot.adapters.console import Message, MessageSegment

# str
Message("Hello, world!")
# MessageSegment
Message(MessageSegment.text("Hello, world!"))
# List[MessageSegment]
Message([MessageSegment.text("Hello, world!")])
```

#### 运算构造

`Message` 对象可以通过 `str`、`MessageSegment` 相加构造，详情请参考[拼接消息](#拼接消息)。

#### 从字典数组构造

`Message` 对象支持 Pydantic 自定义类型构造，可以使用 Pydantic 的 `TypeAdapter` 方法进行构造。

```python
from pydantic import TypeAdapter
from nonebot.adapters.console import Message, MessageSegment

# 由字典构造消息段
TypeAdapter(MessageSegment).validate_python(
    {"type": "text", "data": {"text": "text"}}
) == MessageSegment.text("text")

# 由字典数组构造消息序列
TypeAdapter(Message).validate_python(
    [MessageSegment.text("text"), {"type": "text", "data": {"text": "text"}}],
) == Message([MessageSegment.text("text"), MessageSegment.text("text")])
```

### 获取消息纯文本

由于消息中存在各种类型的消息段，因此 `str(message)` 通常**不能得到消息的纯文本**，而是一个消息序列的字符串表示。

NoneBot 为消息段定义了一个方法 `is_text()` ，可以用于判断消息段是否为纯文本；也可以使用 `message.extract_plain_text()` 方法获取消息纯文本。

```python
from nonebot.adapters.console import Message, MessageSegment

# 判断消息段是否为纯文本
MessageSegment.text("text").is_text() == True

# 提取消息纯文本字符串
Message(
    [MessageSegment.text("text"), MessageSegment.markdown("**markup**")]
).extract_plain_text() == "text"
```

### 遍历

消息序列继承自 `List[MessageSegment]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:
    ...
```

### 比较

消息和消息段都可以使用 `==` 或 `!=` 运算符比较是否相同。

```python
MessageSegment.text("text") != MessageSegment.text("foo")

some_message == Message([MessageSegment.text("text")])
```

### 检查消息段

我们可以通过 `in` 运算符或消息序列的 `has` 方法来：

```python
# 是否存在消息段
MessageSegment.text("text") in message
# 是否存在指定类型的消息段
"text" in message
```

我们还可以使用消息序列的 `only` 方法来检查消息中是否仅包含指定的消息段。

```python
# 是否都为指定消息段
message.only(MessageSegment.text("test"))
# 是否仅包含指定类型的消息段
message.only("text")
```

### 过滤、索引与切片

消息序列对列表的索引与切片进行了增强，在原有列表 `int` 索引与 `slice` 切片的基础上，支持 `type` 过滤索引与切片。

```python
from nonebot.adapters.console import Message, MessageSegment

message = Message(
    [
        MessageSegment.text("test"),
        MessageSegment.markdown("test2"),
        MessageSegment.markdown("test3"),
        MessageSegment.text("test4"),
    ]
)
# 索引
message[0] == MessageSegment.text("test")
# 切片
message[0:2] == Message(
    [MessageSegment.text("test"), MessageSegment.markdown("test2")]
)
# 类型过滤
message["markdown"] == Message(
    [MessageSegment.markdown("test2"), MessageSegment.markdown("test3")]
)
# 类型索引
message["markdown", 0] == MessageSegment.markdown("test2")
# 类型切片
message["markdown", 0:2] == Message(
    [MessageSegment.markdown("test2"), MessageSegment.markdown("test3")]
)
```

我们也可以通过消息序列的 `include`、`exclude` 方法进行类型过滤。

```python
message.include("text", "markdown")
message.exclude("text")
```

同样的，消息序列对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段。

```python
# 指定类型首个消息段索引
message.index("markdown") == 1
# 指定类型消息段数量
message.count("markdown") == 2
```

此外，消息序列添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段。

```python
# 获取指定类型指定个数的消息段
message.get("markdown", 1) == Message([MessageSegment.markdown("test2")])
```

### 拼接消息

`str`、`Message`、`MessageSegment` 对象之间可以直接相加，相加均会返回一个新的 `Message` 对象。

```python
# 消息序列与消息段相加
Message([MessageSegment.text("text")]) + MessageSegment.text("text")
# 消息序列与字符串相加
Message([MessageSegment.text("text")]) + "text"
# 消息序列与消息序列相加
Message([MessageSegment.text("text")]) + Message([MessageSegment.text("text")])
# 字符串与消息序列相加
"text" + Message([MessageSegment.text("text")])
# 消息段与消息段相加
MessageSegment.text("text") + MessageSegment.text("text")
# 消息段与字符串相加
MessageSegment.text("text") + "text"
# 消息段与消息序列相加
MessageSegment.text("text") + Message([MessageSegment.text("text")])
# 字符串与消息段相加
"text" + MessageSegment.text("text")
```

如果需要在当前消息序列后直接拼接新的消息段，可以使用 `Message.append`、`Message.extend` 方法，或者使用自加。

```python
msg = Message([MessageSegment.text("text")])
# 自加
msg += "text"
msg += MessageSegment.text("text")
msg += Message([MessageSegment.text("text")])
# 附加
msg.append("text")
msg.append(MessageSegment.text("text"))
# 扩展
msg.extend([MessageSegment.text("text")])
```

我们也可以通过消息段或消息序列的 `join` 方法来拼接一串消息：

```python
seg = MessageSegment.text("text")
msg = seg.join(
    [
        MessageSegment.text("first"),
        Message(
            [
                MessageSegment.text("second"),
                MessageSegment.text("third"),
            ]
        )
    ]
)
msg == Message(
    [
        MessageSegment.text("first"),
        MessageSegment.text("text"),
        MessageSegment.text("second"),
        MessageSegment.text("third"),
    ]
)
```

### 使用消息模板

为了提供安全可靠的跨平台模板字符，我们提供了一个消息模板功能来构建消息序列

它在以下常见场景中尤其有用：

- 多行富文本编排（包含图片，文字以及表情等）
- 客制化（由 Bot 最终用户提供消息模板时）

在事实上，它的用法和 `str.format` 极为相近，所以你在使用的时候，总是可以参考[Python 文档](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format)来达到你想要的效果，这里给出几个简单的例子。

默认情况下，消息模板采用 `str` 纯文本形式的格式化：

```python title=基础格式化用法
>>> from nonebot.adapters import MessageTemplate
>>> MessageTemplate("{} {}").format("hello", "world")
'hello world'
```

如果 `Message.template` 构建消息模板，那么消息模板将采用消息序列形式的格式化，此时的消息将会是平台特定的：

:::caution 注意
使用 `Message.template` 构建消息模板时，应注意消息序列为平台适配器提供的类型，不能使用 `nonebot.adapters.Message` 基类作为模板构建。使用基类构建模板与使用 `str` 构建模板的效果是一样的，因此请使用上述的 `MessageTemplate` 类直接构建模板。：
:::

```python title=平台格式化用法
>>> from nonebot.adapters.console import Message, MessageSegment
>>> Message.template("{} {}").format("hello", "world")
Message(
    MessageSegment.text("hello"),
    MessageSegment.text(" "),
    MessageSegment.text("world")
)
```

消息模板支持使用消息段进行格式化：

```python title=对消息段进行安全的拼接
>>> from nonebot.adapters.console import Message, MessageSegment
>>> Message.template("{}{}").format(MessageSegment.markdown("**markup**"), "world")
Message(
    MessageSegment(type='markdown', data={'markup': '**markup**'}),
    MessageSegment(type='text', data={'text': 'world'})
)
```

消息模板同样支持使用消息序列作为模板：

```python title=以消息对象作为模板
>>> from nonebot.adapters.console import Message, MessageSegment
>>> Message.template(
...     MessageSegment.text("{user_id}") + MessageSegment.emoji("tada") +
...     MessageSegment.text("{message}")
... ).format_map({"user_id": 123456, "message": "hello world"})
Message(
    MessageSegment(type='text', data={'text': '123456'}),
    MessageSegment(type='emoji', data={'emoji': 'tada'}),
    MessageSegment(type='text', data={'text': 'hello world'})
)
```

:::caution 注意
只有消息序列中的文本类型消息段才能被格式化，其他类型的消息段将会原样添加。
:::

消息模板支持使用拓展控制符来控制消息段类型：

```python title=使用消息段的拓展控制符
>>> from nonebot.adapters.console import Message, MessageSegment
>>> Message.template("{name:emoji}").format(name='tada')
Message(MessageSegment(type='emoji', data={'name': 'tada'}))
```
