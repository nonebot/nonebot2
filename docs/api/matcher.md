---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.matcher 模块

## 事件响应器

该模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行 对话 。


## `matchers`


* **类型**

    `Dict[int, List[Type[Matcher]]]`



* **说明**

    用于存储当前所有的事件响应器



## _class_ `Matcher`

基类：`object`

事件响应器类


### `module`


* **类型**

    `Optional[str]`



* **说明**

    事件响应器所在模块名称



### `type`


* **类型**

    `str`



* **说明**

    事件响应器类型



### `rule`


* **类型**

    `Rule`



* **说明**

    事件响应器匹配规则



### `permission`


* **类型**

    `Permission`



* **说明**

    事件响应器触发权限



### `priority`


* **类型**

    `int`



* **说明**

    事件响应器优先级



### `block`


* **类型**

    `bool`



* **说明**

    事件响应器是否阻止事件传播



### `temp`


* **类型**

    `bool`



* **说明**

    事件响应器是否为临时



### `expire_time`


* **类型**

    `Optional[datetime]`



* **说明**

    事件响应器过期时间点



### `_default_state`


* **类型**

    `dict`



* **说明**

    事件响应器默认状态



### `_default_parser`


* **类型**

    `Optional[ArgsParser]`



* **说明**

    事件响应器默认参数解析函数



### `handlers`


* **类型**

    `List[Handler]`



* **说明**

    事件响应器拥有的事件处理函数列表



### _classmethod_ `new(type_='', rule=None, permission=None, handlers=None, temp=False, priority=1, block=False, *, module=None, default_state=None, expire_time=None)`


* **说明**

    创建一个新的事件响应器，并存储至 [matchers](#matchers)



* **参数**

    
    * `type_: str`: 事件响应器类型，与 `event.type` 一致时触发，空字符串表示任意


    * `rule: Optional[Rule]`: 匹配规则


    * `permission: Optional[Permission]`: 权限


    * `handlers: Optional[List[Handler]]`: 事件处理函数列表


    * `temp: bool`: 是否为临时事件响应器，即触发一次后删除


    * `priority: int`: 响应优先级


    * `block: bool`: 是否阻止事件向更低优先级的响应器传播


    * `module: Optional[str]`: 事件响应器所在模块名称


    * `default_state: Optional[dict]`: 默认状态 `state`


    * `expire_time: Optional[datetime]`: 事件响应器最终有效时间点，过时即被删除



* **返回**

    
    * `Type[Matcher]`: 新的事件响应器类



### _async classmethod_ `check_perm(bot, event)`


* **说明**

    检查是否满足触发权限



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: 上报事件



* **返回**

    
    * `bool`: 是否满足权限



### _async classmethod_ `check_rule(bot, event, state)`


* **说明**

    检查是否满足匹配规则



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: 上报事件


    * `state: dict`: 当前状态



* **返回**

    
    * `bool`: 是否满足匹配规则



### _classmethod_ `args_parser(func)`


* **说明**

    用于装饰一个函数来更改当前事件响应器的默认参数解析函数



* **参数**

    
    * `func: ArgsParser`: 参数解析函数



### _classmethod_ `handle()`

直接处理消息事件


### _classmethod_ `receive()`

接收一条新消息并处理
