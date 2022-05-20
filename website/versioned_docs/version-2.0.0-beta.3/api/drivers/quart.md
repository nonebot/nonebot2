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

## _class_ `Config(_env_file='<object object>', _env_file_encoding=None, _env_nested_delimiter=None, _secrets_dir=None, *, quart_reload=False, quart_reload_dirs=None, quart_reload_delay=None, quart_reload_includes=None, quart_reload_excludes=None)` {#Config}

- **说明**

  Quart 驱动框架设置

- **参数**

  - `_env_file` (str | os.PathLike | NoneType)

  - `_env_file_encoding` (str | None)

  - `_env_nested_delimiter` (str | None)

  - `_secrets_dir` (str | os.PathLike | NoneType)

  - `quart_reload` (bool)

  - `quart_reload_dirs` (list[str])

  - `quart_reload_delay` (float)

  - `quart_reload_includes` (list[str])

  - `quart_reload_excludes` (list[str])

### _class-var_ `quart_reload` {#Config-quart_reload}

- **类型:** bool

- **说明:** 开启/关闭冷重载

### _class-var_ `quart_reload_dirs` {#Config-quart_reload_dirs}

- **类型:** list[str] | None

- **说明:** 重载监控文件夹列表，默认为 uvicorn 默认值

### _class-var_ `quart_reload_delay` {#Config-quart_reload_delay}

- **类型:** float | None

- **说明:** 重载延迟，默认为 uvicorn 默认值

### _class-var_ `quart_reload_includes` {#Config-quart_reload_includes}

- **类型:** list[str] | None

- **说明:** 要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

### _class-var_ `quart_reload_excludes` {#Config-quart_reload_excludes}

- **类型:** list[str] | None

- **说明:** 不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

## _class_ `Driver(env, config)` {#Driver}

- **说明**

  Quart 驱动框架

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

### _property_ `asgi` {#Driver-asgi}

- **类型:**

- **说明:** `Quart` 对象

### _property_ `logger` {#Driver-logger}

- **类型:**

- **说明:** Quart 使用的 logger

### _property_ `server_app` {#Driver-server_app}

- **类型:** quart.app.Quart

- **说明:** `Quart` 对象

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `quart`

### _method_ `on_shutdown(self, func)` {#Driver-on_shutdown}

- **说明**

  参考文档: [`Startup and Shutdown`](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)

- **参数**

  - `func` ((~ \_AsyncCallable))

- **返回**

  - (~ \_AsyncCallable)

### _method_ `on_startup(self, func)` {#Driver-on_startup}

- **说明**

  参考文档: [`Startup and Shutdown`](https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html)

- **参数**

  - `func` ((~ \_AsyncCallable))

- **返回**

  - (~ \_AsyncCallable)

### _method_ `run(self, host=None, port=None, *, app=None, **kwargs)` {#Driver-run}

- **说明**

  使用 `uvicorn` 启动 Quart

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

## _class_ `WebSocket(*, request, websocket)` {#WebSocket}

- **说明**

  Quart WebSocket Wrapper

- **参数**

  - `request` (nonebot.internal.driver.model.Request)

  - `websocket` (quart.wrappers.websocket.Websocket)

### _async method_ `accept(self)` {#WebSocket-accept}

- **返回**

  - Unknown

### _async method_ `close(self, code=1000, reason='')` {#WebSocket-close}

- **参数**

  - `code` (int)

  - `reason` (str)

- **返回**

  - Unknown

### _async method_ `receive(self)` {#WebSocket-receive}

- **返回**

  - str | bytes

### _async method_ `receive_bytes(self)` {#WebSocket-receive_bytes}

- **返回**

  - bytes

### _async method_ `receive_text(self)` {#WebSocket-receive_text}

- **返回**

  - str

### _async method_ `send_bytes(self, data)` {#WebSocket-send_bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - Unknown

### _async method_ `send_text(self, data)` {#WebSocket-send_text}

- **参数**

  - `data` (str)

- **返回**

  - Unknown
