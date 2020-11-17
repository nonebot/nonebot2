---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters 模块

## 协议适配基类

各协议请继承以下基类，并使用 `driver.register_adapter` 注册适配器


## _class_ `BaseBot`

基类：`abc.ABC`

Bot 基类。用于处理上报消息，并提供 API 调用接口。


### _abstract_ `__init__(driver, connection_type, config, self_id, *, websocket=None)`


* **参数**

    
    * `driver: Driver`: Driver 对象


    * `connection_type: str`: http 或者 websocket


    * `config: Config`: Config 对象


    * `self_id: str`: 机器人 ID


    * `websocket: Optional[WebSocket]`: Websocket 连接对象



### `driver`

Driver 对象


### `connection_type`

连接类型


### `config`

Config 配置对象


### `self_id`

机器人 ID


### `websocket`

Websocket 连接对象


### _abstract property_ `type`

Adapter 类型


### _abstract async classmethod_ `check_permission(driver, connection_type, headers, body)`


* **说明**

    检查连接请求是否合法的函数，如果合法则返回当前连接 `唯一标识符`，通常为机器人 ID；如果不合法则抛出 `RequestDenied` 异常。



* **参数**

    
    * `driver: Driver`: Driver 对象


    * `connection_type: str`: 连接类型


    * `headers: dict`: 请求头


    * `body: Optional[dict]`: 请求数据，WebSocket 连接该部分为空



* **返回**

    
    * `str`: 连接唯一标识符



* **异常**

    
    * `RequestDenied`: 请求非法



### _abstract async_ `handle_message(message)`


* **说明**

    处理上报消息的函数，转换为 `Event` 事件后调用 `nonebot.message.handle_event` 进一步处理事件。



* **参数**

    
    * `message: dict`: 收到的上报消息



### _abstract async_ `call_api(api, **data)`


* **说明**

    调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用



* **参数**

    
    * `api: str`: API 名称


    * `**data`: API 数据



* **示例**


```python
await bot.call_api("send_msg", message="hello world"})
await bot.send_msg(message="hello world")
```


### _abstract async_ `send(event, message, **kwargs)`


* **说明**

    调用机器人基础发送消息接口



* **参数**

    
    * `event: Event`: 上报事件


    * `message: Union[str, Message, MessageSegment]`: 要发送的消息


    * `**kwargs`



## _class_ `BaseEvent`

基类：`abc.ABC`

Event 基类。提供上报信息的关键信息，其余信息可从原始上报消息获取。


### `__init__(raw_event)`


* **参数**

    
    * `raw_event: dict`: 原始上报消息



### _property_ `raw_event`

原始上报消息


### _abstract property_ `id`

事件 ID


### _abstract property_ `name`

事件名称


### _abstract property_ `self_id`

机器人 ID


### _abstract property_ `time`

事件发生时间


### _abstract property_ `type`

事件主类型


### _abstract property_ `detail_type`

事件详细类型


### _abstract property_ `sub_type`

事件子类型


### _abstract property_ `user_id`

触发事件的主体 ID


### _abstract property_ `group_id`

触发事件的主体群 ID


### _abstract property_ `to_me`

事件是否为发送给机器人的消息


### _abstract property_ `message`

消息内容


### _abstract property_ `reply`

回复的消息


### _abstract property_ `raw_message`

原始消息


### _abstract property_ `plain_text`

纯文本消息


### _abstract property_ `sender`

消息发送者信息


## _class_ `BaseMessageSegment`

基类：`abc.ABC`

消息段基类


### `type`


* 类型: `str`


* 说明: 消息段类型


### `data`


* 类型: `Dict[str, Union[str, list]]`


* 说明: 消息段数据


## _class_ `BaseMessage`

基类：`list`, `abc.ABC`

消息数组


### `__init__(message=None, *args, **kwargs)`


* **参数**

    
    * `message: Union[str, dict, list, MessageSegment, Message]`: 消息内容



### `append(obj)`


* **说明**

    添加一个消息段到消息数组末尾



* **参数**

    
    * `obj: Union[str, MessageSegment]`: 要添加的消息段



### `extend(obj)`


* **说明**

    拼接一个消息数组或多个消息段到消息数组末尾



* **参数**

    
    * `obj: Union[Message, Iterable[MessageSegment]]`: 要添加的消息数组



### `reduce()`


* **说明**

    缩减消息数组，即拼接相邻纯文本消息段



### `extract_plain_text()`


* **说明**

    提取消息内纯文本消息
