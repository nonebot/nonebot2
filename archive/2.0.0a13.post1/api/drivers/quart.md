---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers.quart 模块

## Quart 驱动适配

后端使用方法请参考: [Quart 文档](https://pgjones.gitlab.io/quart/index.html)


## _class_ `Driver`

基类：[`nonebot.drivers.Driver`](README.md#nonebot.drivers.Driver)

Quart 驱动框架


* **上报地址**

    
    * `/{adapter name}/http`: HTTP POST 上报


    * `/{adapter name}/ws`: WebSocket 上报



### _property_ `type`

驱动名称: `quart`


### _property_ `server_app`

`Quart` 对象


### _property_ `asgi`

`Quart` 对象


### _property_ `logger`

fastapi 使用的 logger


### `on_startup(func)`

参考文档: [Startup and Shutdown](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)


### `on_shutdown(func)`

参考文档: [Startup and Shutdown](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)


### `run(host=None, port=None, *, app=None, **kwargs)`

使用 `uvicorn` 启动 Quart
