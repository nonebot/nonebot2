---
sidebar_position: 4
description: nonebot.drivers.websockets 模块
---

# nonebot.drivers.websockets

[websockets](https://websockets.readthedocs.io/) 驱动适配

```bash
nb driver install websockets
# 或者
pip install nonebot2[websockets]
```

:::tip 提示
本驱动仅支持客户端 WebSocket 连接
:::

## _def_ `catch_closed(func)` {#catch_closed}

- **参数**

  - `func`

- **返回**

  - Unknown

## _class_ `Mixin()` {#Mixin}

- **说明**

  Websockets Mixin

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

## _class_ `WebSocket(*, request, websocket)` {#WebSocket}

- **说明**

  Websockets WebSocket Wrapper

- **参数**

  - `request` (nonebot.internal.driver.model.Request)

  - `websocket` (websockets.legacy.client.WebSocketClientProtocol)

### _property_ `closed` {#WebSocket-closed}

- **类型:** bool

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

  - None

### _async method_ `send_text(self, data)` {#WebSocket-send_text}

- **参数**

  - `data` (str)

- **返回**

  - None

## _library-attr_ `Driver`

三方库 API
