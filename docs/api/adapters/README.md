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
await bot.call_api("send_msg", data={"message": "hello world"})
await bot.send_msg(message="hello world")
```


### _abstract async_ `send(*args, **kwargs)`


* **说明**

    调用机器人基础发送消息接口



* **参数**

    
    * `*args`


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


## _class_ `BaseMessage`

基类：`list`, `abc.ABC`


### `__init__(message=None, *args, **kwargs)`

Initialize self.  See help(type(self)) for accurate signature.


### `append(obj)`

Append object to the end of the list.


### `extend(obj)`

Extend list by appending elements from the iterable.
