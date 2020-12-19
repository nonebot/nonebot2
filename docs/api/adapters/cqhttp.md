---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.cqhttp 模块


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



## _exception_ `CQHTTPAdapterException`

基类：[`nonebot.exception.AdapterException`](../exception.md#nonebot.exception.AdapterException)


## _exception_ `ActionFailed`

基类：[`nonebot.exception.ActionFailed`](../exception.md#nonebot.exception.ActionFailed), `nonebot.adapters.cqhttp.exception.CQHTTPAdapterException`


* **说明**

    API 请求返回错误信息。



* **参数**

    
    * `retcode: Optional[int]`: 错误码



## _exception_ `NetworkError`

基类：[`nonebot.exception.NetworkError`](../exception.md#nonebot.exception.NetworkError), `nonebot.adapters.cqhttp.exception.CQHTTPAdapterException`


* **说明**

    网络错误。



* **参数**

    
    * `retcode: Optional[int]`: 错误码



## _exception_ `ApiNotAvailable`

基类：[`nonebot.exception.ApiNotAvailable`](../exception.md#nonebot.exception.ApiNotAvailable), `nonebot.adapters.cqhttp.exception.CQHTTPAdapterException`


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

基类：[`nonebot.adapters.Bot`](README.md#nonebot.adapters.Bot)

CQHTTP 协议 Bot 适配。继承属性参考 [BaseBot](./#class-basebot) 。


### _property_ `type`


* 返回: `"cqhttp"`


### _async classmethod_ `check_permission(driver, connection_type, headers, body)`


* **说明**

    CQHTTP (OneBot) 协议鉴权。参考 [鉴权](https://github.com/howmanybots/onebot/blob/master/v11/specs/communication/authorization.md)



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



## _class_ `MessageSegment`

基类：[`nonebot.adapters.MessageSegment`](README.md#nonebot.adapters.MessageSegment)

CQHTTP 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


## _class_ `Message`

基类：[`nonebot.adapters.Message`](README.md#nonebot.adapters.Message)

CQHTTP 协议 Message 适配。


## _class_ `Event`

基类：[`nonebot.adapters.Event`](README.md#nonebot.adapters.Event)

CQHTTP 协议事件。各事件字段未列出部分参考 [CQHTTP 文档](https://github.com/howmanybots/onebot/blob/master/README.md)


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



## _class_ `MessageEvent`

基类：`nonebot.adapters.cqhttp.event.Event`

消息事件


### `to_me`


* **说明**

    消息是否与机器人有关



* **类型**

    `bool`



### `reply`


* **说明**

    消息中提取的回复消息，内容为 `get_msg` API 返回结果



* **类型**

    `Optional[Reply]`



### `get_event_name()`


* **说明**

    获取事件名称的方法。



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



## _class_ `PrivateMessageEvent`

基类：`nonebot.adapters.cqhttp.event.MessageEvent`

私聊消息


### `get_event_description()`


* **说明**

    获取事件描述的方法，通常为事件具体内容。



* **返回**

    
    * `str`



## _class_ `GroupMessageEvent`

基类：`nonebot.adapters.cqhttp.event.MessageEvent`

群消息


### `get_event_description()`


* **说明**

    获取事件描述的方法，通常为事件具体内容。



* **返回**

    
    * `str`



## _class_ `NoticeEvent`

基类：`nonebot.adapters.cqhttp.event.Event`

通知事件


### `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



## _class_ `GroupUploadNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群文件上传事件


## _class_ `GroupAdminNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群管理员变动


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `GroupDecreaseNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群成员减少事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `GroupIncreaseNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群成员增加事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `GroupBanNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群禁言事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `FriendAddNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

好友添加事件


## _class_ `GroupRecallNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

群消息撤回事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `FriendRecallNoticeEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

好友消息撤回事件


## _class_ `NotifyEvent`

基类：`nonebot.adapters.cqhttp.event.NoticeEvent`

提醒事件


## _class_ `PokeNotifyEvent`

基类：`nonebot.adapters.cqhttp.event.NotifyEvent`

戳一戳提醒事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `LuckyKingNotifyEvent`

基类：`nonebot.adapters.cqhttp.event.NotifyEvent`

群红包运气王提醒事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `HonorNotifyEvent`

基类：`nonebot.adapters.cqhttp.event.NotifyEvent`

群荣誉变更提醒事件


### `is_tome()`


* **说明**

    获取事件是否与机器人有关的方法。



* **返回**

    
    * `bool`



## _class_ `RequestEvent`

基类：`nonebot.adapters.cqhttp.event.Event`

请求事件


### `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



## _class_ `FriendRequestEvent`

基类：`nonebot.adapters.cqhttp.event.RequestEvent`

加好友请求事件


## _class_ `GroupRequestEvent`

基类：`nonebot.adapters.cqhttp.event.RequestEvent`

加群请求/邀请事件


## _class_ `MetaEvent`

基类：`nonebot.adapters.cqhttp.event.Event`

元事件


### `get_event_name()`


* **说明**

    获取事件名称的方法。



* **返回**

    
    * `str`



### `get_log_string()`


* **说明**

    获取事件日志信息的方法，通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 `NoLogException` 异常。



* **返回**

    
    * `str`



* **异常**

    
    * `NoLogException`



## _class_ `LifecycleMetaEvent`

基类：`nonebot.adapters.cqhttp.event.MetaEvent`

生命周期元事件


## _class_ `HeartbeatMetaEvent`

基类：`nonebot.adapters.cqhttp.event.MetaEvent`

心跳元事件


## `get_event_model(event_name)`


* **说明**

    根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表



* **返回**

    
    * `List[Type[Event]]`
