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

基类：`nonebot.adapters.ding.exception.ApiNotAvailable`, `nonebot.adapters.ding.exception.DingAdapterException`


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



### _async_ `handle_message(message)`


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

钉钉 协议 Event 适配。各事件字段参考 [钉钉文档](https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p)


### `get_type()`


* **说明**

    获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。



* **返回**

    
    * `Literal["message", "notice", "request", "meta_event"]`



### `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



### `get_event_description()`


* **说明**

    获取事件描述的方法，通常为事件具体内容。



* **返回**

    
    * `str`



### `get_message()`


* **说明**

    获取事件消息内容的方法。



* **返回**

    
    * `Message`



### `get_plaintext()`


* **说明**

    获取消息纯文本的方法，通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。



* **返回**

    
    * `str`



### `get_user_id()`


* **说明**

    获取事件主体 id 的方法，通常是用户 id 。



* **返回**

    
    * `str`



### `get_session_id()`


* **说明**

    获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。



* **返回**

    
    * `str`



### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `ConversationType`

基类：`str`, `enum.Enum`

An enumeration.


### `_member_type_`

`builtins.str` 的别名


## _class_ `MessageEvent`

基类：`nonebot.adapters.ding.event.Event`


### `get_type()`


* **说明**

    获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。



* **返回**

    
    * `Literal["message", "notice", "request", "meta_event"]`



### `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



### `get_event_description()`


* **说明**

    获取事件描述的方法，通常为事件具体内容。



* **返回**

    
    * `str`



### `get_message()`


* **说明**

    获取事件消息内容的方法。



* **返回**

    
    * `Message`



### `get_plaintext()`


* **说明**

    获取消息纯文本的方法，通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。



* **返回**

    
    * `str`



### `get_user_id()`


* **说明**

    获取事件主体 id 的方法，通常是用户 id 。



* **返回**

    
    * `str`



### `get_session_id()`


* **说明**

    获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。



* **返回**

    
    * `str`



## _class_ `PrivateMessageEvent`

基类：`nonebot.adapters.ding.event.MessageEvent`


## _class_ `GroupMessageEvent`

基类：`nonebot.adapters.ding.event.MessageEvent`


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `MessageSegment`

基类：[`nonebot.adapters.MessageSegment`](README.md#nonebot.adapters.MessageSegment)

钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


### _static_ `extension(dict_)`

"标记 text 文本的 extension 属性，需要与 text 消息段相加。


### _static_ `actionCardMultiBtns(title, text, btns, hideAvatar=False, btnOrientation='1')`


* **参数**

    
    * `btnOrientation`: 0：按钮竖直排列 1：按钮横向排列


    * `btns`: [{ "title": title, "actionURL": actionURL }, ...]



### _static_ `feedCard(links)`


* **参数**

    
    * `links`: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]



## _class_ `Message`

基类：[`nonebot.adapters.Message`](README.md#nonebot.adapters.Message)

钉钉 协议 Message 适配。
