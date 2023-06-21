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

  - untyped

## _class_ `Mixin(<auto>)` {#Mixin}

- **说明:** Websockets Mixin

- **参数**

  auto

### _async method_ `request(setup)` {#Mixin-request}

- **参数**

  - `setup` ([Request](index.md#Request))

- **返回**

  - [Response](index.md#Response)

### _method_ `websocket(setup)` {#Mixin-websocket}

- **参数**

  - `setup` ([Request](index.md#Request))

- **返回**

  - AsyncGenerator[[WebSocket](index.md#WebSocket), None]

## _class_ `WebSocket(*, request, websocket)` {#WebSocket}

- **说明:** Websockets WebSocket Wrapper

- **参数**

  - `request` ([Request](index.md#Request))

  - `websocket` (WebSocketClientProtocol)

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

### _async method_ `receive_text()` {#WebSocket-receive_text}

- **参数**

  empty

- **返回**

  - str

### _async method_ `receive_bytes()` {#WebSocket-receive_bytes}

- **参数**

  empty

- **返回**

  - bytes

### _async method_ `send_text(data)` {#WebSocket-send_text}

- **参数**

  - `data` (str)

- **返回**

  - None

### _async method_ `send_bytes(data)` {#WebSocket-send_bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - None

## _var_ `Driver` {#Driver}

- **类型:** type[[ForwardDriver](index.md#ForwardDriver)]

- **说明:** Websockets Driver
