---
sidebar_position: 1
description: nonebot.drivers.fastapi 模块
---

# nonebot.drivers.fastapi

[FastAPI](https://fastapi.tiangolo.com/) 驱动适配

:::tip 提示
本驱动仅支持服务端连接
:::

## _class_ `Config(_env_file='<object object>', _env_file_encoding=None, _env_nested_delimiter=None, _secrets_dir=None, *, fastapi_openapi_url=None, fastapi_docs_url=None, fastapi_redoc_url=None, fastapi_include_adapter_schema=True, fastapi_reload=False, fastapi_reload_dirs=None, fastapi_reload_delay=0.25, fastapi_reload_includes=None, fastapi_reload_excludes=None)` {#Config}

- **说明**

  FastAPI 驱动框架设置，详情参考 FastAPI 文档

- **参数**

  - `_env_file` (str | os.PathLike | list[str | os.PathLike] | tuple[str | os.PathLike, ...] | NoneType)

  - `_env_file_encoding` (str | None)

  - `_env_nested_delimiter` (str | None)

  - `_secrets_dir` (str | os.PathLike | NoneType)

  - `fastapi_openapi_url` (str | None)

  - `fastapi_docs_url` (str | None)

  - `fastapi_redoc_url` (str | None)

  - `fastapi_include_adapter_schema` (bool)

  - `fastapi_reload` (bool)

  - `fastapi_reload_dirs` (list[str] | None)

  - `fastapi_reload_delay` (float)

  - `fastapi_reload_includes` (list[str] | None)

  - `fastapi_reload_excludes` (list[str] | None)

### _class-var_ `fastapi_openapi_url` {#Config-fastapi_openapi_url}

- **类型:** str | None

- **说明:** `openapi.json` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_docs_url` {#Config-fastapi_docs_url}

- **类型:** str | None

- **说明:** `swagger` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_redoc_url` {#Config-fastapi_redoc_url}

- **类型:** str | None

- **说明:** `redoc` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_include_adapter_schema` {#Config-fastapi_include_adapter_schema}

- **类型:** bool

- **说明:** 是否包含适配器路由的 schema，默认为 `True`

### _class-var_ `fastapi_reload` {#Config-fastapi_reload}

- **类型:** bool

- **说明:** 开启/关闭冷重载

### _class-var_ `fastapi_reload_dirs` {#Config-fastapi_reload_dirs}

- **类型:** list[str] | None

- **说明:** 重载监控文件夹列表，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_delay` {#Config-fastapi_reload_delay}

- **类型:** float

- **说明:** 重载延迟，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_includes` {#Config-fastapi_reload_includes}

- **类型:** list[str] | None

- **说明:** 要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_excludes` {#Config-fastapi_reload_excludes}

- **类型:** list[str] | None

- **说明:** 不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

## _class_ `Driver(env, config)` {#Driver}

- **说明**

  FastAPI 驱动框架。

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

### _property_ `asgi` {#Driver-asgi}

- **类型:** fastapi.applications.FastAPI

- **说明:** `FastAPI APP` 对象

### _property_ `logger` {#Driver-logger}

- **类型:** logging.Logger

- **说明:** fastapi 使用的 logger

### _property_ `server_app` {#Driver-server_app}

- **类型:** fastapi.applications.FastAPI

- **说明:** `FastAPI APP` 对象

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `fastapi`

### _method_ `on_shutdown(self, func)` {#Driver-on_shutdown}

- **说明**

  参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#shutdown-event>`\_

- **参数**

  - `func` (Callable)

- **返回**

  - Callable

### _method_ `on_startup(self, func)` {#Driver-on_startup}

- **说明**

  参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#startup-event>`\_

- **参数**

  - `func` (Callable)

- **返回**

  - Callable

### _method_ `run(self, host=None, port=None, *, app=None, **kwargs)` {#Driver-run}

- **说明**

  使用 `uvicorn` 启动 FastAPI

- **参数**

  - `host` (str | None)

  - `port` (int | None)

  - `app` (str | None)

  - `**kwargs`

- **返回**

  - Unknown

### _method_ `setup_http_server(self, setup)` {#Driver-setup_http_server}

- **参数**

  - `setup` (nonebot.internal.driver.model.HTTPServerSetup)

- **返回**

  - Unknown

### _method_ `setup_websocket_server(self, setup)` {#Driver-setup_websocket_server}

- **参数**

  - `setup` (nonebot.internal.driver.model.WebSocketServerSetup)

- **返回**

  - None

## _class_ `FastAPIWebSocket(*, request, websocket)` {#FastAPIWebSocket}

- **说明**

  FastAPI WebSocket Wrapper

- **参数**

  - `request` (nonebot.internal.driver.model.Request)

  - `websocket` (starlette.websockets.WebSocket)

### _property_ `closed` {#FastAPIWebSocket-closed}

- **类型:** bool

### _async method_ `accept(self)` {#FastAPIWebSocket-accept}

- **返回**

  - None

### _async method_ `close(self, code=1000, reason='')` {#FastAPIWebSocket-close}

- **参数**

  - `code` (int)

  - `reason` (str)

- **返回**

  - None

### _async method_ `receive(self)` {#FastAPIWebSocket-receive}

- **返回**

  - str | bytes

### _async method_ `receive_bytes(self)` {#FastAPIWebSocket-receive_bytes}

- **返回**

  - bytes

### _async method_ `receive_text(self)` {#FastAPIWebSocket-receive_text}

- **返回**

  - str

### _async method_ `send_bytes(self, data)` {#FastAPIWebSocket-send_bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - None

### _async method_ `send_text(self, data)` {#FastAPIWebSocket-send_text}

- **参数**

  - `data` (str)

- **返回**

  - None
