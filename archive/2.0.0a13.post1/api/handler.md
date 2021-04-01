---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.handler 模块

## 事件处理函数

该模块实现事件处理函数的封装，以实现动态参数等功能。


## _class_ `Handler`

基类：`object`

事件处理函数类


### `__init__(func)`

装饰事件处理函数以便根据动态参数运行


### `func`


* **类型**

    `T_Handler`



* **说明**

    事件处理函数



### `signature`


* **类型**

    `inspect.Signature`



* **说明**

    事件处理函数签名



### _property_ `bot_type`


* **类型**

    `Union[Type["Bot"], inspect.Parameter.empty]`



* **说明**

    事件处理函数接受的 Bot 对象类型



### _property_ `event_type`


* **类型**

    `Optional[Union[Type[Event], inspect.Parameter.empty]]`



* **说明**

    事件处理函数接受的 event 类型 / 不需要 event 参数



### _property_ `state_type`


* **类型**

    `Optional[Union[T_State, inspect.Parameter.empty]]`



* **说明**

    事件处理函数是否接受 state 参数



### _property_ `matcher_type`


* **类型**

    `Optional[Union[Type["Matcher"], inspect.Parameter.empty]]`



* **说明**

    事件处理函数是否接受 matcher 参数
