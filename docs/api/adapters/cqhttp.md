---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.cqhttp 模块

## CQHTTP (OneBot) v11 协议适配

协议详情请看: [CQHTTP](http://cqhttp.cc/) | [OneBot](https://github.com/howmanybots/onebot)


## `log(level, message)`


* **说明**

    用于打印 CQHTTP 日志。



* **参数**

    
    * `level: str`: 日志等级


    * `message: str`: 日志信息



## `escape(s, *, escape_comma=True)`


* **说明**

    对字符串进行 CQ 码转义。



* **参数**

    
    * `s: str`: 需要转义的字符串


    * `escape_comma: bool`: 是否转义逗号（`,`）。



## `unescape(s)`


* **说明**

    对字符串进行 CQ 码去转义。



* **参数**

    
    * `s: str`: 需要转义的字符串



## `_b2s(b)`

转换布尔值为字符串。


## _async_ `_check_reply(bot, event)`


* **说明**

    检查消息中存在的回复，去除并赋值 `event.reply`, `event.to_me`



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象



## `_check_at_me(bot, event)`


* **说明**

    检查消息开头或结尾是否存在 @机器人，去除并赋值 `event.to_me`



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象



## `_check_nickname(bot, event)`


* **说明**

    检查消息开头是否存在，去除并赋值 `event.to_me`



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象



## `_handle_api_result(result)`


* **说明**

    处理 API 请求返回值。



* **参数**

    
    * `result: Optional[Dict[str, Any]]`: API 返回数据



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `ActionFailed`: API 调用失败



## _class_ `Bot`

基类：[`nonebot.adapters.BaseBot`](#None)

CQHTTP 协议 Bot 适配。继承属性参考 [BaseBot](./#class-basebot) 。


### _property_ `type`


* 返回: `"cqhttp"`


### _async_ `handle_message(message)`


* **说明**

    调用 [_check_reply](#async-check-reply-bot-event), [_check_at_me](#check-at-me-bot-event), [_check_nickname](#check-nickname-bot-event) 处理事件并转换为 [Event](#class-event)



### _async_ `call_api(api, **data)`


* **说明**

    调用 CQHTTP 协议 API



* **参数**

    
    * `api: str`: API 名称


    * `**data: Any`: API 参数



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `NetworkError`: 网络错误


    * `ActionFailed`: API 调用失败



### _async_ `send(event, message, at_sender=False, **kwargs)`


* **说明**

    根据 `event`  向触发事件的主体发送消息。



* **参数**

    
    * `event: Event`: Event 对象


    * `message: Union[str, Message, MessageSegment]`: 要发送的消息


    * `at_sender: bool`: 是否 @ 事件主体


    * `**kwargs`: 覆盖默认参数



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `ValueError`: 缺少 `user_id`, `group_id`


    * `NetworkError`: 网络错误


    * `ActionFailed`: API 调用失败



## _class_ `Event`

基类：[`nonebot.adapters.BaseEvent`](#None)

CQHTTP 协议 Event 适配。继承属性参考 [BaseEvent](./#class-baseevent) 。


### _property_ `id`


* 类型: `Optional[int]`


* 说明: 事件/消息 ID


### _property_ `name`


* 类型: `str`


* 说明: 事件名称，由类型与 `.` 组合而成


### _property_ `self_id`


* 类型: `str`


* 说明: 机器人自身 ID


### _property_ `time`


* 类型: `int`


* 说明: 事件发生时间


### _property_ `type`


* 类型: `str`


* 说明: 事件类型


### _property_ `detail_type`


* 类型: `str`


* 说明: 事件详细类型


### _property_ `sub_type`


* 类型: `Optional[str]`


* 说明: 事件子类型


### _property_ `user_id`


* 类型: `Optional[int]`


* 说明: 事件主体 ID


### _property_ `group_id`


* 类型: `Optional[int]`


* 说明: 事件主体群 ID


### _property_ `to_me`


* 类型: `Optional[bool]`


* 说明: 消息是否与机器人相关


### _property_ `message`


* 类型: `Optional[Message]`


* 说明: 消息内容


### _property_ `reply`


* 类型: `Optional[dict]`


* 说明: 回复消息详情


### _property_ `raw_message`


* 类型: `Optional[str]`


* 说明: 原始消息


### _property_ `plain_text`


* 类型: `Optional[str]`


* 说明: 纯文本消息内容


### _property_ `sender`


* 类型: `Optional[dict]`


* 说明: 消息发送者信息


## _class_ `MessageSegment`

基类：[`nonebot.adapters.BaseMessageSegment`](#None)

CQHTTP 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


## _class_ `Message`

基类：[`nonebot.adapters.BaseMessage`](#None)

CQHTTP 协议 Message 适配。
