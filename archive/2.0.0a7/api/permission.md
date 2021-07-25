---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.permission 模块

## 权限

每个 `Matcher` 拥有一个 `Permission` ，其中是 **异步** `PermissionChecker` 的集合，只要有一个 `PermissionChecker` 检查结果为 `True` 时就会继续运行。

:::tip 提示
`PermissionChecker` 既可以是 async function 也可以是 sync function
:::


## `MESSAGE`


* **说明**: 匹配任意 `message` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 message type 的 Matcher。


## `NOTICE`


* **说明**: 匹配任意 `notice` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 notice type 的 Matcher。


## `REQUEST`


* **说明**: 匹配任意 `request` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 request type 的 Matcher。


## `METAEVENT`


* **说明**: 匹配任意 `meta_event` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 meta_event type 的 Matcher。


## `USER(*user, perm=<nonebot.permission.Permission object>)`


* **说明**

    在白名单内且满足 perm



* **参数**

    
    * `*user: int`: 白名单


    * `perm: Permission`: 需要同时满足的权限



## `PRIVATE`


* **说明**: 匹配任意私聊消息类型事件


## `PRIVATE_FRIEND`


* **说明**: 匹配任意好友私聊消息类型事件


## `PRIVATE_GROUP`


* **说明**: 匹配任意群临时私聊消息类型事件


## `PRIVATE_OTHER`


* **说明**: 匹配任意其他私聊消息类型事件


## `GROUP`


* **说明**: 匹配任意群聊消息类型事件


## `GROUP_MEMBER`


* **说明**: 匹配任意群员群聊消息类型事件

:::warning 警告
该权限通过 event.sender 进行判断且不包含管理员以及群主！
:::


## `GROUP_ADMIN`


* **说明**: 匹配任意群管理员群聊消息类型事件


## `GROUP_OWNER`


* **说明**: 匹配任意群主群聊消息类型事件


## `SUPERUSER`


* **说明**: 匹配任意超级用户消息类型事件


## `EVERYBODY`


* **说明**: 匹配任意消息类型事件
