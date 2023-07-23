---
sidebar_position: 3
description: nonebot.drivers.httpx 模块
---

# nonebot.drivers.httpx

[HTTPX](https://www.python-httpx.org/) 驱动适配

```bash
nb driver install httpx
# 或者
pip install nonebot2[httpx]
```

:::tip 提示
本驱动仅支持客户端 HTTP 连接
:::

## _class_ `Mixin(<auto>)` {#Mixin}

- **说明:** HTTPX Mixin

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

## _var_ `Driver` {#Driver}

- **类型:** type[[ForwardDriver](index.md#ForwardDriver)]

- **说明:** HTTPX Driver
