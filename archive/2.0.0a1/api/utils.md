---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.utils 模块


## `run_sync(func)`


* **说明**

    一个用于包装 sync function 为 async function 的装饰器



* **参数**

    
    * `func: Callable[..., Any]`: 被装饰的同步函数



* **返回**

    
    * `Callable[..., Awaitable[Any]]`



## _class_ `DataclassEncoder`

基类：`json.encoder.JSONEncoder`


* **说明**

    在JSON序列化 `Message` (List[Dataclass]) 时使用的 `JSONEncoder`
