---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.adapters.mirai 模块

## Mirai-API-HTTP 协议适配

协议详情请看: [mirai-api-http 文档](https://github.com/project-mirai/mirai-api-http/tree/master/docs)

::: tip
该Adapter目前仍然处在早期实验性阶段, 并未经过充分测试

如果你在使用过程中遇到了任何问题, 请前往 [Issue页面](https://github.com/nonebot/nonebot2/issues) 为我们提供反馈
:::

::: danger
Mirai-API-HTTP 的适配器以 [AGPLv3许可](https://opensource.org/licenses/AGPL-3.0) 单独开源

这意味着在使用该适配器时需要 **以该许可开源您的完整程序代码**
:::

# NoneBot.adapters.mirai.config 模块


## _class_ `Config`

Mirai 配置类


* **必填**

    
    * `auth_key` / `mirai_auth_key`: mirai-api-http 的 auth_key


    * `mirai_host`: mirai-api-http 的地址


    * `mirai_port`: mirai-api-http 的端口


# NoneBot.adapters.mirai.bot 模块


## _class_ `SessionManager`

基类：`object`

Bot会话管理器, 提供API主动调用接口


### _async_ `post(path, *, params=None)`


* **说明**

    以POST方式主动提交API请求



* **参数**

    
    * `path: str`: 对应API路径


    * `params: Optional[Dict[str, Any]]`: 请求参数 (无需sessionKey)



* **返回**

    
    * `Dict[str, Any]`: API 返回值



### _async_ `request(path, *, params=None)`


* **说明**

    以GET方式主动提交API请求



* **参数**

    
    * `path: str`: 对应API路径


    * `params: Optional[Dict[str, Any]]`: 请求参数 (无需sessionKey)



### _async_ `upload(path, *, params)`


* **说明**

    以表单(`multipart/form-data`)形式主动提交API请求



* **参数**

    
    * `path: str`: 对应API路径


    * `params: Dict[str, Any]`: 请求参数 (无需sessionKey)



## _class_ `Bot`

基类：[`nonebot.adapters._base.Bot`](README.md#nonebot.adapters._base.Bot)

mirai-api-http 协议 Bot 适配。

::: warning
API中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

部分字段可能与文档在符号上不一致
:::


### _property_ `api`

返回该Bot对象的会话管理实例以提供API主动调用


### _async_ `call_api(api, **data)`

::: danger
由于Mirai的HTTP API特殊性, 该API暂时无法实现
:::

::: tip
你可以使用 `MiraiBot.api` 中提供的调用方法来代替
:::


### `send(event, message, at_sender=False)`


* **说明**

    根据 `event` 向触发事件的主体发送信息



* **参数**

    
    * `event: Event`: Event对象


    * `message: Union[MessageChain, MessageSegment, str]`: 要发送的消息


    * `at_sender: bool`: 是否 @ 事件主体



### `send_friend_message(target, message_chain)`


* **说明**

    使用此方法向指定好友发送消息



* **参数**

    
    * `target: int`: 发送消息目标好友的 QQ 号


    * `message_chain: MessageChain`: 消息链，是一个消息对象构成的数组



### `send_temp_message(qq, group, message_chain)`


* **说明**

    使用此方法向临时会话对象发送消息



* **参数**

    
    * `qq: int`: 临时会话对象 QQ 号


    * `group: int`: 临时会话群号


    * `message_chain: MessageChain`: 消息链，是一个消息对象构成的数组



### `send_group_message(group, message_chain, quote=None)`


* **说明**

    使用此方法向指定群发送消息



* **参数**

    
    * `group: int`: 发送消息目标群的群号


    * `message_chain: MessageChain`: 消息链，是一个消息对象构成的数组


    * `quote: Optional[int]`: 引用一条消息的 message_id 进行回复



### `recall(target)`


* **说明**

    使用此方法撤回指定消息。对于bot发送的消息，有2分钟时间限制。对于撤回群聊中群员的消息，需要有相应权限



* **参数**

    
    * `target: int`: 需要撤回的消息的message_id



### `send_image_message(target, qq, group, urls)`


* **说明**

    使用此方法向指定对象（群或好友）发送图片消息
    除非需要通过此手段获取image_id，否则不推荐使用该接口

    > 当qq和group同时存在时，表示发送临时会话图片，qq为临时会话对象QQ号，group为临时会话发起的群号



* **参数**

    
    * `target: int`: 发送对象的QQ号或群号，可能存在歧义


    * `qq: int`: 发送对象的QQ号


    * `group: int`: 发送对象的群号


    * `urls: List[str]`: 是一个url字符串构成的数组



* **返回**

    
    * `List[str]`: 一个包含图片imageId的数组



### `upload_image(type, img)`


* **说明**

    使用此方法上传图片文件至服务器并返回Image_id



* **参数**

    
    * `type: str`: "friend" 或 "group" 或 "temp"


    * `img: BytesIO`: 图片的BytesIO对象



### `upload_voice(type, voice)`


* **说明**

    使用此方法上传语音文件至服务器并返回voice_id



* **参数**

    
    * `type: str`: 当前仅支持 "group"


    * `voice: BytesIO`: 语音的BytesIO对象



### `fetch_message(count=10)`


* **说明**

    使用此方法获取bot接收到的最老消息和最老各类事件
    (会从MiraiApiHttp消息记录中删除)



* **参数**

    
    * `count: int`: 获取消息和事件的数量



### `fetch_latest_message(count=10)`


* **说明**

    使用此方法获取bot接收到的最新消息和最新各类事件
    (会从MiraiApiHttp消息记录中删除)



* **参数**

    
    * `count: int`: 获取消息和事件的数量



### `peek_message(count=10)`


* **说明**

    使用此方法获取bot接收到的最老消息和最老各类事件
    (不会从MiraiApiHttp消息记录中删除)



* **参数**

    
    * `count: int`: 获取消息和事件的数量



### `peek_latest_message(count=10)`


* **说明**

    使用此方法获取bot接收到的最新消息和最新各类事件
    (不会从MiraiApiHttp消息记录中删除)



* **参数**

    
    * `count: int`: 获取消息和事件的数量



### `messsage_from_id(id)`


* **说明**

    通过messageId获取一条被缓存的消息
    使用此方法获取bot接收到的消息和各类事件



* **参数**

    
    * `id: int`: 获取消息的message_id



### `count_message()`


* **说明**

    使用此方法获取bot接收并缓存的消息总数，注意不包含被删除的



### `friend_list()`


* **说明**

    使用此方法获取bot的好友列表



* **返回**

    
    * `List[Dict[str, Any]]`: 返回的好友列表数据



### `group_list()`


* **说明**

    使用此方法获取bot的群列表



* **返回**

    
    * `List[Dict[str, Any]]`: 返回的群列表数据



### `member_list(target)`


* **说明**

    使用此方法获取bot指定群种的成员列表



* **参数**

    
    * `target: int`: 指定群的群号



* **返回**

    
    * `List[Dict[str, Any]]`: 返回的群成员列表数据



### `mute(target, member_id, time)`


* **说明**

    使用此方法指定群禁言指定群员（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号


    * `member_id: int`: 指定群员QQ号


    * `time: int`: 禁言时长，单位为秒，最多30天



### `unmute(target, member_id)`


* **说明**

    使用此方法指定群解除群成员禁言（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号


    * `member_id: int`: 指定群员QQ号



### `kick(target, member_id, msg)`


* **说明**

    使用此方法移除指定群成员（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号


    * `member_id: int`: 指定群员QQ号


    * `msg: str`: 信息



### `quit(target)`


* **说明**

    使用此方法使Bot退出群聊



* **参数**

    
    * `target: int`: 退出的群号



### `mute_all(target)`


* **说明**

    使用此方法令指定群进行全体禁言（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号



### `unmute_all(target)`


* **说明**

    使用此方法令指定群解除全体禁言（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号



### `group_config(target)`


* **说明**

    使用此方法获取群设置



* **参数**

    
    * `target: int`: 指定群的群号



* **返回**


```json
{
    "name": "群名称",
    "announcement": "群公告",
    "confessTalk": true,
    "allowMemberInvite": true,
    "autoApprove": true,
    "anonymousChat": true
}
```


### `modify_group_config(target, config)`


* **说明**

    使用此方法修改群设置（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号


    * `config: Dict[str, Any]`: 群设置, 格式见 `group_config` 的返回值



### `member_info(target, member_id)`


* **说明**

    使用此方法获取群员资料



* **参数**

    
    * `target: int`: 指定群的群号


    * `member_id: int`: 群员QQ号



* **返回**


```json
{
    "name": "群名片",
    "specialTitle": "群头衔"
}
```


### `modify_member_info(target, member_id, info)`


* **说明**

    使用此方法修改群员资料（需要有相关权限）



* **参数**

    
    * `target: int`: 指定群的群号


    * `member_id: int`: 群员QQ号


    * `info: Dict[str, Any]`: 群员资料, 格式见 `member_info` 的返回值


# NoneBot.adapters.mirai.bot_ws 模块


## _class_ `WebsocketBot`

基类：`nonebot.adapters.mirai.bot.Bot`

mirai-api-http 正向 Websocket 协议 Bot 适配。


### _classmethod_ `register(driver, config, qq)`


* **说明**

    注册该Adapter



* **参数**

    
    * `driver: Driver`: 程序所使用的\`\`Driver\`\`


    * `config: Config`: 程序配置对象


    * `qq: int`: 要使用的Bot的QQ号 **注意: 在使用正向Websocket时必须指定该值!**


# NoneBot.adapters.mirai.message 模块


## _class_ `MessageType`

基类：`str`, `enum.Enum`

消息类型枚举类


## _class_ `MessageSegment`

基类：`abc.ABC`, `Mapping`

Mirai-API-HTTP 协议 MessageSegment 适配。具体方法参考 [mirai-api-http 消息类型](https://github.com/project-mirai/mirai-api-http/blob/master/docs/MessageType.md)


### `as_dict()`

导出可以被正常json序列化的结构体


### _classmethod_ `quote(id, group_id, sender_id, target_id, origin)`


* **说明**

    生成回复引用消息段



* **参数**

    
    * `id: int`: 被引用回复的原消息的message_id


    * `group_id: int`: 被引用回复的原消息所接收的群号，当为好友消息时为0


    * `sender_id: int`: 被引用回复的原消息的发送者的QQ号


    * `target_id: int`: 被引用回复的原消息的接收者者的QQ号（或群号）


    * `origin: MessageChain`: 被引用回复的原消息的消息链对象



### _classmethod_ `at(target)`


* **说明**

    @某个人



* **参数**

    
    * `target: int`: 群员QQ号



### _classmethod_ `at_all()`


* **说明**

    @全体成员



### _classmethod_ `face(face_id=None, name=None)`


* **说明**

    发送QQ表情



* **参数**

    
    * `face_id: Optional[int]`: QQ表情编号，可选，优先高于name


    * `name: Optional[str]`: QQ表情拼音，可选



### _classmethod_ `plain(text)`


* **说明**

    纯文本消息



* **参数**

    
    * `text: str`: 文字消息



### _classmethod_ `image(image_id=None, url=None, path=None)`


* **说明**

    图片消息



* **参数**

    
    * `image_id: Optional[str]`: 图片的image_id，群图片与好友图片格式不同。不为空时将忽略url属性


    * `url: Optional[str]`: 图片的URL，发送时可作网络图片的链接


    * `path: Optional[str]`: 图片的路径，发送本地图片



### _classmethod_ `flash_image(image_id=None, url=None, path=None)`


* **说明**

    闪照消息



* **参数**

    同 `image`



### _classmethod_ `voice(voice_id=None, url=None, path=None)`


* **说明**

    语音消息



* **参数**

    
    * `voice_id: Optional[str]`: 语音的voice_id，不为空时将忽略url属性


    * `url: Optional[str]`: 语音的URL，发送时可作网络语音的链接


    * `path: Optional[str]`: 语音的路径，发送本地语音



### _classmethod_ `xml(xml)`


* **说明**

    XML消息



* **参数**

    
    * `xml: str`: XML文本



### _classmethod_ `json(json)`


* **说明**

    Json消息



* **参数**

    
    * `json: str`: Json文本



### _classmethod_ `app(content)`


* **说明**

    应用程序消息



* **参数**

    
    * `content: str`: 内容



### _classmethod_ `poke(name)`


* **说明**

    戳一戳消息



* **参数**

    
    * `name: str`: 戳一戳的类型


        * `Poke`: 戳一戳


        * `ShowLove`: 比心


        * `Like`: 点赞


        * `Heartbroken`: 心碎


        * `SixSixSix`: 666


        * `FangDaZhao`: 放大招



## _class_ `MessageChain`

基类：[`nonebot.adapters._base.Message`](README.md#nonebot.adapters._base.Message)[`nonebot.adapters.mirai.message.MessageSegment`]

Mirai 协议 Message 适配

由于Mirai协议的Message实现较为特殊, 故使用MessageChain命名


### `reduce()`


* **说明**

    忽略为空的消息段, 合并相邻的纯文本消息段



### `export()`

导出为可以被正常json序列化的数组


### `extract_first(*type)`


* **说明**

    弹出该消息链的第一个消息



* **参数**

    
    * \*type: MessageType: 指定的消息类型, 当指定后如类型不匹配不弹出


# NoneBot.adapters.mirai.utils 模块


## _exception_ `ActionFailed`

基类：[`nonebot.exception.ActionFailed`](../exception.md#nonebot.exception.ActionFailed)


* **说明**

    API 请求成功返回数据，但 API 操作失败。



## _exception_ `InvalidArgument`

基类：[`nonebot.exception.AdapterException`](../exception.md#nonebot.exception.AdapterException)


* **说明**

    调用API的参数出错



## `catch_network_error(function)`


* **说明**

    捕捉函数抛出的httpx网络异常并释放 `NetworkError` 异常

    处理返回数据, 在code不为0时释放 `ActionFailed` 异常


::: warning
此装饰器只支持使用了httpx的异步函数
:::


## `argument_validation(function)`


* **说明**

    通过函数签名中的类型注解来对传入参数进行运行时校验

    会在参数出错时释放 `InvalidArgument` 异常


# NoneBot.adapters.mirai.event 模块

::: warning 
事件中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

部分字段可能与文档在符号上不一致
:::


## _class_ `Event`

基类：[`nonebot.adapters._base.Event`](README.md#nonebot.adapters._base.Event)

mirai-api-http 协议事件，字段与 mirai-api-http 一致。各事件字段参考 [mirai-api-http 事件类型](https://github.com/project-mirai/mirai-api-http/blob/master/docs/EventType.md)


### _classmethod_ `new(data)`

此事件类的工厂函数, 能够通过事件数据选择合适的子类进行序列化


### `normalize_dict(**kwargs)`

返回可以被json正常反序列化的结构体


## _class_ `UserPermission`

基类：`str`, `enum.Enum`


* **说明**


用户权限枚举类

> 
> * `OWNER`: 群主


> * `ADMINISTRATOR`: 群管理


> * `MEMBER`: 普通群成员


## _class_ `MessageEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

消息事件基类


## _class_ `GroupMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

群消息事件


## _class_ `FriendMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

好友消息事件


## _class_ `TempMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

临时会话消息事件


## _class_ `NoticeEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

通知事件基类


## _class_ `MuteEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

禁言类事件基类


## _class_ `BotMuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

Bot被禁言


## _class_ `BotUnmuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

Bot被取消禁言


## _class_ `MemberMuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

群成员被禁言事件（该成员不是Bot）


## _class_ `MemberUnmuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

群成员被取消禁言事件（该成员不是Bot）


## _class_ `BotJoinGroupEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

Bot加入了一个新群


## _class_ `BotLeaveEventActive`

基类：`nonebot.adapters.mirai.event.notice.BotJoinGroupEvent`

Bot主动退出一个群


## _class_ `BotLeaveEventKick`

基类：`nonebot.adapters.mirai.event.notice.BotJoinGroupEvent`

Bot被踢出一个群


## _class_ `MemberJoinEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

新人入群的事件


## _class_ `MemberLeaveEventKick`

基类：`nonebot.adapters.mirai.event.notice.MemberJoinEvent`

成员被踢出群（该成员不是Bot）


## _class_ `MemberLeaveEventQuit`

基类：`nonebot.adapters.mirai.event.notice.MemberJoinEvent`

成员主动离群（该成员不是Bot）


## _class_ `FriendRecallEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

好友消息撤回


## _class_ `GroupRecallEvent`

基类：`nonebot.adapters.mirai.event.notice.FriendRecallEvent`

群消息撤回


## _class_ `GroupStateChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

群变化事件基类


## _class_ `GroupNameChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

某个群名改变


## _class_ `GroupEntranceAnnouncementChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

某群入群公告改变


## _class_ `GroupMuteAllEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

全员禁言


## _class_ `GroupAllowAnonymousChatEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

匿名聊天


## _class_ `GroupAllowConfessTalkEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

坦白说


## _class_ `GroupAllowMemberInviteEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

允许群员邀请好友加群


## _class_ `MemberStateChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

群成员变化事件基类


## _class_ `MemberCardChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

群名片改动


## _class_ `MemberSpecialTitleChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

群头衔改动（只有群主有操作限权）


## _class_ `BotGroupPermissionChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

Bot在群里的权限被改变


## _class_ `MemberPermissionChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

成员权限改变的事件（该成员不是Bot）


## _class_ `RequestEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

请求事件基类


## _class_ `NewFriendRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

添加好友申请


### _async_ `approve(bot)`


* **说明**

    通过此人的好友申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, operate=1, message='')`


* **说明**

    拒绝此人的好友申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `operate: Literal[1, 2]`: 响应的操作类型


        * `1`: 拒绝添加好友


        * `2`: 拒绝添加好友并添加黑名单，不再接收该用户的好友申请


    * `message: str`: 回复的信息



## _class_ `MemberJoinRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

用户入群申请（Bot需要有管理员权限）


### _async_ `approve(bot)`


* **说明**

    通过此人的加群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, operate=1, message='')`


* **说明**

    拒绝(忽略)此人的加群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `operate: Literal[1, 2, 3, 4]`: 响应的操作类型


        * `1`: 拒绝入群


        * `2`: 忽略请求


        * `3`: 拒绝入群并添加黑名单，不再接收该用户的入群申请


        * `4`: 忽略入群并添加黑名单，不再接收该用户的入群申请


    * `message: str`: 回复的信息



## _class_ `BotInvitedJoinGroupRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

Bot被邀请入群申请


### _async_ `approve(bot)`


* **说明**

    通过这份被邀请入群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, message='')`


* **说明**

    拒绝这份被邀请入群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `message: str`: 邀请消息


# NoneBot.adapters.mirai.event.base 模块


## _class_ `UserPermission`

基类：`str`, `enum.Enum`


* **说明**


用户权限枚举类

> 
> * `OWNER`: 群主


> * `ADMINISTRATOR`: 群管理


> * `MEMBER`: 普通群成员


## _class_ `Event`

基类：[`nonebot.adapters._base.Event`](README.md#nonebot.adapters._base.Event)

mirai-api-http 协议事件，字段与 mirai-api-http 一致。各事件字段参考 [mirai-api-http 事件类型](https://github.com/project-mirai/mirai-api-http/blob/master/docs/EventType.md)


### _classmethod_ `new(data)`

此事件类的工厂函数, 能够通过事件数据选择合适的子类进行序列化


### `normalize_dict(**kwargs)`

返回可以被json正常反序列化的结构体

# NoneBot.adapters.mirai.event.meta 模块


## _class_ `MetaEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

元事件基类


## _class_ `BotOnlineEvent`

基类：`nonebot.adapters.mirai.event.meta.MetaEvent`

Bot登录成功


## _class_ `BotOfflineEventActive`

基类：`nonebot.adapters.mirai.event.meta.MetaEvent`

Bot主动离线


## _class_ `BotOfflineEventForce`

基类：`nonebot.adapters.mirai.event.meta.MetaEvent`

Bot被挤下线


## _class_ `BotOfflineEventDropped`

基类：`nonebot.adapters.mirai.event.meta.MetaEvent`

Bot被服务器断开或因网络问题而掉线


## _class_ `BotReloginEvent`

基类：`nonebot.adapters.mirai.event.meta.MetaEvent`

Bot主动重新登录

# NoneBot.adapters.mirai.event.message 模块


## _class_ `MessageEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

消息事件基类


## _class_ `GroupMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

群消息事件


## _class_ `FriendMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

好友消息事件


## _class_ `TempMessage`

基类：`nonebot.adapters.mirai.event.message.MessageEvent`

临时会话消息事件

# NoneBot.adapters.mirai.event.notice 模块


## _class_ `NoticeEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

通知事件基类


## _class_ `MuteEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

禁言类事件基类


## _class_ `BotMuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

Bot被禁言


## _class_ `BotUnmuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

Bot被取消禁言


## _class_ `MemberMuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

群成员被禁言事件（该成员不是Bot）


## _class_ `MemberUnmuteEvent`

基类：`nonebot.adapters.mirai.event.notice.MuteEvent`

群成员被取消禁言事件（该成员不是Bot）


## _class_ `BotJoinGroupEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

Bot加入了一个新群


## _class_ `BotLeaveEventActive`

基类：`nonebot.adapters.mirai.event.notice.BotJoinGroupEvent`

Bot主动退出一个群


## _class_ `BotLeaveEventKick`

基类：`nonebot.adapters.mirai.event.notice.BotJoinGroupEvent`

Bot被踢出一个群


## _class_ `MemberJoinEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

新人入群的事件


## _class_ `MemberLeaveEventKick`

基类：`nonebot.adapters.mirai.event.notice.MemberJoinEvent`

成员被踢出群（该成员不是Bot）


## _class_ `MemberLeaveEventQuit`

基类：`nonebot.adapters.mirai.event.notice.MemberJoinEvent`

成员主动离群（该成员不是Bot）


## _class_ `FriendRecallEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

好友消息撤回


## _class_ `GroupRecallEvent`

基类：`nonebot.adapters.mirai.event.notice.FriendRecallEvent`

群消息撤回


## _class_ `GroupStateChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

群变化事件基类


## _class_ `GroupNameChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

某个群名改变


## _class_ `GroupEntranceAnnouncementChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

某群入群公告改变


## _class_ `GroupMuteAllEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

全员禁言


## _class_ `GroupAllowAnonymousChatEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

匿名聊天


## _class_ `GroupAllowConfessTalkEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

坦白说


## _class_ `GroupAllowMemberInviteEvent`

基类：`nonebot.adapters.mirai.event.notice.GroupStateChangeEvent`

允许群员邀请好友加群


## _class_ `MemberStateChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.NoticeEvent`

群成员变化事件基类


## _class_ `MemberCardChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

群名片改动


## _class_ `MemberSpecialTitleChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

群头衔改动（只有群主有操作限权）


## _class_ `BotGroupPermissionChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

Bot在群里的权限被改变


## _class_ `MemberPermissionChangeEvent`

基类：`nonebot.adapters.mirai.event.notice.MemberStateChangeEvent`

成员权限改变的事件（该成员不是Bot）

# NoneBot.adapters.mirai.event.request 模块


## _class_ `RequestEvent`

基类：`nonebot.adapters.mirai.event.base.Event`

请求事件基类


## _class_ `NewFriendRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

添加好友申请


### _async_ `approve(bot)`


* **说明**

    通过此人的好友申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, operate=1, message='')`


* **说明**

    拒绝此人的好友申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `operate: Literal[1, 2]`: 响应的操作类型


        * `1`: 拒绝添加好友


        * `2`: 拒绝添加好友并添加黑名单，不再接收该用户的好友申请


    * `message: str`: 回复的信息



## _class_ `MemberJoinRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

用户入群申请（Bot需要有管理员权限）


### _async_ `approve(bot)`


* **说明**

    通过此人的加群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, operate=1, message='')`


* **说明**

    拒绝(忽略)此人的加群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `operate: Literal[1, 2, 3, 4]`: 响应的操作类型


        * `1`: 拒绝入群


        * `2`: 忽略请求


        * `3`: 拒绝入群并添加黑名单，不再接收该用户的入群申请


        * `4`: 忽略入群并添加黑名单，不再接收该用户的入群申请


    * `message: str`: 回复的信息



## _class_ `BotInvitedJoinGroupRequestEvent`

基类：`nonebot.adapters.mirai.event.request.RequestEvent`

Bot被邀请入群申请


### _async_ `approve(bot)`


* **说明**

    通过这份被邀请入群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象



### _async_ `reject(bot, message='')`


* **说明**

    拒绝这份被邀请入群申请



* **参数**

    
    * `bot: Bot`: 当前的 `Bot` 对象


    * `message: str`: 邀请消息
