---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers.fastapi 模块

## FastAPI 驱动适配

后端使用方法请参考: [FastAPI 文档](https://fastapi.tiangolo.com/)


## _class_ `Driver`

基类：[`nonebot.drivers.Driver`](README.md#nonebot.drivers.Driver)

FastAPI 驱动框架


* **上报地址**

    
    * `/{adapter name}/`: HTTP POST 上报


    * `/{adapter name}/http/`: HTTP POST 上报


    * `/{adapter name}/ws`: WebSocket 上报


    * `/{adapter name}/ws/`: WebSocket 上报



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
