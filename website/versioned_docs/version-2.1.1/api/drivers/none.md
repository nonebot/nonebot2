---
sidebar_position: 6
description: nonebot.drivers.none 模块
---

# nonebot.drivers.none

None 驱动适配

:::tip 提示
本驱动不支持任何服务器或客户端连接
:::

## _class_ `Driver(env, config)` {#Driver}

- **说明:** None 驱动框架

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `none`

### _property_ `logger` {#Driver-logger}

- **类型:** untyped

- **说明:** none driver 使用的 logger

### _method_ `on_startup(func)` {#Driver-on-startup}

- **说明:** 注册一个启动时执行的函数

- **参数**

  - `func` (LIFESPAN_FUNC)

- **返回**

  - LIFESPAN_FUNC

### _method_ `on_shutdown(func)` {#Driver-on-shutdown}

- **说明:** 注册一个停止时执行的函数

- **参数**

  - `func` (LIFESPAN_FUNC)

- **返回**

  - LIFESPAN_FUNC

### _method_ `run(*args, **kwargs)` {#Driver-run}

- **说明:** 启动 none driver

- **参数**

  - `*args`

  - `**kwargs`

- **返回**

  - untyped

### _method_ `exit(force=False)` {#Driver-exit}

- **说明:** 退出 none driver

- **参数**

  - `force` (bool): 强制退出

- **返回**

  - untyped
