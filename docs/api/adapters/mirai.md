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

    
    * `verify_key` / `mirai_verify_key`: mirai-api-http 的 verify_key


    * `mirai_host`: mirai-api-http 的地址


    * `mirai_port`: mirai-api-http 的端口


# NoneBot.adapters.mirai.bot 模块


## _class_ `Bot`

基类：[`nonebot.adapters._base.Bot`](README.md#nonebot.adapters._base.Bot)

mirai-api-http 协议 Bot 适配。

::: warning
API中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

部分字段可能与文档在符号上不一致
:::


### _async_ `send(event, message, at_sender=False)`


* **说明**

    根据 `event` 向触发事件的主体发送信息



* **参数**

    
    * `event: Event`: Event对象


    * `message: Union[MessageChain, MessageSegment, str]`: 要发送的消息


    * `at_sender: bool`: 是否 @ 事件主体


# NoneBot.adapters.mirai.message 模块


## _class_ `MessageType`

基类：`str`, `enum.Enum`

消息类型枚举类


## _class_ `MessageSegment`

基类：[`nonebot.adapters._base.MessageSegment`](README.md#nonebot.adapters._base.MessageSegment)[`MessageChain`]

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


### `export()`

导出为可以被正常json序列化的数组


### `extract_first(*type)`


* **说明**

    弹出该消息链的第一个消息



* **参数**

    
    * \*type: MessageType: 指定的消息类型, 当指定后如类型不匹配不弹出


# NoneBot.adapters.mirai.utils 模块

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
