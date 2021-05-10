---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters 模块

## 协议适配基类

各协议请继承以下基类，并使用 `driver.register_adapter` 注册适配器


## _class_ `Bot`

基类：`abc.ABC`

Bot 基类。用于处理上报消息，并提供 API 调用接口。


### `driver`

Driver 对象


### `config`

Config 配置对象


### `_calling_api_hook`


* **类型**

    `Set[T_CallingAPIHook]`



* **说明**

    call_api 时执行的函数



### `_called_api_hook`


* **类型**

    `Set[T_CalledAPIHook]`



* **说明**

    call_api 后执行的函数



### _abstract_ `__init__(connection_type, self_id, *, websocket=None)`


* **参数**

    
    * `connection_type: str`: http 或者 websocket


    * `self_id: str`: 机器人 ID


    * `websocket: Optional[WebSocket]`: Websocket 连接对象



### `connection_type`

连接类型


### `self_id`

机器人 ID


### `websocket`

Websocket 连接对象


### _abstract property_ `type`

Adapter 类型


### _classmethod_ `register(driver, config)`


* **说明**

    register 方法会在 driver.register_adapter 时被调用，用于初始化相关配置



### _abstract async classmethod_ `check_permission(driver, connection_type, headers, body)`


* **说明**

    检查连接请求是否合法的函数，如果合法则返回当前连接 `唯一标识符`，通常为机器人 ID；如果不合法则抛出 `RequestDenied` 异常。



* **参数**

    
    * `driver: Driver`: Driver 对象


    * `connection_type: str`: 连接类型


    * `headers: dict`: 请求头


    * `body: Optional[bytes]`: 请求数据，WebSocket 连接该部分为 None



* **返回**

    
    * `str`: 连接唯一标识符



* **异常**

    
    * `RequestDenied`: 请求非法



### _abstract async_ `handle_message(message)`


* **说明**

    处理上报消息的函数，转换为 `Event` 事件后调用 `nonebot.message.handle_event` 进一步处理事件。



* **参数**

    
    * `message: dict`: 收到的上报消息



### _abstract async_ `_call_api(api, **data)`


* **说明**

    `adapter` 实际调用 api 的逻辑实现函数，实现该方法以调用 api。



* **参数**

    
    * `api: str`: API 名称


    * `**data`: API 数据



### _async_ `call_api(api, **data)`


* **说明**

    调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用



* **参数**

    
    * `api: str`: API 名称


    * `self_id: Optional[str]`: 指定调用 API 的机器人


    * `**data`: API 数据



* **示例**


```python
await bot.call_api("send_msg", message="hello world")
await bot.send_msg(message="hello world")
```


### _abstract async_ `send(event, message, **kwargs)`


* **说明**

    调用机器人基础发送消息接口



* **参数**

    
    * `event: Event`: 上报事件


    * `message: Union[str, Message, MessageSegment]`: 要发送的消息


    * `**kwargs`



## _class_ `MessageSegment`

基类：`abc.ABC`, `Mapping`

消息段基类


### `type`


* 类型: `str`


* 说明: 消息段类型


### `data`


* 类型: `Dict[str, Union[str, list]]`


* 说明: 消息段数据


## _class_ `Message`

基类：`List`[`nonebot.adapters._base.T_MessageSegment`], `abc.ABC`

消息数组


### `__init__(message=None, *args, **kwargs)`


* **参数**

    
    * `message: Union[str, list, dict, MessageSegment, Message, Any]`: 消息内容



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

    缩减消息数组，即按 MessageSegment 的实现拼接相邻消息段



### `extract_plain_text()`


* **说明**

    提取消息内纯文本消息



## _class_ `Event`

基类：`abc.ABC`, `pydantic.main.BaseModel`

Event 基类。提供获取关键信息的方法，其余信息可直接获取。


### _abstract_ `get_type()`


* **说明**

    获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。



* **返回**

    
    * `Literal["message", "notice", "request", "meta_event"]`


    * 其他自定义 `str`



### _abstract_ `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



### _abstract_ `get_event_description()`


* **说明**

    获取事件描述的方法，通常为事件具体内容。



* **返回**

    
    * `str`



### `get_log_string()`


* **说明**

    获取事件日志信息的方法，通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 `NoLogException` 异常。



* **返回**

    
    * `str`



* **异常**

    
    * `NoLogException`



### _abstract_ `get_user_id()`


* **说明**

    获取事件主体 id 的方法，通常是用户 id 。



* **返回**

    
    * `str`



### _abstract_ `get_session_id()`


* **说明**

    获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。



* **返回**

    
    * `str`



### _abstract_ `get_message()`


* **说明**

    获取事件消息内容的方法。



* **返回**

    
    * `Message`



### `get_plaintext()`


* **说明**

    获取消息纯文本的方法，通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。



* **返回**

    
    * `str`



### _abstract_ `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`
