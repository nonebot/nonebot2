---
sidebar_position: 1
description: nonebot.config 模块
---

# nonebot.config

本模块定义了 NoneBot 本身运行所需的配置项。

NoneBot 使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及
[`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。

配置项需符合特殊格式或 json 序列化格式
详情见 [`pydantic Field Type`](https://pydantic-docs.helpmanual.io/usage/types/) 文档。

## _class_ `Env(<auto>)` {#Env}

- **说明**

  运行环境配置。大小写不敏感。

  将会从 **环境变量** > **dotenv 配置文件** 的优先级读取环境信息。

- **参数**

  auto

### _class-var_ `environment` {#Env-environment}

- **类型:** str

- **说明**

  当前环境名。

  NoneBot 将从 `.env.{environment}` 文件中加载配置。

## _class_ `Config(<auto>)` {#Config}

- **说明**

  NoneBot 主要配置。大小写不敏感。

  除了 NoneBot 的配置项外，还可以自行添加配置项到 `.env.{environment}` 文件中。
  这些配置将会在 json 反序列化后一起带入 `Config` 类中。

  配置方法参考: [配置](https://nonebot.dev/docs/appendices/config)

- **参数**

  auto

### _class-var_ `driver` {#Config-driver}

- **类型:** str

- **说明**

  NoneBot 运行所使用的 `Driver` 。继承自 [Driver](drivers/index.md#Driver) 。

  配置格式为 `<module>[:<Driver>][+<module>[:<Mixin>]]*`。

  `~` 为 `nonebot.drivers.` 的缩写。

  配置方法参考: [配置驱动器](https://nonebot.dev/docs/advanced/driver#%E9%85%8D%E7%BD%AE%E9%A9%B1%E5%8A%A8%E5%99%A8)

### _class-var_ `host` {#Config-host}

- **类型:** IPvAnyAddress

- **说明:** NoneBot [ReverseDriver](drivers/index.md#ReverseDriver) 服务端监听的 IP/主机名。

### _class-var_ `port` {#Config-port}

- **类型:** int

- **说明:** NoneBot [ReverseDriver](drivers/index.md#ReverseDriver) 服务端监听的端口。

### _class-var_ `log_level` {#Config-log-level}

- **类型:** int | str

- **说明**

  NoneBot 日志输出等级，可以为 `int` 类型等级或等级名称。

  参考 [记录日志](https://nonebot.dev/docs/appendices/log)，[loguru 日志等级](https://loguru.readthedocs.io/en/stable/api/logger.html#levels)。

  :::tip 提示
  日志等级名称应为大写，如 `INFO`。
  :::

- **用法**

  ```conf
  LOG_LEVEL=25
  LOG_LEVEL=INFO
  ```

### _class-var_ `api_timeout` {#Config-api-timeout}

- **类型:** float | None

- **说明:** API 请求超时时间，单位: 秒。

### _class-var_ `superusers` {#Config-superusers}

- **类型:** set[str]

- **说明:** 机器人超级用户。

- **用法**

  ```conf
  SUPERUSERS=["12345789"]
  ```

### _class-var_ `nickname` {#Config-nickname}

- **类型:** set[str]

- **说明:** 机器人昵称。

### _class-var_ `command_start` {#Config-command-start}

- **类型:** set[str]

- **说明**

  命令的起始标记，用于判断一条消息是不是命令。

  参考[命令响应规则](https://nonebot.dev/docs/advanced/matcher#command)。

- **用法**

  ```conf
  COMMAND_START=["/", ""]
  ```

### _class-var_ `command_sep` {#Config-command-sep}

- **类型:** set[str]

- **说明**

  命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。

  参考[命令响应规则](https://nonebot.dev/docs/advanced/matcher#command)。

- **用法**

  ```conf
  COMMAND_SEP=["."]
  ```

### _class-var_ `session_expire_timeout` {#Config-session-expire-timeout}

- **类型:** timedelta

- **说明:** 等待用户回复的超时时间。

- **用法**

  ```conf
  SESSION_EXPIRE_TIMEOUT=120  # 单位: 秒
  SESSION_EXPIRE_TIMEOUT=[DD ][HH:MM]SS[.ffffff]
  SESSION_EXPIRE_TIMEOUT=P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
  ```
