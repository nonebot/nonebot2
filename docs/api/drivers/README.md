---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers 模块

## 后端驱动适配基类

各驱动请继承以下基类


## _class_ `Driver`

基类：`abc.ABC`

Driver 基类。


### `_adapters`


* **类型**

    `Dict[str, Type[Bot]]`



* **说明**

    已注册的适配器列表



### `_bot_connection_hook`


* **类型**

    `Set[T_BotConnectionHook]`



* **说明**

    Bot 连接建立时执行的函数



### `_bot_disconnection_hook`


* **类型**

    `Set[T_BotDisconnectionHook]`



* **说明**

    Bot 连接断开时执行的函数



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



### _property_ `bots`


* **类型**

    `Dict[str, Bot]`



* **说明**

    获取当前所有已连接的 Bot



### `register_adapter(name, adapter, **kwargs)`


* **说明**

    注册一个协议适配器



* **参数**

    
    * `name: str`: 适配器名称，用于在连接时进行识别


    * `adapter: Type[Bot]`: 适配器 Class



### _abstract property_ `type`

驱动类型名称


### _abstract property_ `logger`

驱动专属 logger 日志记录器


### _abstract_ `run(host=None, port=None, *args, **kwargs)`


* **说明**

    启动驱动框架



* **参数**

    
    * `host: Optional[str]`: 驱动绑定 IP


    * `post: Optional[int]`: 驱动绑定端口


    * `*args`


    * `**kwargs`



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



### `_bot_connect(bot)`

在 WebSocket 连接成功后，调用该函数来注册 bot 对象


### `_bot_disconnect(bot)`

在 WebSocket 连接断开后，调用该函数来注销 bot 对象


## _class_ `ReverseDriver`

基类：`nonebot.drivers.Driver`

Reverse Driver 基类。将后端框架封装，以满足适配器使用。


### _abstract property_ `server_app`

驱动 APP 对象


### _abstract property_ `asgi`

驱动 ASGI 对象


## _class_ `HTTPConnection`

基类：`abc.ABC`


### `http_version`

One of "1.0", "1.1" or "2".


### `scheme`

URL scheme portion (likely "http" or "https").


### `path`

HTTP request target excluding any query string,
with percent-encoded sequences and UTF-8 byte sequences
decoded into characters.


### `query_string`

URL portion after the ?, percent-encoded.


### `headers`

A dict of name-value pairs,
where name is the header name, and value is the header value.

Order of header values must be preserved from the original HTTP request;
order of header names is not important.

Header names must be lowercased.


### _abstract property_ `type`

Connection type.


## _class_ `HTTPRequest`

基类：`nonebot.drivers.HTTPConnection`

HTTP 请求封装。参考 [asgi http scope](https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope)。


### `method`

The HTTP method name, uppercased.


### `body`

Body of the request.

Optional; if missing defaults to b"".


### _property_ `type`

Always `http`


## _class_ `HTTPResponse`

基类：`object`

HTTP 响应封装。参考 [asgi http scope](https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope)。


### `status`

HTTP status code.


### `body`

HTTP body content.

Optional; if missing defaults to `None`.


### `headers`

A dict of name-value pairs,
where name is the header name, and value is the header value.

Order must be preserved in the HTTP response.

Header names must be lowercased.

Optional; if missing defaults to an empty dict.


### _property_ `type`

Always `http`


## _class_ `WebSocket`

基类：`nonebot.drivers.HTTPConnection`, `abc.ABC`

WebSocket 连接封装。参考 [asgi websocket scope](https://asgi.readthedocs.io/en/latest/specs/www.html#websocket-connection-scope)。


### _property_ `type`

Always `websocket`


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

接收一条 WebSocket text 信息


### _abstract async_ `receive_bytes()`

接收一条 WebSocket binary 信息


### _abstract async_ `send(data)`

发送一条 WebSocket text 信息


### _abstract async_ `send_bytes(data)`

发送一条 WebSocket binary 信息
