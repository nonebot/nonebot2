# NoneBot.drivers.fastapi 模块

## FastAPI 驱动适配

本驱动同时支持服务端以及客户端连接

后端使用方法请参考: [FastAPI 文档](https://fastapi.tiangolo.com/)

## _class_ `Config`

基类：`pydantic.env_settings.BaseSettings`

FastAPI 驱动框架设置，详情参考 FastAPI 文档

### `fastapi_openapi_url`

- **类型**

  `Optional[str]`

- **说明**

  `openapi.json` 地址，默认为 `None` 即关闭

### `fastapi_docs_url`

- **类型**

  `Optional[str]`

- **说明**

  `swagger` 地址，默认为 `None` 即关闭

### `fastapi_redoc_url`

- **类型**

  `Optional[str]`

- **说明**

  `redoc` 地址，默认为 `None` 即关闭

### `fastapi_reload`

- **类型**

  `bool`

- **说明**

  开启/关闭冷重载

### `fastapi_reload_dirs`

- **类型**

  `Optional[List[str]]`

- **说明**

  重载监控文件夹列表，默认为 uvicorn 默认值

### `fastapi_reload_delay`

- **类型**

  `Optional[float]`

- **说明**

  重载延迟，默认为 uvicorn 默认值

### `fastapi_reload_includes`

- **类型**

  `Optional[List[str]]`

- **说明**

  要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### `fastapi_reload_excludes`

- **类型**

  `Optional[List[str]]`

- **说明**

  不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

## _class_ `Driver`

基类：[`nonebot.drivers.ReverseDriver`](README.md#nonebot.drivers.ReverseDriver)

FastAPI 驱动框架。包含反向 Server 功能。

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
