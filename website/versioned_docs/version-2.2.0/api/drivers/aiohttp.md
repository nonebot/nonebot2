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

## _class_ `Mixin(<auto>)` {#Mixin}

- **说明:** AIOHTTP Mixin

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

## _class_ `WebSocket(*, request, session, websocket)` {#WebSocket}

- **说明:** AIOHTTP Websocket Wrapper

- **参数**

  - `request` ([Request](index.md#Request))

  - `session` (aiohttp.ClientSession)

  - `websocket` (aiohttp.ClientWebSocketResponse)

### _async method_ `accept()` {#WebSocket-accept}

- **参数**

  empty

- **返回**

  - untyped

### _async method_ `close(code=1000)` {#WebSocket-close}

- **参数**

  - `code` (int)

- **返回**

  - untyped

### _async method_ `receive()` {#WebSocket-receive}

- **参数**

  empty

- **返回**

  - str

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

  - None

### _async method_ `send_bytes(data)` {#WebSocket-send-bytes}

- **参数**

  - `data` (bytes)

- **返回**

  - None

## _class_ `Driver(env, config)` {#Driver}

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))
