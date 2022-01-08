---
id: index
slug: /api/adapters/
---

# NoneBot.adapters 模块

## 协议适配基类

各协议请继承以下基类，并使用 `driver.register_adapter` 注册适配器

## _class_ `Bot`

基类：`abc.ABC`

Bot 基类。用于处理上报消息，并提供 API 调用接口。

### `_calling_api_hook`

- **类型**

  `Set[T_CallingAPIHook]`

- **说明**

  call_api 时执行的函数

### `_called_api_hook`

- **类型**

  `Set[T_CalledAPIHook]`

- **说明**

  call_api 后执行的函数

### `__init__(adapter, self_id)`

- **参数**

  - `self_id: str`: 机器人 ID

  - `request: HTTPConnection`: request 连接对象

### `self_id`

机器人 ID

### _async_ `call_api(api, **data)`

- **说明**

  调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

- **参数**

  - `api: str`: API 名称

  - `**data`: API 数据

- **示例**

```python
await bot.call_api("send_msg", message="hello world")
await bot.send_msg(message="hello world")
```

### _abstract async_ `send(event, message, **kwargs)`

- **说明**

  调用机器人基础发送消息接口

- **参数**

  - `event: Event`: 上报事件

  - `message: Union[str, Message, MessageSegment]`: 要发送的消息

  - `**kwargs`

### _classmethod_ `on_calling_api(func)`

- **说明**

  调用 api 预处理。

- **参数**

  - `bot: Bot`: 当前 bot 对象

  - `api: str`: 调用的 api 名称

  - `data: Dict[str, Any]`: api 调用的参数字典

### _classmethod_ `on_called_api(func)`

- **说明**

  调用 api 后处理。

- **参数**

  - `bot: Bot`: 当前 bot 对象

  - `exception: Optional[Exception]`: 调用 api 时发生的错误

  - `api: str`: 调用的 api 名称

  - `data: Dict[str, Any]`: api 调用的参数字典

  - `result: Any`: api 调用的返回

## _class_ `MessageSegment`

基类：`Mapping`, `abc.ABC`, `Generic`[`nonebot.adapters._message.TM`]

消息段基类

### `type`

- 类型: `str`

- 说明: 消息段类型

### `data`

- 类型: `Dict[str, Union[str, list]]`

- 说明: 消息段数据

## _class_ `Message`

基类：`List`[`nonebot.adapters._message.TMS`], `abc.ABC`

消息数组

### `__init__(message=None, *args, **kwargs)`

- **参数**

  - `message: Union[str, list, dict, MessageSegment, Message, Any]`: 消息内容

### _classmethod_ `template(format_string)`

- **说明**

  根据创建消息模板, 用法和 `str.format` 大致相同, 但是可以输出消息对象, 并且支持以 `Message` 对象作为消息模板
  并且提供了拓展的格式化控制符, 可以用适用于该消息类型的 `MessageSegment` 的工厂方法创建消息

- **示例**

```python
>>> Message.template("{} {}").format("hello", "world") # 基础演示
Message(MessageSegment(type='text', data={'text': 'hello world'}))
>>> Message.template("{} {}").format(MessageSegment.image("file///..."), "world") # 支持消息段等对象
Message(MessageSegment(type='image', data={'file': 'file///...'}), MessageSegment(type='text', data={'text': 'world'}))
>>> Message.template( # 支持以Message对象作为消息模板
...       MessageSegment.text('test {event.user_id}') + MessageSegment.face(233) +
...       MessageSegment.text('test {event.message}')).format(event={'user_id':123456, 'message':'hello world'})
Message(MessageSegment(type='text', data={'text': 'test 123456'}),
        MessageSegment(type='face', data={'face': 233}),
        MessageSegment(type='text', data={'text': 'test hello world'}))
>>> Message.template("{link:image}").format(link='https://...') # 支持拓展格式化控制符
Message(MessageSegment(type='image', data={'file': 'https://...'}))
```

- **参数**

  - `format_string: str`: 格式化字符串

- **返回**

  - `MessageFormatter[TM]`: 消息格式化器

### `append(obj)`

- **说明**

  添加一个消息段到消息数组末尾

- **参数**

  - `obj: Union[str, MessageSegment]`: 要添加的消息段

### `extend(obj)`

- **说明**

  拼接一个消息数组或多个消息段到消息数组末尾

- **参数**

  - `obj: Union[Message, Iterable[MessageSegment]]`: 要添加的消息数组

### `extract_plain_text()`

- **说明**

  提取消息内纯文本消息

## _class_ `Event`

基类：`abc.ABC`, `pydantic.main.BaseModel`

Event 基类。提供获取关键信息的方法，其余信息可直接获取。

### _abstract_ `get_type()`

- **说明**

  获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。

- **返回**

  - `Literal["message", "notice", "request", "meta_event"]`

  - 其他自定义 `str`

### _abstract_ `get_event_name()`

- **说明**

  获取事件名称的方法。

- **返回**

  - `str`

### _abstract_ `get_event_description()`

- **说明**

  获取事件描述的方法，通常为事件具体内容。

- **返回**

  - `str`

### `get_log_string()`

- **说明**

  获取事件日志信息的方法，通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 `NoLogException` 异常。

- **返回**

  - `str`

- **异常**

  - `NoLogException`

### _abstract_ `get_user_id()`

- **说明**

  获取事件主体 id 的方法，通常是用户 id 。

- **返回**

  - `str`

### _abstract_ `get_session_id()`

- **说明**

  获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。

- **返回**

  - `str`

### _abstract_ `get_message()`

- **说明**

  获取事件消息内容的方法。

- **返回**

  - `Message`

### `get_plaintext()`

- **说明**

  获取消息纯文本的方法，通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。

- **返回**

  - `str`

### _abstract_ `is_tome()`

- **说明**

  获取事件是否与机器人有关的方法。

- **返回**

  - `bool`

## _class_ `MessageTemplate`

基类：`string.Formatter`, `Generic`[`nonebot.adapters._template.TF`]

消息模板格式化实现类

### `__init__(template, factory=<class 'str'>)`

- **说明**

  创建一个模板

- **参数**

  - `template: Union[str, Message]`: 模板

  - `factory: Union[str, Message]`: 消息构造类型，默认为 str

### `format(*args, **kwargs)`

- **说明**

  根据模板和参数生成消息对象
