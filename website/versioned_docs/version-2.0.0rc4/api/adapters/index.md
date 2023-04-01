---
sidebar_position: 0
description: nonebot.adapters 模块
---

# nonebot.adapters

本模块定义了协议适配基类，各协议请继承以下基类。

使用 [Driver.register_adapter](../drivers/index.md#Driver-register_adapter) 注册适配器。

## _abstract class_ `Bot(adapter, self_id)` {#Bot}

- **说明**

  Bot 基类。

  用于处理上报消息，并提供 API 调用接口。

- **参数**

  - `adapter` ([Adapter](#Adapter)): 协议适配器实例

  - `self_id` (str): 机器人 ID

### _instance-var_ `adapter` {#Bot-adapter}

- **类型:** [Adapter](#Adapter)

- **说明:** 协议适配器实例

### _instance-var_ `self_id` {#Bot-self_id}

- **类型:** str

- **说明:** 机器人 ID

### _property_ `type` {#Bot-type}

- **类型:** str

- **说明:** 协议适配器名称

### _property_ `config` {#Bot-config}

- **类型:** [Config](../config.md#Config)

- **说明:** 全局 NoneBot 配置

### _async method_ `call_api(api, **data)` {#Bot-call_api}

- **说明:** 调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

- **参数**

  - `api` (str): API 名称

  - `**data` (Any): API 数据

- **返回**

  - Any

- **用法**

  ```python
  await bot.call_api("send_msg", message="hello world")
  await bot.send_msg(message="hello world")
  ```

### _abstract async method_ `send(event, message, **kwargs)` {#Bot-send}

- **说明:** 调用机器人基础发送消息接口

- **参数**

  - `event` ([Event](#Event)): 上报事件

  - `message` (str | [Message](#Message) | [MessageSegment](#MessageSegment)): 要发送的消息

  - `**kwargs` (Any): 任意额外参数

- **返回**

  - Any

### _classmethod_ `on_calling_api(func)` {#Bot-on_calling_api}

- **说明**

  调用 api 预处理。

  钩子函数参数:

  - bot: 当前 bot 对象
  - api: 调用的 api 名称
  - data: api 调用的参数字典

- **参数**

  - `func` ([T_CallingAPIHook](../typing.md#T_CallingAPIHook))

- **返回**

  - [T_CallingAPIHook](../typing.md#T_CallingAPIHook)

### _classmethod_ `on_called_api(func)` {#Bot-on_called_api}

- **说明**

  调用 api 后处理。

  钩子函数参数:

  - bot: 当前 bot 对象
  - exception: 调用 api 时发生的错误
  - api: 调用的 api 名称
  - data: api 调用的参数字典
  - result: api 调用的返回

- **参数**

  - `func` ([T_CalledAPIHook](../typing.md#T_CalledAPIHook))

- **返回**

  - [T_CalledAPIHook](../typing.md#T_CalledAPIHook)

## _abstract class_ `Event(<auto>)` {#Event}

- **说明:** Event 基类。提供获取关键信息的方法，其余信息可直接获取。

- **参数**

  auto

### _classmethod_ `validate(value)` {#Event-validate}

- **参数**

  - `value` (Any)

- **返回**

  - E

### _abstract method_ `get_type()` {#Event-get_type}

- **说明:** 获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。

- **参数**

  empty

- **返回**

  - str

### _abstract method_ `get_event_name()` {#Event-get_event_name}

- **说明:** 获取事件名称的方法。

- **参数**

  empty

- **返回**

  - str

### _abstract method_ `get_event_description()` {#Event-get_event_description}

- **说明:** 获取事件描述的方法，通常为事件具体内容。

- **参数**

  empty

- **返回**

  - str

### _method_ `get_log_string()` {#Event-get_log_string}

- **说明**

  获取事件日志信息的方法。

  通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 `NoLogException` 异常。

- **参数**

  empty

- **返回**

  - str

- **异常**

  - NoLogException

### _abstract method_ `get_user_id()` {#Event-get_user_id}

- **说明:** 获取事件主体 id 的方法，通常是用户 id 。

- **参数**

  empty

- **返回**

  - str

### _abstract method_ `get_session_id()` {#Event-get_session_id}

- **说明:** 获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。

- **参数**

  empty

- **返回**

  - str

### _abstract method_ `get_message()` {#Event-get_message}

- **说明:** 获取事件消息内容的方法。

- **参数**

  empty

- **返回**

  - [Message](#Message)

### _method_ `get_plaintext()` {#Event-get_plaintext}

- **说明**

  获取消息纯文本的方法。

  通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。

- **参数**

  empty

- **返回**

  - str

### _abstract method_ `is_tome()` {#Event-is_tome}

- **说明:** 获取事件是否与机器人有关的方法。

- **参数**

  empty

- **返回**

  - bool

## _abstract class_ `Adapter(driver, **kwargs)` {#Adapter}

- **说明**

  协议适配器基类。

  通常，在 Adapter 中编写协议通信相关代码，如: 建立通信连接、处理接收与发送 data 等。

- **参数**

  - `driver` ([Driver](../drivers/index.md#Driver)): [Driver](../drivers/index.md#Driver) 实例

  - `**kwargs` (Any): 其他由 [Driver.register_adapter](../drivers/index.md#Driver-register_adapter) 传入的额外参数

### _instance-var_ `driver` {#Adapter-driver}

- **类型:** [Driver](../drivers/index.md#Driver)

- **说明:** 实例

### _instance-var_ `bots` {#Adapter-bots}

- **类型:** dict[str, [Bot](#Bot)]

- **说明:** 本协议适配器已建立连接的 [Bot](#Bot) 实例

### _abstract classmethod_ `get_name()` {#Adapter-get_name}

- **说明:** 当前协议适配器的名称

- **参数**

  empty

- **返回**

  - str

### _property_ `config` {#Adapter-config}

- **类型:** [Config](../config.md#Config)

- **说明:** 全局 NoneBot 配置

### _method_ `bot_connect(bot)` {#Adapter-bot_connect}

- **说明**

  告知 NoneBot 建立了一个新的 [Bot](#Bot) 连接。

  当有新的 [Bot](#Bot) 实例连接建立成功时调用。

- **参数**

  - `bot` ([Bot](#Bot)): [Bot](#Bot) 实例

- **返回**

  - None

### _method_ `bot_disconnect(bot)` {#Adapter-bot_disconnect}

- **说明**

  告知 NoneBot [Bot](#Bot) 连接已断开。

  当有 [Bot](#Bot) 实例连接断开时调用。

- **参数**

  - `bot` ([Bot](#Bot)): [Bot](#Bot) 实例

- **返回**

  - None

### _method_ `setup_http_server(setup)` {#Adapter-setup_http_server}

- **说明:** 设置一个 HTTP 服务器路由配置

- **参数**

  - `setup` ([HTTPServerSetup](../drivers/index.md#HTTPServerSetup))

- **返回**

  - untyped

### _method_ `setup_websocket_server(setup)` {#Adapter-setup_websocket_server}

- **说明:** 设置一个 WebSocket 服务器路由配置

- **参数**

  - `setup` ([WebSocketServerSetup](../drivers/index.md#WebSocketServerSetup))

- **返回**

  - untyped

### _async method_ `request(setup)` {#Adapter-request}

- **说明:** 进行一个 HTTP 客户端请求

- **参数**

  - `setup` ([Request](../drivers/index.md#Request))

- **返回**

  - [Response](../drivers/index.md#Response)

### _method_ `websocket(setup)` {#Adapter-websocket}

- **说明:** 建立一个 WebSocket 客户端连接请求

- **参数**

  - `setup` ([Request](../drivers/index.md#Request))

- **返回**

  - AsyncGenerator[[WebSocket](../drivers/index.md#WebSocket), None]

## _abstract class_ `Message(<auto>)` {#Message}

- **说明:** 消息数组

- **参数**

  - `message`: 消息内容

### _classmethod_ `template(format_string)` {#Message-template}

- **说明**

  创建消息模板。

  用法和 `str.format` 大致相同, 但是可以输出消息对象, 并且支持以 `Message` 对象作为消息模板

  并且提供了拓展的格式化控制符, 可以用适用于该消息类型的 `MessageSegment` 的工厂方法创建消息

- **参数**

  - `format_string` (str | TM): 格式化模板

- **返回**

  - [MessageTemplate](#MessageTemplate)[TM]: 消息格式化器

### _abstract classmethod_ `get_segment_class()` {#Message-get_segment_class}

- **说明:** 获取消息段类型

- **参数**

  empty

- **返回**

  - type[TMS]

### _method_ `index(value, *args)` {#Message-index}

- **参数**

  - `value` (TMS | str)

  - `*args`

- **返回**

  - int

### _method_ `get(type_, count=None)` {#Message-get}

- **参数**

  - `type_` (str)

  - `count` (int | None)

- **返回**

  - TM

### _method_ `count(value)` {#Message-count}

- **参数**

  - `value` (TMS | str)

- **返回**

  - int

### _method_ `append(obj)` {#Message-append}

- **说明:** 添加一个消息段到消息数组末尾。

- **参数**

  - `obj` (str | TMS): 要添加的消息段

- **返回**

  - TM

### _method_ `extend(obj)` {#Message-extend}

- **说明:** 拼接一个消息数组或多个消息段到消息数组末尾。

- **参数**

  - `obj` (TM | Iterable[TMS]): 要添加的消息数组

- **返回**

  - TM

### _method_ `copy()` {#Message-copy}

- **参数**

  empty

- **返回**

  - TM

### _method_ `extract_plain_text()` {#Message-extract_plain_text}

- **说明:** 提取消息内纯文本消息

- **参数**

  empty

- **返回**

  - str

## _abstract class_ `MessageSegment(<auto>)` {#MessageSegment}

- **说明:** 消息段基类

- **参数**

  auto

### _instance-var_ `type` {#MessageSegment-type}

- **类型:** str

- **说明:** 消息段类型

### _class-var_ `data` {#MessageSegment-data}

- **类型:** dict[str, Any]

- **说明:** 消息段数据

### _abstract classmethod_ `get_message_class()` {#MessageSegment-get_message_class}

- **说明:** 获取消息数组类型

- **参数**

  empty

- **返回**

  - type[TM]

### _method_ `get(key, default=None)` {#MessageSegment-get}

- **参数**

  - `key` (str)

  - `default` (Any)

- **返回**

  - untyped

### _method_ `keys()` {#MessageSegment-keys}

- **参数**

  empty

- **返回**

  - untyped

### _method_ `values()` {#MessageSegment-values}

- **参数**

  empty

- **返回**

  - untyped

### _method_ `items()` {#MessageSegment-items}

- **参数**

  empty

- **返回**

  - untyped

### _method_ `copy()` {#MessageSegment-copy}

- **参数**

  empty

- **返回**

  - T

### _abstract method_ `is_text()` {#MessageSegment-is_text}

- **说明:** 当前消息段是否为纯文本

- **参数**

  empty

- **返回**

  - bool

## _class_ `MessageTemplate(template, factory=str)` {#MessageTemplate}

- **说明:** 消息模板格式化实现类。

- **参数**

  - `template` (str | TM): 模板

  - `factory` (type[str] | type[TM]): 消息类型工厂，默认为 `str`

### _method_ `add_format_spec(spec, name=None)` {#MessageTemplate-add_format_spec}

- **参数**

  - `spec` (FormatSpecFunc_T)

  - `name` (str | None)

- **返回**

  - FormatSpecFunc_T

### _method_ `format(*args, **kwargs)` {#MessageTemplate-format}

- **说明:** 根据传入参数和模板生成消息对象

- **参数**

  - `*args`

  - `**kwargs`

- **返回**

  - untyped

### _method_ `format_map(mapping)` {#MessageTemplate-format_map}

- **说明:** 根据传入字典和模板生成消息对象, 在传入字段名不是有效标识符时有用

- **参数**

  - `mapping` (Mapping[str, Any])

- **返回**

  - TF

### _method_ `vformat(format_string, args, kwargs)` {#MessageTemplate-vformat}

- **参数**

  - `format_string` (str)

  - `args` (Sequence[Any])

  - `kwargs` (Mapping[str, Any])

- **返回**

  - TF

### _method_ `format_field(value, format_spec)` {#MessageTemplate-format_field}

- **参数**

  - `value` (Any)

  - `format_spec` (str)

- **返回**

  - Any
