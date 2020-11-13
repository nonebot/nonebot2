---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers.fastapi 模块

## FastAPI 驱动适配

后端使用方法请参考: [FastAPI 文档](https://fastapi.tiangolo.com/)


## _class_ `Driver`

基类：[`nonebot.drivers.BaseDriver`](README.md#nonebot.drivers.BaseDriver)

FastAPI 驱动框架


### _property_ `type`

驱动名称: `fastapi`


### _property_ `server_app`

`FastAPI APP` 对象


### _property_ `asgi`

`FastAPI APP` 对象


### _property_ `logger`

fastapi 使用的 logger


### `on_startup(func)`

参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#startup-event)


### `on_shutdown(func)`

参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#startup-event)


### `run(host=None, port=None, *, app=None, **kwargs)`

使用 `uvicorn` 启动 FastAPI


### _async_ `_handle_http(adapter, request, data=Body(Ellipsis))`

用于处理 HTTP 类型请求的函数


### _async_ `_handle_ws_reverse(adapter, websocket)`

用于处理 WebSocket 类型请求的函数


## _class_ `WebSocket`

基类：[`nonebot.drivers.BaseWebSocket`](README.md#nonebot.drivers.BaseWebSocket)


### _property_ `closed`


* **类型**

    `bool`



* **说明**

    连接是否已经关闭



### _async_ `accept()`

接受 WebSocket 连接请求


### _async_ `close(code=1000)`

关闭 WebSocket 连接请求


### _async_ `receive()`

接收一条 WebSocket 信息


### _async_ `send(data)`

发送一条 WebSocket 信息
