---
sidebar_position: 1
description: nonebot.drivers.fastapi 模块
---

# nonebot.drivers.fastapi

[FastAPI](https://fastapi.tiangolo.com/) 驱动适配

```bash
nb driver install fastapi
# 或者
pip install nonebot2[fastapi]
```

:::tip 提示
本驱动仅支持服务端连接
:::

## _class_ `Config(<auto>)` {#Config}

- **说明:** FastAPI 驱动框架设置，详情参考 FastAPI 文档

- **参数**

  auto

### _class-var_ `fastapi_openapi_url` {#Config-fastapi-openapi-url}

- **类型:** str | None

- **说明:** `openapi.json` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_docs_url` {#Config-fastapi-docs-url}

- **类型:** str | None

- **说明:** `swagger` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_redoc_url` {#Config-fastapi-redoc-url}

- **类型:** str | None

- **说明:** `redoc` 地址，默认为 `None` 即关闭

### _class-var_ `fastapi_include_adapter_schema` {#Config-fastapi-include-adapter-schema}

- **类型:** bool

- **说明:** 是否包含适配器路由的 schema，默认为 `True`

### _class-var_ `fastapi_reload` {#Config-fastapi-reload}

- **类型:** bool

- **说明:** 开启/关闭冷重载

### _class-var_ `fastapi_reload_dirs` {#Config-fastapi-reload-dirs}

- **类型:** list[str] | None

- **说明:** 重载监控文件夹列表，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_delay` {#Config-fastapi-reload-delay}

- **类型:** float

- **说明:** 重载延迟，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_includes` {#Config-fastapi-reload-includes}

- **类型:** list[str] | None

- **说明:** 要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `fastapi_reload_excludes` {#Config-fastapi-reload-excludes}

- **类型:** list[str] | None

- **说明:** 不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `fastapi_extra` {#Config-fastapi-extra}

- **类型:** dict[str, Any]

- **说明:** 传递给 `FastAPI` 的其他参数。

## _class_ `Driver(env, config)` {#Driver}

- **说明:** FastAPI 驱动框架。

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` (NoneBotConfig)

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `fastapi`

### _property_ `server_app` {#Driver-server-app}

- **类型:** FastAPI

- **说明:** `FastAPI APP` 对象

### _property_ `asgi` {#Driver-asgi}

- **类型:** FastAPI

- **说明:** `FastAPI APP` 对象

### _property_ `logger` {#Driver-logger}

- **类型:** logging.Logger

- **说明:** fastapi 使用的 logger

### _method_ `setup_http_server(setup)` {#Driver-setup-http-server}

- **参数**

  - `setup` ([HTTPServerSetup](index.md#HTTPServerSetup))

- **返回**

  - untyped

### _method_ `setup_websocket_server(setup)` {#Driver-setup-websocket-server}

- **参数**

  - `setup` ([WebSocketServerSetup](index.md#WebSocketServerSetup))

- **返回**

  - None

### _method_ `on_startup(func)` {#Driver-on-startup}

- **参数**

  - `func` (LIFESPAN_FUNC)

- **返回**

  - LIFESPAN_FUNC

### _method_ `on_shutdown(func)` {#Driver-on-shutdown}

- **参数**

  - `func` (LIFESPAN_FUNC)

- **返回**

  - LIFESPAN_FUNC

### _method_ `run(host=None, port=None, *, app=None, **kwargs)` {#Driver-run}

- **说明:** 使用 `uvicorn` 启动 FastAPI

- **参数**

  - `host` (str | None)

  - `port` (int | None)

  - `app` (str | None)

  - `**kwargs`

- **返回**

  - untyped

## _class_ `FastAPIWebSocket(*, request, websocket)` {#FastAPIWebSocket}

- **说明:** FastAPI WebSocket Wrapper

- **参数**

  - `request` (BaseRequest)

  - `websocket` ([WebSocket](index.md#WebSocket))

### _async method_ `accept()` {#FastAPIWebSocket-accept}

- **参数**

  empty

- **返回**

  - None

### _async method_ `close(code=status.WS_1000_NORMAL_CLOSURE, reason="")` {#FastAPIWebSocket-close}

- **参数**

  - `code` (int)

  - `reason` (str)

- **返回**

  - None

### _async method_ `receive()` {#FastAPIWebSocket-receive}

- **参数**

  empty

- **返回**

  - str | bytes

### _async method_ `receive_text()` {#FastAPIWebSocket-receive-text}

- **参数**

  empty

- **返回**

  - str

### _async method_ `receive_bytes()` {#FastAPIWebSocket-receive-bytes}

- **参数**

  empty

- **返回**

  - bytes

### _async method_ `send_text(data)` {#FastAPIWebSocket-send-text}

- **参数**

  - `data` (str)

- **返回**

  - None

### _async method_ `send_bytes(data)` {#FastAPIWebSocket-send-bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - None
