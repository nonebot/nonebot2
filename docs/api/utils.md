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

    
    * Callable[..., Awaitable[Any]]



## _class_ `DataclassEncoder`

基类：`json.encoder.JSONEncoder`


* **类型**

    `json.JSONEncoder`



* **说明**

    `JSONEncoder` used when encoding `Message` (List of dataclasses)



### `default(o)`

Implement this method in a subclass such that it returns
a serializable object for `o`, or calls the base implementation
(to raise a `TypeError`).

For example, to support arbitrary iterators, you could
implement default like this:

```default
def default(self, o):
    try:
        iterable = iter(o)
    except TypeError:
        pass
    else:
        return list(iterable)
    # Let the base class default method raise the TypeError
    return JSONEncoder.default(self, o)
```
