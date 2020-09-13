---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.rule 模块

## 规则

每个 `Matcher` 拥有一个 `Rule` ，其中是 `RuleChecker` 的集合，只有当所有 `RuleChecker` 检查结果为 `True` 时继续运行。

:::tip 提示
`RuleChecker` 既可以是 async function 也可以是 sync function
:::


## _class_ `Rule`

基类：`object`


* **说明**

    `Matcher` 规则类，当事件传递时，在 `Matcher` 运行前进行检查。



* **示例**


```python
Rule(async_function) & sync_function
# 等价于
from nonebot.utils import run_sync
Rule(async_function, run_sync(sync_function))
```


### `__init__(*checkers)`


* **参数**

    
    * `*checkers: Callable[[Bot, Event, dict], Awaitable[bool]]`: **异步** RuleChecker



### `checkers`


* **说明**

    存储 `RuleChecker`



* **类型**

    
    * `Set[Callable[[Bot, Event, dict], Awaitable[bool]]]`



### _async_ `__call__(bot, event, state)`


* **说明**

    检查是否符合所有规则



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象


    * `state: dict`: 当前 State



* **返回**

    
    * `bool`
