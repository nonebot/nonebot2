---
sidebar_position: 7
description: nonebot.log 模块
---

# nonebot.log

本模块定义了 NoneBot 的日志记录 Logger。

NoneBot 使用 [`loguru`][loguru] 来记录日志信息。

自定义 logger 请参考 [自定义日志](https://nonebot.dev/docs/appendices/log)
以及 [`loguru`][loguru] 文档。

[loguru]: https://github.com/Delgan/loguru

## _var_ `logger` {#logger}

- **类型:** Logger

- **说明**

  NoneBot 日志记录器对象。

  默认信息:

  - 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
  - 等级: `INFO` ，根据 `config.log_level` 配置改变
  - 输出: 输出至 stdout

- **用法**

  ```python
  from nonebot.log import logger
  ```

## _class_ `LoguruHandler(<auto>)` {#LoguruHandler}

- **说明:** logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。

- **参数**

  auto

### _method_ `emit(record)` {#LoguruHandler-emit}

- **参数**

  - `record` (logging.LogRecord)

- **返回**

  - untyped

## _def_ `default_filter(record)` {#default-filter}

- **说明:** 默认的日志过滤器，根据 `config.log_level` 配置改变日志等级。

- **参数**

  - `record` (Record)

- **返回**

  - untyped

## _var_ `default_format` {#default-format}

- **类型:** str

- **说明:** 默认日志格式
