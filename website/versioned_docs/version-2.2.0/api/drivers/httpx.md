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

## _class_ `Driver(env, config)` {#Driver}

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))
