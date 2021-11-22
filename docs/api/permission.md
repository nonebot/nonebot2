---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.permission 模块

## 权限

每个 `Matcher` 拥有一个 `Permission` ，其中是 `PermissionChecker` 的集合，只要有一个 `PermissionChecker` 检查结果为 `True` 时就会继续运行。

:::tip 提示
`PermissionChecker` 既可以是 async function 也可以是 sync function
:::


## _class_ `Permission`

基类：`object`


* **说明**

    `Matcher` 规则类，当事件传递时，在 `Matcher` 运行前进行检查。



* **示例**


```python
Permission(async_function) | sync_function
# 等价于
from nonebot.utils import run_sync
Permission(async_function, run_sync(sync_function))
```


### `__init__(*checkers)`


* **参数**

    
    * `*checkers: Union[T_PermissionChecker, Handler]`: PermissionChecker



### `checkers`


* **说明**

    存储 `PermissionChecker`



* **类型**

    
    * `Set[Handler]`



### _async_ `__call__(bot, event, stack=None, dependency_cache=None)`


* **说明**

    检查是否满足某个权限



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象


    * `stack: Optional[AsyncExitStack]`: 异步上下文栈


    * `dependency_cache: Optional[Dict[Callable[..., Any], Any]]`: 依赖缓存



* **返回**

    
    * `bool`



## `MESSAGE`


* **说明**: 匹配任意 `message` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 message type 的 Matcher。


## `NOTICE`


* **说明**: 匹配任意 `notice` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 notice type 的 Matcher。


## `REQUEST`


* **说明**: 匹配任意 `request` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 request type 的 Matcher。


## `METAEVENT`


* **说明**: 匹配任意 `meta_event` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 meta_event type 的 Matcher。


## `USER(*user, perm=None)`


* **说明**

    `event` 的 `session_id` 在白名单内且满足 perm



* **参数**

    
    * `*user: str`: 白名单


    * `perm: Optional[Permission]`: 需要同时满足的权限



## `SUPERUSER`


* **说明**: 匹配任意超级用户消息类型事件
