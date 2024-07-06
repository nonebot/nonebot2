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

## _class_ `Session(params=None, headers=None, cookies=None, version=HTTPVersion.H11, timeout=None, proxy=None)` {#Session}

- **参数**

  - `params` (QueryTypes)

  - `headers` (HeaderTypes)

  - `cookies` (CookieTypes)

  - `version` (str | [HTTPVersion](index.md#HTTPVersion))

  - `timeout` (float | None)

  - `proxy` (str | None)

### _async method_ `request(setup)` {#Session-request}

- **参数**

  - `setup` ([Request](index.md#Request))

- **返回**

  - [Response](index.md#Response)

### _async method_ `setup()` {#Session-setup}

- **参数**

  empty

- **返回**

  - None

### _async method_ `close()` {#Session-close}

- **参数**

  empty

- **返回**

  - None

## _class_ `Mixin(<auto>)` {#Mixin}

- **说明:** HTTPX Mixin

- **参数**

  auto

### _async method_ `request(setup)` {#Mixin-request}

- **参数**

  - `setup` ([Request](index.md#Request))

- **返回**

  - [Response](index.md#Response)

### _method_ `get_session(params=None, headers=None, cookies=None, version=HTTPVersion.H11, timeout=None, proxy=None)` {#Mixin-get-session}

- **参数**

  - `params` (QueryTypes)

  - `headers` (HeaderTypes)

  - `cookies` (CookieTypes)

  - `version` (str | [HTTPVersion](index.md#HTTPVersion))

  - `timeout` (float | None)

  - `proxy` (str | None)

- **返回**

  - Session

## _class_ `Driver(env, config)` {#Driver}

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))
