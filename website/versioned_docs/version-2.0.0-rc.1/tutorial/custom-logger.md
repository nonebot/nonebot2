---
sidebar_position: 100
description: 修改日志级别与输出
---

# 自定义日志

NoneBot 使用 [Loguru](https://loguru.readthedocs.io/) 进行日志记录，并提供了一些内置的格式和过滤器等。

## 默认日志

NoneBot 启动时会添加一个默认的日志 handler。此 handler 将会将日志输出到 **stdout**，并且根据配置的日志级别进行过滤。

[默认格式](../api/log.md#default_format)):

```python
default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}"
)

from nonebot.log import default_format
```

[默认过滤器](../api/log.md#default_filter):

```python
from nonebot.log import default_filter
```

## 转移 logging 日志

NoneBot 提供了一个 logging handler 用于将日志输出转移至 loguru 处理。将 logging 的默认 handler 替换为 `LoguruHandler` 即可。

```python
from nonebot.log import LoguruHandler
```

## 自定义日志记录

如果需要移除 NoneBot 的默认日志 handler，可以在 `nonebot.init` 之前进行如下操作：

```python
from nonebot.log import logger, logger_id

logger.remove(logger_id)
```

如果需要添加自定义的日志 handler，可以在 `nonebot.init` 之前添加 handler，参考 [loguru 文档](https://loguru.readthedocs.io/)。

示例：

```python
from nonebot.log import logger, default_format

logger.add("error.log", level="ERROR", format=default_format, rotation="1 week")
```
