---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.ding 模块


## _exception_ `DingAdapterException`

基类：[`nonebot.exception.AdapterException`](../exception.md#nonebot.exception.AdapterException)


* **说明**

    钉钉 Adapter 错误基类



## _exception_ `ActionFailed`

基类：[`nonebot.exception.ActionFailed`](../exception.md#nonebot.exception.ActionFailed), `nonebot.adapters.ding.exception.DingAdapterException`


* **说明**

    API 请求返回错误信息。



* **参数**

    
    * `errcode: Optional[int]`: 错误码


    * `errmsg: Optional[str]`: 错误信息



## _exception_ `ApiNotAvailable`

基类：[`nonebot.exception.ApiNotAvailable`](../exception.md#nonebot.exception.ApiNotAvailable), `nonebot.adapters.ding.exception.DingAdapterException`


## _exception_ `NetworkError`

基类：[`nonebot.exception.NetworkError`](../exception.md#nonebot.exception.NetworkError), `nonebot.adapters.ding.exception.DingAdapterException`


* **说明**

    网络错误。



* **参数**

    
    * `retcode: Optional[int]`: 错误码



## _exception_ `SessionExpired`

基类：[`nonebot.exception.ApiNotAvailable`](../exception.md#nonebot.exception.ApiNotAvailable), `nonebot.adapters.ding.exception.DingAdapterException`


* **说明**

    发消息的 session 已经过期。



## _class_ `Bot`

基类：[`nonebot.adapters.Bot`](README.md#nonebot.adapters.Bot)

钉钉 协议 Bot 适配。继承属性参考 [BaseBot](./#class-basebot) 。


### _property_ `type`


* 返回: `"ding"`


### _async classmethod_ `check_permission(driver, connection_type, headers, body)`


* **说明**

    钉钉协议鉴权。参考 [鉴权](https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p)



### _async_ `handle_message(body)`


* **说明**

    处理上报消息的函数，转换为 `Event` 事件后调用 `nonebot.message.handle_event` 进一步处理事件。



* **参数**

    
    * `message: dict`: 收到的上报消息



### _async_ `call_api(api, event=None, **data)`


* **说明**

    调用 钉钉 协议 API



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

基类：[`nonebot.adapters.Event`](README.md#nonebot.adapters.Event)

钉钉 协议 Event 适配。继承属性参考 [BaseEvent](./#class-baseevent) 。


### _property_ `raw_event`

原始上报消息


### _property_ `id`


* 类型: `Optional[str]`


* 说明: 消息 ID


### _property_ `name`


* 类型: `str`


* 说明: 事件名称，由 type.\`detail_type\` 组合而成


### _property_ `self_id`


* 类型: `str`


* 说明: 机器人自身 ID


### _property_ `time`


* 类型: `int`


* 说明: 消息的时间戳，单位 s


### _property_ `type`


* 类型: `str`


* 说明: 事件类型


### _property_ `detail_type`


* 类型: `str`


* 说明: 事件详细类型


### _property_ `sub_type`


* 类型: `None`


* 说明: 钉钉适配器无事件子类型


### _property_ `user_id`


* 类型: `Optional[str]`


* 说明: 发送者 ID


### _property_ `group_id`


* 类型: `Optional[str]`


* 说明: 事件主体群 ID


### _property_ `to_me`


* 类型: `Optional[bool]`


* 说明: 消息是否与机器人相关


### _property_ `message`


* 类型: `Optional[Message]`


* 说明: 消息内容


### _property_ `reply`


* 类型: `None`


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

基类：[`nonebot.adapters.MessageSegment`](README.md#nonebot.adapters.MessageSegment)

钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


### _static_ `actionCardSingleMultiBtns(title, text, btns=[], hideAvatar=False, btnOrientation='1')`


* **参数**

    
    * `btnOrientation`: 0：按钮竖直排列 1：按钮横向排列


    * `btns`: [{ "title": title, "actionURL": actionURL }, ...]



### _static_ `feedCard(links=[])`


* **参数**

    
    * `links`: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]



### _static_ `empty()`

不想回复消息到群里


## _class_ `Message`

基类：[`nonebot.adapters.Message`](README.md#nonebot.adapters.Message)

钉钉 协议 Message 适配。
