---
sidebar_position: 2
description: nonebot.drivers.aiohttp 模块
---

# nonebot.drivers.aiohttp

[AIOHTTP](https://aiohttp.readthedocs.io/en/stable/) 驱动适配器。

```bash
nb driver install aiohttp
# 或者
pip install nonebot2[aiohttp]
```

:::tip 提示
本驱动仅支持客户端连接
:::

## _class_ `Mixin()` {#Mixin}

- **说明**

  AIOHTTP Mixin

### _property_ `type` {#Mixin-type}

- **类型:** str

### _async method_ `request(self, setup)` {#Mixin-request}

- **参数**

  - `setup` (nonebot.internal.driver.model.Request)

- **返回**

  - nonebot.internal.driver.model.Response

### _method_ `websocket(self, setup)` {#Mixin-websocket}

- **参数**

  - `setup` (nonebot.internal.driver.model.Request)

- **返回**

  - AsyncGenerator[WebSocket, NoneType]

## _class_ `WebSocket(*, request, session, websocket)` {#WebSocket}

- **说明**

  AIOHTTP Websocket Wrapper

- **参数**

  - `request` (nonebot.internal.driver.model.Request)

  - `session` (aiohttp.client.ClientSession)

  - `websocket` (aiohttp.client_ws.ClientWebSocketResponse)

### _async method_ `accept(self)` {#WebSocket-accept}

- **返回**

  - Unknown

### _async method_ `close(self, code=1000)` {#WebSocket-close}

- **参数**

  - `code` (int)

- **返回**

  - Unknown

### _async method_ `receive(self)` {#WebSocket-receive}

- **返回**

  - str

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

  - None

### _async method_ `send_text(self, data)` {#WebSocket-send_text}

- **参数**

  - `data` (str)

- **返回**

  - None

## _library-attr_ `Driver`

三方库 API
