---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers 模块

## 后端驱动适配基类

各驱动请继承以下基类


## _class_ `BaseDriver`

基类：`abc.ABC`

Driver 基类。将后端框架封装，以满足适配器使用。


### `_adapters`


* **类型**

    `Dict[str, Type[Bot]]`



* **说明**

    已注册的适配器列表



### _abstract_ `__init__(env, config)`

Initialize self.  See help(type(self)) for accurate signature.
