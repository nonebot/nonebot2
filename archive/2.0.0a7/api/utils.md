---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.utils 模块


## `escape_tag(s)`


* **说明**

    用于记录带颜色日志时转义 `<tag>` 类型特殊标签



* **参数**

    
    * `s: str`: 需要转义的字符串



* **返回**

    
    * `str`



## `run_sync(func)`


* **说明**

    一个用于包装 sync function 为 async function 的装饰器



* **参数**

    
    * `func: Callable[..., Any]`: 被装饰的同步函数



* **返回**

    
    * `Callable[..., Awaitable[Any]]`



## _class_ `DataclassEncoder`


* **说明**

    在JSON序列化 `Message` (List[Dataclass]) 时使用的 `JSONEncoder`
