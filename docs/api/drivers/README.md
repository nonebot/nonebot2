---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers 模块

## 后端驱动适配基类

各驱动请继承以下基类


## _class_ `Driver`

基类：`abc.ABC`

Driver 基类。将后端框架封装，以满足适配器使用。


### `_adapters`


* **类型**

    `Dict[str, Type[Bot]]`



* **说明**

    已注册的适配器列表



### `_ws_connection_hook`


* **类型**

    `Set[T_WebSocketConnectionHook]`



* **说明**

    WebSocket 连接建立时执行的函数



### `_ws_disconnection_hook`


* **类型**

    `Set[T_WebSocketDisconnectionHook]`



* **说明**

    WebSocket 连接断开时执行的函数



### _abstract_ `__init__(env, config)`


* **参数**

    
    * `env: Env`: 包含环境信息的 Env 对象


    * `config: Config`: 包含配置信息的 Config 对象



### `env`


* **类型**

    `str`



* **说明**

    环境名称



### `config`


* **类型**

    `Config`



* **说明**

    配置对象



### `_clients`


* **类型**

    `Dict[str, Bot]`



* **说明**

    已连接的 Bot



### _classmethod_ `register_adapter(name, adapter)`


* **说明**

    注册一个协议适配器



* **参数**

    
    * `name: str`: 适配器名称，用于在连接时进行识别


    * `adapter: Type[Bot]`: 适配器 Class



### _abstract property_ `type`

驱动类型名称


### _abstract property_ `server_app`

驱动 APP 对象


### _abstract property_ `asgi`

驱动 ASGI 对象


### _abstract property_ `logger`

驱动专属 logger 日志记录器


### _property_ `bots`


* **类型**

    `Dict[str, Bot]`



* **说明**

    获取当前所有已连接的 Bot



### _abstract_ `on_startup(func)`

注册一个在驱动启动时运行的函数


### _abstract_ `on_shutdown(func)`

注册一个在驱动停止时运行的函数


### `on_bot_connect(func)`


* **说明**

    装饰一个函数使他在 bot 通过 WebSocket 连接成功时执行。



* **函数参数**

    
    * `bot: Bot`: 当前连接上的 Bot 对象



### `on_bot_disconnect(func)`


* **说明**

    装饰一个函数使他在 bot 通过 WebSocket 连接断开时执行。



* **函数参数**

    
    * `bot: Bot`: 当前连接上的 Bot 对象



### `bot_connect(bot)`

在 WebSocket 连接成功后，调用该函数来注册 bot 对象


### `bot_disconnect(bot)`

在 WebSocket 连接断开后，调用该函数来注销 bot 对象


### _abstract_ `run(host=None, port=None, *args, **kwargs)`


* **说明**

    启动驱动框架



* **参数**

    
    * `host: Optional[str]`: 驱动绑定 IP


    * `post: Optional[int]`: 驱动绑定端口


    * `*args`


    * `**kwargs`



### _abstract async_ `_handle_http()`

用于处理 HTTP 类型请求的函数


### _abstract async_ `_handle_ws_reverse()`

用于处理 WebSocket 类型请求的函数


## _class_ `WebSocket`

基类：`object`

WebSocket 连接封装，统一接口方便外部调用。


### _abstract_ `__init__(websocket)`


* **参数**

    
    * `websocket: Any`: WebSocket 连接对象



### _property_ `websocket`

WebSocket 连接对象


### _abstract property_ `closed`


* **类型**

    `bool`



* **说明**

    连接是否已经关闭



### _abstract async_ `accept()`

接受 WebSocket 连接请求


### _abstract async_ `close(code)`

关闭 WebSocket 连接请求


### _abstract async_ `receive()`

接收一条 WebSocket 信息


### _abstract async_ `send(data)`

发送一条 WebSocket 信息
