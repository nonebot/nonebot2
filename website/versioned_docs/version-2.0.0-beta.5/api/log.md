---
sidebar_position: 7
description: nonebot.log 模块
---

# nonebot.log

本模块定义了 NoneBot 的日志记录 Logger。

NoneBot 使用 [`loguru`][loguru] 来记录日志信息。

自定义 logger 请参考 [自定义日志](https://v2.nonebot.dev/docs/tutorial/custom-logger)
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

## _var_ `default_filter` {#default_filter}

- **类型:** nonebot.log.Filter

- **说明:** 默认日志等级过滤器

## _var_ `default_format` {#default_format}

- **类型:** str

- **说明:** 默认日志格式
