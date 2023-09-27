---
sidebar_position: 9
description: 添加服务端路由规则

options:
  menu:
    - category: advanced
      weight: 100
---

# 添加路由

在[驱动器](./driver.md)一节中，我们了解了驱动器的两种类型。既然驱动器可以作为服务端运行，那么我们就可以向驱动器添加路由规则，从而实现自定义的 API 接口等功能。在添加路由规则时，我们需要注意驱动器的类型，详情可以参考[选择驱动器](./driver.md#配置驱动器)。

NoneBot 中，我们可以通过两种途径向 ASGI 驱动器添加路由规则：

1. 通过 NoneBot 的兼容层建立路由规则。
2. 直接向 ASGI 应用添加路由规则。

这两种途径各有优劣，前者可以在各种服务端型驱动器下运行，但并不能直接使用 ASGI 应用框架提供的特性与功能；后者直接使用 ASGI 应用，更自由、功能完整，但只能在特定类型驱动器下运行。

在向驱动器添加路由规则时，我们需要注意驱动器是否为服务端类型，我们可以通过以下方式判断：

```python
from nonebot import get_driver
from nonebot.drivers import ASGIMixin

# highlight-next-line
can_use = isinstance(get_driver(), ASGIMixin)
```

## 通过兼容层添加路由

NoneBot 兼容层定义了两个数据类 `HTTPServerSetup` 和 `WebSocketServerSetup`，分别用于定义 HTTP 服务端和 WebSocket 服务端的路由规则。

### HTTP 路由

`HTTPServerSetup` 具有四个属性：

- `path`：路由路径，不支持特殊占位表达式。类型为 `URL`。
- `method`：请求方法。类型为 `str`。
- `name`：路由名称，不可重复。类型为 `str`。
- `handle_func`：路由处理函数。类型为 `Callable[[Request], Awaitable[Response]]`。

例如，我们添加一个 `/hello` 的路由，当请求方法为 `GET` 时，返回 `200 OK` 以及返回体信息：

```python
from nonebot import get_driver
from nonebot.drivers import URL, Request, Response, ASGIMixin, HTTPServerSetup

async def hello(request: Request) -> Response:
    return Response(200, content="Hello, world!")

if isinstance((driver := get_driver()), ASGIMixin):
    driver.setup_http_server(
        HTTPServerSetup(
            path=URL("/hello"),
            method="GET",
            name="hello",
            handle_func=hello,
        )
    )
```

对于 `Request` 和 `Response` 的详细信息，可以参考 [API 文档](../api/drivers/index.md)。

### WebSocket 路由

`WebSocketServerSetup` 具有三个属性：

- `path`：路由路径，不支持特殊占位表达式。类型为 `URL`。
- `name`：路由名称，不可重复。类型为 `str`。
- `handle_func`：路由处理函数。类型为 `Callable[[WebSocket], Awaitable[Any]]`。

例如，我们添加一个 `/ws` 的路由，发送所有接收到的数据：

```python
from nonebot import get_driver
from nonebot.drivers import URL, ASGIMixin, WebSocket, WebSocketServerSetup

async def ws_handler(ws: WebSocket):
    await ws.accept()
    try:
      while True:
          data = await ws.receive()
          await ws.send(data)
    except WebSocketClosed as e:
        # handle closed
        ...
    finally:
        with contextlib.suppress(Exception):
            await websocket.close()
        # do some cleanup

if isinstance((driver := get_driver()), ASGIMixin):
    driver.setup_websocket_server(
        WebSocketServerSetup(
            path=URL("/ws"),
            name="ws",
            handle_func=ws_handler,
        )
    )
```

对于 `WebSocket` 的详细信息，可以参考 [API 文档](../api/drivers/index.md)。

## 使用 ASGI 应用添加路由

### 获取 ASGI 应用

NoneBot 服务端类型的驱动器具有两个属性 `server_app` 和 `asgi`，分别对应驱动框架应用和 ASGI 应用。通常情况下，这两个应用是同一个对象。我们可以通过 `get_app()` 方法快速获取：

```python
import nonebot

app = nonebot.get_app()
asgi = nonebot.get_asgi()
```

### 添加路由规则

在获取到了 ASGI 应用后，我们就可以直接使用 ASGI 应用框架提供的功能来添加路由规则了。这里我们以 [FastAPI](./driver.md#fastapi默认) 为例，演示如何添加路由规则。

在下面的代码中，我们添加了一个 `GET` 类型的 `/api` 路由，具体方法参考 [FastAPI 文档](https://fastapi.tiangolo.com/)。

```python
import nonebot
from fastapi import FastAPI

app: FastAPI = nonebot.get_app()

@app.get("/api")
async def custom_api():
    return {"message": "Hello, world!"}
```
