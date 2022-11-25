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

## _class_ `Mixin()` {#Mixin}

- **说明**

  HTTPX Mixin

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

  - AsyncGenerator[nonebot.internal.driver.model.WebSocket, NoneType]

## _library-attr_ `Driver`

三方库 API
