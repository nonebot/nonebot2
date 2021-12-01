# NoneBot.message 模块

## 事件处理

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。


## `event_preprocessor(func)`


* **说明**

    事件预处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。



## `event_postprocessor(func)`


* **说明**

    事件后处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。



## `run_preprocessor(func)`


* **说明**

    运行预处理。装饰一个函数，使它在每次事件响应器运行前执行。



## `run_postprocessor(func)`


* **说明**

    运行后处理。装饰一个函数，使它在每次事件响应器运行后执行。



## _async_ `handle_event(bot, event)`


* **说明**

    处理一个事件。调用该函数以实现分发事件。



* **参数**

    
    * `bot: Bot`: Bot 对象


    * `event: Event`: Event 对象



* **示例**


```python
import asyncio
asyncio.create_task(handle_event(bot, event))
```
