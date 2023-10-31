---
sidebar_position: 5
description: nonebot.drivers.quart 模块
---

# nonebot.drivers.quart

[Quart](https://pgjones.gitlab.io/quart/index.html) 驱动适配

```bash
nb driver install quart
# 或者
pip install nonebot2[quart]
```

:::tip 提示
本驱动仅支持服务端连接
:::

## _class_ `Config(<auto>)` {#Config}

- **说明:** Quart 驱动框架设置

- **参数**

  auto

### _class-var_ `quart_reload` {#Config-quart-reload}

- **类型:** bool

- **说明:** 开启/关闭冷重载

### _class-var_ `quart_reload_dirs` {#Config-quart-reload-dirs}

- **类型:** list[str] | None

- **说明:** 重载监控文件夹列表，默认为 uvicorn 默认值

### _class-var_ `quart_reload_delay` {#Config-quart-reload-delay}

- **类型:** float

- **说明:** 重载延迟，默认为 uvicorn 默认值

### _class-var_ `quart_reload_includes` {#Config-quart-reload-includes}

- **类型:** list[str] | None

- **说明:** 要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `quart_reload_excludes` {#Config-quart-reload-excludes}

- **类型:** list[str] | None

- **说明:** 不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `quart_extra` {#Config-quart-extra}

- **类型:** dict[str, Any]

- **说明:** 传递给 `Quart` 的其他参数。

## _class_ `Driver(env, config)` {#Driver}

- **说明:** Quart 驱动框架

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` (NoneBotConfig)

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `quart`

### _property_ `server_app` {#Driver-server-app}

- **类型:** Quart

- **说明:** `Quart` 对象

### _property_ `asgi` {#Driver-asgi}

- **类型:** untyped

- **说明:** `Quart` 对象

### _property_ `logger` {#Driver-logger}

- **类型:** untyped

- **说明:** Quart 使用的 logger

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

- **说明:** 参考文档: [`Startup and Shutdown`](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)

- **参数**

  - `func` (\_AsyncCallable)

- **返回**

  - \_AsyncCallable

### _method_ `on_shutdown(func)` {#Driver-on-shutdown}

- **说明:** 参考文档: [`Startup and Shutdown`](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)

- **参数**

  - `func` (\_AsyncCallable)

- **返回**

  - \_AsyncCallable

### _method_ `run(host=None, port=None, *, app=None, **kwargs)` {#Driver-run}

- **说明:** 使用 `uvicorn` 启动 Quart

- **参数**

  - `host` (str | None)

  - `port` (int | None)

  - `app` (str | None)

  - `**kwargs`

- **返回**

  - untyped

## _class_ `WebSocket(*, request, websocket_ctx)` {#WebSocket}

- **说明:** Quart WebSocket Wrapper

- **参数**

  - `request` (BaseRequest)

  - `websocket_ctx` (WebsocketContext)

### _async method_ `accept()` {#WebSocket-accept}

- **参数**

  empty

- **返回**

  - untyped

### _async method_ `close(code=1000, reason="")` {#WebSocket-close}

- **参数**

  - `code` (int)

  - `reason` (str)

- **返回**

  - untyped

### _async method_ `receive()` {#WebSocket-receive}

- **参数**

  empty

- **返回**

  - str | bytes

### _async method_ `receive_text()` {#WebSocket-receive-text}

- **参数**

  empty

- **返回**

  - str

### _async method_ `receive_bytes()` {#WebSocket-receive-bytes}

- **参数**

  empty

- **返回**

  - bytes

### _async method_ `send_text(data)` {#WebSocket-send-text}

- **参数**

  - `data` (str)

- **返回**

  - untyped

### _async method_ `send_bytes(data)` {#WebSocket-send-bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - untyped
