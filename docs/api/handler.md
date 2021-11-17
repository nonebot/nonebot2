---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.handler 模块

## 事件处理函数

该模块实现事件处理函数的封装，以实现动态参数等功能。


## _class_ `Handler`

基类：`object`

事件处理器类。支持依赖注入。


### `__init__(func, *, name=None, dependencies=None, allow_types=None, dependency_overrides_provider=None)`


* **说明**

    装饰一个函数为事件处理器。



* **参数**

    
    * `func: T_Handler`: 事件处理函数。


    * `name: Optional[str]`: 事件处理器名称。默认为函数名。


    * `dependencies: Optional[List[DependsWrapper]]`: 额外的非参数依赖注入。


    * `allow_types: Optional[List[Type[Param]]]`: 允许的参数类型。


    * `dependency_overrides_provider: Optional[Any]`: 依赖注入覆盖提供者。



### `func`


* **类型**

    `T_Handler`



* **说明**

    事件处理函数



### `name`


* **类型**

    `str`



* **说明**

    事件处理函数名



### `allow_types`


* **类型**

    `List[Type[Param]]`



* **说明**

    事件处理器允许的参数类型



### `dependencies`


* **类型**

    `List[DependsWrapper]`



* **说明**

    事件处理器的额外依赖
