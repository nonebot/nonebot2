# NoneBot.drivers.quart 模块

## Quart 驱动适配

后端使用方法请参考: [Quart 文档](https://pgjones.gitlab.io/quart/index.html)


## _class_ `Config`

基类：`pydantic.env_settings.BaseSettings`

Quart 驱动框架设置


### `quart_reload`


* **类型**

    `Optional[bool]`



* **说明**

    开启/关闭冷重载，默认会在配置了 app 的 debug 模式启用



### `quart_reload_dirs`


* **类型**

    `Optional[List[str]]`



* **说明**

    重载监控文件夹列表，默认为 uvicorn 默认值



### `quart_reload_delay`


* **类型**

    `Optional[float]`



* **说明**

    重载延迟，默认为 uvicorn 默认值



### `quart_reload_includes`


* **类型**

    `Optional[List[str]]`



* **说明**

    要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值



### `quart_reload_excludes`


* **类型**

    `Optional[List[str]]`



* **说明**

    不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值



## _class_ `Driver`

基类：[`nonebot.drivers.ReverseDriver`](README.md#nonebot.drivers.ReverseDriver)

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

Quart 使用的 logger


### `on_startup(func)`

参考文档: [Startup and Shutdown](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)


### `on_shutdown(func)`

参考文档: [Startup and Shutdown](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)


### `run(host=None, port=None, *, app=None, **kwargs)`

使用 `uvicorn` 启动 Quart


## _class_ `WebSocket`

基类：[`nonebot.drivers.WebSocket`](README.md#nonebot.drivers.WebSocket)
