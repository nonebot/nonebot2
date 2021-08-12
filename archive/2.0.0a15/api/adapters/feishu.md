---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.feishu 模块

# NoneBot.adapters.feishu.config 模块


## _class_ `Config`

钉钉配置类


* **配置项**

    
    * `app_id` / `feishu_app_id`: 飞书开放平台后台“凭证与基础信息”处给出的 App ID


    * `app_secret` / `feishu_app_secret`: 飞书开放平台后台“凭证与基础信息”处给出的 App Secret


    * `encrypt_key` / `feishu_encrypt_key`: 飞书开放平台后台“事件订阅”处设置的 Encrypt Key


    * `verification_token` / `feishu_verification_token`: 飞书开放平台后台“事件订阅”处设置的 Verification Token


    * `tenant_access_token` / `feishu_tenant_access_token`: 请求飞书 API 后返回的租户密钥


# NoneBot.adapters.feishu.exception 模块


## _exception_ `ActionFailed`

基类：[`nonebot.exception.ActionFailed`](../exception.md#nonebot.exception.ActionFailed), `nonebot.adapters.feishu.exception.FeishuAdapterException`


* **说明**

    API 请求返回错误信息。



* **参数**

    
    * `retcode: Optional[int]`: 错误码



## _exception_ `NetworkError`

基类：[`nonebot.exception.NetworkError`](../exception.md#nonebot.exception.NetworkError), `nonebot.adapters.feishu.exception.FeishuAdapterException`


* **说明**

    网络错误。



* **参数**

    
    * `retcode: Optional[int]`: 错误码


# NoneBot.adapters.feishu.bot 模块


## `_check_at_me(bot, event)`


* **说明**

    检查消息开头或结尾是否存在 @机器人，去除并赋值 `event.reply`, `event.to_me`



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象



## `_check_nickname(bot, event)`


* **说明**

    检查消息开头是否存在昵称，去除并赋值 `event.to_me`



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

基类：[`nonebot.adapters._base.Bot`](README.md#nonebot.adapters._base.Bot)

飞书 协议 Bot 适配。继承属性参考 [BaseBot](./#class-basebot) 。


### _async_ `handle_message(message)`


* **说明**

    处理事件并转换为 [Event](#class-event)



### _async_ `call_api(api, **data)`


* **说明**

    调用 飞书 协议 API



* **参数**

    
    * `api: str`: API 名称


    * `**data: Any`: API 参数



* **返回**

    
    * `Any`: API 调用返回数据



* **异常**

    
    * `NetworkError`: 网络错误


    * `ActionFailed`: API 调用失败


# NoneBot.adapters.feishu.message 模块


## _class_ `MessageSegment`

基类：[`nonebot.adapters._base.MessageSegment`](README.md#nonebot.adapters._base.MessageSegment)[`Message`]

飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。


## _class_ `Message`

基类：[`nonebot.adapters._base.Message`](README.md#nonebot.adapters._base.Message)[`nonebot.adapters.feishu.message.MessageSegment`]

飞书 协议 Message 适配。


## _class_ `MessageSerializer`

基类：`object`

飞书 协议 Message 序列化器。


## _class_ `MessageDeserializer`

基类：`object`

飞书 协议 Message 反序列化器。

# NoneBot.adapters.feishu.event 模块


## _class_ `Event`

基类：[`nonebot.adapters._base.Event`](README.md#nonebot.adapters._base.Event)

飞书协议事件。各事件字段参考 [飞书文档](https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list)


## `get_event_model(event_name)`


* **说明**

    根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表



* **返回**

    
    * `List[Type[Event]]`
