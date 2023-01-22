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

- **说明**

  None 驱动框架

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

### _property_ `logger` {#Driver-logger}

- **类型:**

- **说明:** none driver 使用的 logger

### _property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动名称: `none`

### _method_ `on_shutdown(self, func)` {#Driver-on_shutdown}

- **说明**

  注册一个停止时执行的函数

- **参数**

  - `func` (() -> NoneType | () -> Awaitable[NoneType])

- **返回**

  - () -> NoneType | () -> Awaitable[NoneType]

### _method_ `on_startup(self, func)` {#Driver-on_startup}

- **说明**

  注册一个启动时执行的函数

- **参数**

  - `func` (() -> NoneType | () -> Awaitable[NoneType])

- **返回**

  - () -> NoneType | () -> Awaitable[NoneType]

### _method_ `run(self, *args, **kwargs)` {#Driver-run}

- **说明**

  启动 none driver

- **参数**

  - `*args`

  - `**kwargs`

- **返回**

  - Unknown
