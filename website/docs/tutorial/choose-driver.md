---
sidebar_position: 5
description: 各驱动器的功能与区别

options:
  menu:
    weight: 22
    category: guide
---

# 选择驱动器

:::warning 注意
驱动器的选择通常与你所使用的协议适配器相关，如果你不知道该选择哪个驱动器，可以先阅读你想要使用的协议适配器文档说明。
:::

:::tip 提示
如何**安装**驱动器请参考 [安装驱动器](../start/install-driver.md)

如何**使用**驱动器请参考 [配置](./configuration.md#driver)
:::

## 驱动器的类型

驱动器的类型有两种：

- `ForwardDriver`: 即客户端类型驱动器，多用于使用 HTTP 轮询，WebSocket 连接服务器的情形。
- `ReverseDriver`: 即服务端类型驱动器，多用于使用 WebHook 情形。

其中 `ReverseDriver` 可以配合 `ForwardDriver` 一起使用，即可以同时使用客户端功能和服务端功能。

## 驱动器的功能

在 NoneBot 中，驱动器主要负责数据的收发，不对数据进行处理。通常，驱动器会实现以下功能：

### ForwardDriver

1. 异步发送 HTTP 请求，自定义 `HTTP Method`, `URL`, `Header`, `Body`, `Cookie`, `Proxy`, `Timeout` 等。
2. 异步建立 WebSocket 连接上下文，自定义 `WebSocket URL`, `Header`, `Cookie`, `Proxy`, `Timeout` 等。

### ReverseDriver

1. 协议适配器自定义 HTTP 上报地址以及对上报数据处理的回调函数。
2. 协议适配器自定义 WebSocket 连接请求地址以及对 WebSocket 请求处理的回调函数。
3. 用户可以将 Driver 作为服务端使用，自行添加任何服务端相关功能。

## 内置驱动器

### FastAPI （默认）

类型: `ReverseDriver`

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

FastAPI 是一个易上手、高性能的异步 Web 框架，具有极佳的编写体验，可以挂载其他 ASGI, WSGI 应用。

FastAPI: [文档](https://fastapi.tiangolo.com/), [仓库](https://github.com/tiangolo/fastapi)

驱动器: [API](../api/drivers/fastapi.md), [源码](https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/fastapi.py)

```env
DRIVER=~fastapi
```

<!-- TODO: 配置项 -->

### Quart

类型: `ReverseDriver`

> Quart is an asyncio reimplementation of the popular Flask microframework API.

Quart 是一个类 Flask 的异步版本，拥有与 Flask 非常相似的接口和使用方法。

Quart: [文档](https://pgjones.gitlab.io/quart/), [仓库](https://gitlab.com/pgjones/quart)

驱动器: [API](../api/drivers/quart.md), [源码](https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/quart.py)

```env
DRIVER=~quart
```

### HTTPX

类型: `ForwardDriver`

:::warning 注意
本驱动器仅支持 HTTP 请求，不支持 WebSocket 请求。
:::

> HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

HTTPX: [文档](https://www.python-httpx.org/), [仓库](https://github.com/encode/httpx/)

驱动器: [API](../api/drivers/httpx.md), [源码](https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/httpx.py)

```env
DRIVER=~httpx
```

:::important 注意
本驱动器支持 `Mixin`
:::

### websockets

类型: `ForwardDriver`

:::warning 注意
本驱动器仅支持 WebSocket 请求，不支持 HTTP 请求。
:::

> websockets is a library for building WebSocket servers and clients in Python with a focus on correctness, simplicity, robustness, and performance.

websockets: [文档](https://websockets.readthedocs.io/en/stable/), [仓库](https://github.com/aaugustin/websockets)

驱动器: [API](../api/drivers/websockets.md), [源码](https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/websockets.py)

```env
DRIVER=~websockets
```

:::important 注意
本驱动器支持 `Mixin`
:::

### AIOHTTP

类型: `ForwardDriver`

> Asynchronous HTTP Client/Server for asyncio and Python.

AIOHTTP: [文档](https://docs.aiohttp.org/en/stable/), [仓库](https://github.com/aio-libs/aiohttp)

驱动器: [API](../api/drivers/aiohttp.md), [源码](https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/aiohttp.py)

```env
DRIVER=~httpx
```

:::important 注意
本驱动器支持 `Mixin`
:::
