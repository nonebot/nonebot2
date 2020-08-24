---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot 模块


## `get_driver()`


* **说明**

    获取全局 Driver 对象。可用于在计划任务的回调中获取当前 Driver 对象。



* **返回**

    
    * `Driver`: 全局 Driver 对象



* **异常**

    
    * `ValueError`: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)



* **用法**


```python
driver = nonebot.get_driver()
```


## `get_app()`


* **说明**

    获取全局 Driver 对应 Server App 对象。



* **返回**

    
    * `Any`: Server App 对象



* **异常**

    
    * `ValueError`: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)



* **用法**


```python
app = nonebot.get_app()
```


## `get_asgi()`


* **说明**

    获取全局 Driver 对应 Asgi 对象。



* **返回**

    
    * `Any`: Asgi 对象



* **异常**

    
    * `ValueError`: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)



* **用法**


```python
asgi = nonebot.get_asgi()
```


## `get_bots()`


* **说明**

    获取所有通过 ws 连接 NoneBot 的 Bot 对象。



* **返回**

    
    * `Dict[str, Bot]`: 一个以字符串 ID 为键，Bot 对象为值的字典



* **异常**

    
    * `ValueError`: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)



* **用法**


```python
bots = nonebot.get_bots()
```


## `init(*, _env_file=None, **kwargs)`


* **说明**

    初始化 NoneBot 以及 全局 Driver 对象。

    NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。

    你也可以传入自定义的 _env_file 来指定 NoneBot 从该文件读取配置。



* **参数**

    
    * `_env_file: Optional[str]`: 配置文件名，默认从 .env.{env_name} 中读取配置


    * `**kwargs`: 任意变量，将会存储到 Config 对象里



* **返回**

    
    * None



* **用法**


```python
nonebot.init(database=Database(...))
```


## `run(host=None, port=None, *args, **kwargs)`


* **说明**

    启动 NoneBot，即运行全局 Driver 对象。



* **参数**

    
    * `host: Optional[str]`: 主机名／IP，若不传入则使用配置文件中指定的值


    * `port: Optional[int]`: 端口，若不传入则使用配置文件中指定的值


    * `*args`: 传入 Driver.run 的位置参数


    * `**kwargs`: 传入 Driver.run 的命名参数



* **返回**

    
    * None



* **用法**


```python
nonebot.run(host="127.0.0.1", port=8080)
```
