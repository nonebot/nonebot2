---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.ding 模块

## 钉钉群机器人 协议适配

协议详情请看: [钉钉文档](https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p)

# NoneBot.adapters.ding.config 模块


## _class_ `Config`

钉钉配置类


* **配置项**

    
    * `access_token` / `ding_access_token`: 钉钉令牌


    * `secret` / `ding_secret`: 钉钉 HTTP 上报数据签名口令


# NoneBot.adapters.ding.exception 模块


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


# NoneBot.adapters.ding.bot 模块


## _class_ `Bot`

基类：[`nonebot.adapters._base.Bot`](README.md#nonebot.adapters._base.Bot)

钉钉 协议 Bot 适配。继承属性参考 [BaseBot](./#class-basebot) 。


### _property_ `type`


* 返回: `"ding"`


### _async classmethod_ `check_permission(driver, connection_type, headers, body)`


* **说明**

    钉钉协议鉴权。参考 [鉴权](https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p)



### _async_ `call_api(api, event=None, **data)`


* **说明**

    调用 钉钉 协议 API



* **参数**

    
    * `api: str`: API 名称


    * `event: Optional[MessageEvent]`: Event 对象


    * `**data: Any`: API 参数



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `NetworkError`: 网络错误


    * `ActionFailed`: API 调用失败



### _async_ `send(event, message, at_sender=False, webhook=None, secret=None, **kwargs)`


* **说明**

    根据 `event`  向触发事件的主体发送消息。



* **参数**

    
    * `event: Event`: Event 对象


    * `message: Union[str, Message, MessageSegment]`: 要发送的消息


    * `at_sender: bool`: 是否 @ 事件主体


    * `webhook: Optional[str]`: 该条消息将调用的 webhook 地址。不传则将使用 sessionWebhook，若其也不存在，该条消息不发送，使用自定义 webhook 时注意你设置的安全方式，如加关键词，IP地址，加签等等。


    * `secret: Optional[str]`: 如果你使用自定义的 webhook 地址，推荐使用加签方式对消息进行验证，将 机器人安全设置页面，加签一栏下面显示的SEC开头的字符串 传入这个参数即可。


    * `**kwargs`: 覆盖默认参数



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `ValueError`: 缺少 `user_id`, `group_id`


    * `NetworkError`: 网络错误


    * `ActionFailed`: API 调用失败


# NoneBot.adapters.ding.message 模块


## _class_ `MessageSegment`

基类：`abc.ABC`, `Mapping`

钉钉 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


### _static_ `atAll()`

@全体


### _static_ `atMobiles(*mobileNumber)`

@指定手机号人员


### _static_ `atDingtalkIds(*dingtalkIds)`

@指定 id，@ 默认会在消息段末尾。
所以你可以在消息中使用 @{senderId} 占位，发送出去之后 @ 就会出现在占位的位置：
``python
message = MessageSegment.text(f"@{event.senderId}，你好")
message += MessageSegment.atDingtalkIds(event.senderId)
``


### _static_ `text(text)`

发送 `text` 类型消息


### _static_ `image(picURL)`

发送 `image` 类型消息


### _static_ `extension(dict_)`

"标记 text 文本的 extension 属性，需要与 text 消息段相加。


### _static_ `code(code_language, code)`

"发送 code 消息段


### _static_ `markdown(title, text)`

发送 `markdown` 类型消息


### _static_ `actionCardSingleBtn(title, text, singleTitle, singleURL)`

发送 `actionCardSingleBtn` 类型消息


### _static_ `actionCardMultiBtns(title, text, btns, hideAvatar=False, btnOrientation='1')`

发送 `actionCardMultiBtn` 类型消息


* **参数**

    
    * `btnOrientation`: 0：按钮竖直排列 1：按钮横向排列


    * `btns`: [{ "title": title, "actionURL": actionURL }, ...]



### _static_ `feedCard(links)`

发送 `feedCard` 类型消息


* **参数**

    
    * `links`: [{ "title": xxx, "messageURL": xxx, "picURL": xxx }, ...]



## _class_ `Message`

基类：[`nonebot.adapters._base.Message`](README.md#nonebot.adapters._base.Message)[`nonebot.adapters.ding.message.MessageSegment`]

钉钉 协议 Message 适配。

# NoneBot.adapters.ding.event 模块


## _class_ `Event`

基类：[`nonebot.adapters._base.Event`](README.md#nonebot.adapters._base.Event)

钉钉协议事件。各事件字段参考 [钉钉文档](https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p)


## _class_ `ConversationType`

基类：`str`, `enum.Enum`

An enumeration.


## _class_ `MessageEvent`

基类：`nonebot.adapters.ding.event.Event`

消息事件


## _class_ `PrivateMessageEvent`

基类：`nonebot.adapters.ding.event.MessageEvent`

私聊消息事件


## _class_ `GroupMessageEvent`

基类：`nonebot.adapters.ding.event.MessageEvent`

群消息事件
