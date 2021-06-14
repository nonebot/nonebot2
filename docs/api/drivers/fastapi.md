---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.drivers.fastapi 模块

## FastAPI 驱动适配

后端使用方法请参考: [FastAPI 文档](https://fastapi.tiangolo.com/)


## _class_ `Config`

基类：`pydantic.env_settings.BaseSettings`

FastAPI 驱动框架设置，详情参考 FastAPI 文档


### `fastapi_openapi_url`


* **类型**

    `Optional[str]`



* **说明**

    `openapi.json` 地址，默认为 `None` 即关闭



### `fastapi_docs_url`


* **类型**

    `Optional[str]`



* **说明**

    `swagger` 地址，默认为 `None` 即关闭



### `fastapi_redoc_url`


* **类型**

    `Optional[str]`



* **说明**

    `redoc` 地址，默认为 `None` 即关闭



### `fastapi_reload_dirs`


* **类型**

    `List[str]`



* **说明**

    `debug` 模式下重载监控文件夹列表，默认为 uvicorn 默认值



## _class_ `Driver`

基类：[`nonebot.drivers.ReverseDriver`](README.md#nonebot.drivers.ReverseDriver)

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


## _class_ `WebSocket`

基类：[`nonebot.drivers.WebSocket`](README.md#nonebot.drivers.WebSocket)
