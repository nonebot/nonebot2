# NoneBot.drivers.aiohttp 模块

## AIOHTTP 驱动适配

本驱动仅支持客户端连接


## _class_ `Driver`

基类：[`nonebot.drivers.ForwardDriver`](README.md#nonebot.drivers.ForwardDriver)

AIOHTTP 驱动框架


### _property_ `type`

驱动名称: `aiohttp`


### _property_ `logger`

aiohttp driver 使用的 logger


### `on_startup(func)`


* **说明**

    注册一个启动时执行的函数



* **参数**

    
    * `func: Callable[[], Awaitable[None]]`



### `on_shutdown(func)`


* **说明**

    注册一个停止时执行的函数



* **参数**

    
    * `func: Callable[[], Awaitable[None]]`



### `setup_http_polling(setup)`


* **说明**

    注册一个 HTTP 轮询连接，如果传入一个函数，则该函数会在每次连接时被调用



* **参数**

    
    * `setup: Union[HTTPPollingSetup, Callable[[], Awaitable[HTTPPollingSetup]]]`



### `setup_websocket(setup)`


* **说明**

    注册一个 WebSocket 连接，如果传入一个函数，则该函数会在每次重连时被调用



* **参数**

    
    * `setup: Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]`



### `run(*args, **kwargs)`

启动 aiohttp driver


## _class_ `WebSocket`

基类：[`nonebot.drivers.WebSocket`](README.md#nonebot.drivers.WebSocket)
