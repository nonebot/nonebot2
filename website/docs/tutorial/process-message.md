---
sidebar_position: 9
description: 处理消息序列与消息段

options:
  menu:
    weight: 30
    category: guide
---

# 处理消息

## NoneBot2 中的消息

在不同平台中，一条消息可能会有承载有各种不同的表现形式，它可能是一段纯文本、一张图片、一段语音、一篇富文本文章，也有可能是多种类型的组合等等。

在 NoneBot2 中，为确保消息的正常处理与跨平台兼容性，采用了扁平化的消息序列形式，即 `Message` 对象。

`Message` 是多个消息段 `MessageSegment` 的集合，它继承自 `List[MessageSegment]`，并在此基础上添加或强化了一些特性。

`MessageSegment` 是一个 [`dataclass`](https://docs.python.org/zh-cn/3/library/dataclasses.html#dataclasses.dataclass) ，它具有一个类型标识 `type`，以及一些对应的数据信息 `data`。

此外，NoneBot2 还提供了 `MessageTemplate` ，用于构建支持消息序列以及消息段的特殊消息模板。

## 使用消息序列

通常情况下，适配器在接收到消息时，会将消息转换为消息序列，可以通过 [`EventMessage`](./plugin/create-handler.md#EventMessage) 作为依赖注入, 或者使用 `event.get_message()` 获取。

由于它是`List[MessageSegment]`的子类, 所以你总是可以用和操作List类似的方式来处理消息序列

```python
>>> message = Message([
    MessageSegment(type='text', data={'text':'hello'}),
    MessageSegment(type='image', data={'url':'http://example.com/image.png'}),
    MessageSegment(type='text', data={'text':'world'}),
])
>>> for segment in message:
...     print(segment.type, segment.data)
...
text {'text': 'hello'}
image {'url': 'http://example.com/image.png'}
text {'text': 'world'}
>>> len(message)
3
```

### 构造消息序列

在使用事件响应器操作发送消息时，既可以使用 `str` 作为消息，也可以使用 `Message`、`MessageSegment` 或者 `MessageTemplate`。那么，我们就需要先构造一个消息序列。

#### 直接构造

`Message` 类可以直接实例化，支持 `str`、`MessageSegment`、`Iterable[MessageSegment]` 或适配器自定义类型的参数。

```python
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

`Message` 对象支持 Pydantic 自定义类型构造，可以使用 Pydantic 的 `parse_obj_as` (`parse_raw_as`) 方法进行构造。

```python
from pydantic import parse_obj_as

# 由字典构造消息段
parse_obj_as(
    MessageSegment, {"type": "text", "data": {"text": "text"}}
) == MessageSegment.text("text")
# 由字典数组构造消息序列
parse_obj_as(
    Message,
    [MessageSegment.text("text"), {"type": "text", "data": {"text": "text"}}],
) == Message([MessageSegment.text("text"), MessageSegment.text("text")])
```

:::tip 提示
以上示例中的字典数据仅做参考，具体的数据格式由适配器自行定义。
:::

### 获取消息纯文本

由于消息中存在各种类型的消息段，因此 `str(message)` 通常并不能得到消息的纯文本，而是一个消息序列的字符串表示。

NoneBot2 为消息段定义了一个方法 `is_text()` ，可以用于判断消息段是否为纯文本；也可以使用 `message.extract_plain_text()` 方法获取消息纯文本。

```python
# 判断消息段是否为纯文本
MessageSegment.text("text").is_text() == True
# 提取消息纯文本字符串
Message(
    [MessageSegment.text("text"), MessageSegment.at(123)]
).extract_plain_text() == "text"
```

### 遍历

`Message` 继承自 `List[MessageSegment]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:
    ...
```

### 索引与切片

`Message` 对列表的索引与切片进行了增强，在原有列表 int 索引与切片的基础上，支持 `type` 过滤索引与切片。

```python
message = Message(
    [
        MessageSegment.text("test"),
        MessageSegment.image("test2"),
        MessageSegment.image("test3"),
        MessageSegment.text("test4"),
    ]
)

# 索引
message[0] == MessageSegment.text("test")
# 切片
message[0:2] == Message(
    [MessageSegment.text("test"), MessageSegment.image("test2")]
)

# 类型过滤
message["image"] == Message(
    [MessageSegment.image("test2"), MessageSegment.image("test3")]
)
# 类型索引
message["image", 0] == MessageSegment.image("test2")
# 类型切片
message["image", 0:2] == Message(
    [MessageSegment.image("test2"), MessageSegment.image("test3")]
)
```

同样的，`Message` 对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段。

```python
# 指定类型首个消息段索引
message.index("image") == 1
# 指定类型消息段数量
message.count("image") == 2
```

此外，`Message` 添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段。

```python
# 获取指定类型指定个数的消息段
message.get("image", 1) == Message([MessageSegment.image("test2")])
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

## 使用消息模板

为了提供安全可靠的跨平台模板字符, 我们提供了一个消息模板功能来构建消息序列

它在以下常见场景中尤其有用:

- 多行富文本编排(包含图片,文字以及表情等)

- 客制化(由Bot最终用户提供消息模板时)

在事实上, 它的用法和`str.format`极为相近, 所以你在使用的时候, 总是可以参考[Python文档](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format)来达到你想要的效果

这里给出几个简单的例子:

:::tip
这里面所有的`Message`均是用对应Adapter的实现导入的, 而不是抽象基类
:::

```python title="基础格式化用法"
>>> Message.template("{} {}").format("hello", "world")
Message(MessageSegment(type='text', data={'text': 'hello world'}))
```

```python title="对消息段进行安全的拼接"
>>> Message.template("{} {}").format(MessageSegment.image("file:///..."), "world")
Message(MessageSegment(type='image', data={'file': 'file:///...'}), MessageSegment(type='text', data={'text': 'world'}))
```

```python title="以消息对象作为模板"
>>> Message.template( 
...       MessageSegment.text('test {user_id}') + MessageSegment.face(233) +
...       MessageSegment.text('test {message}')).format_map({'user_id':123456, 'message':'hello world'})
Message(MessageSegment(type='text', data={'text': 'test 123456'}),
        MessageSegment(type='face', data={'face': 233}),
        MessageSegment(type='text', data={'text': 'test hello world'}))
```

```python title="使用消息段的拓展格式规格"
>>> Message.template("{link:image}").format(link='https://...')
Message(MessageSegment(type='image', data={'file': 'https://...'}))
```
