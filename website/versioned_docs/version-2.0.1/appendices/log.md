---
sidebar_position: 6
description: 记录与控制日志

options:
  menu:
    - category: appendices
      weight: 70
---

# 日志

无论是在开发还是在生产环境中，日志都是一个重要的功能，可以帮助我们了解运行状况、排查问题等。虽然我们可以使用 `print` 来将需要的信息输出到控制台，但是这种方式难以控制，而且不利于日志的归档、分析等。NoneBot 使用优秀的 [Loguru](https://loguru.readthedocs.io/) 库来进行日志记录。

## 记录日志

我们可以从 NoneBot 中导入 `logger` 对象，然后使用 `logger` 对象的方法来记录日志。

```python
from nonebot import logger

logger.trace("This is a trace message")
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

我们仅需一行代码即可记录对应级别的日志。日志可以通过配置 [`LOG_LEVEL` 配置项](./config.mdx#log-level)来过滤输出等级，控制台中仅会输出大于等于 `LOG_LEVEL` 的日志。默认的 `LOG_LEVEL` 为 `INFO`，即只会输出 `INFO`、`SUCCESS`、`WARNING`、`ERROR`、`CRITICAL` 级别的日志。

如果需要记录 `Exception traceback` 日志，可以向 `logger` 添加 `exception` 选项：

```python {4}
try:
    1 / 0
except ZeroDivisionError:
    logger.opt(exception=True).error("ZeroDivisionError")
```

如果需要输出彩色日志，可以向 `logger` 添加 `colors` 选项：

```python
logger.opt(colors=True).warning("We got a <red>BIG</red> problem")
```

更多日志记录方法请参考 [Loguru 文档](https://loguru.readthedocs.io/)。

## 自定义日志输出

NoneBot 在启动时会添加一个默认的日志处理器，该处理器会将日志输出到**stdout**，并且根据 `LOG_LEVEL` 配置项过滤日志等级。

默认的日志格式为：

```text
<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}
```

我们可以从 `nonebot.log` 模块导入以使用 NoneBot 的默认格式和过滤器：

```python
from nonebot.log import default_format, default_filter
```

如果需要自定义日志格式，我们需要移除 NoneBot 默认的日志处理器并添加新的日志处理器。例如，在机器人入口文件中 `nonebot.init` 之前添加以下内容：

```python title=bot.py
from nonebot.log import logger_id

# 移除 NoneBot 默认的日志处理器
logger.remove(logger_id)
# 添加新的日志处理器
logger.add(
    sys.stdout,
    level=0,
    diagnose=True,
    format="<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}",
    filter=default_filter
)
```

如果想要输出日志到文件，我们可以使用 `logger.add` 方法添加文件处理器：

```python title=bot.py
logger.add("error.log", level="ERROR", format=default_format, rotation="1 week")
```

更多日志处理器的使用方法请参考 [Loguru 文档](https://loguru.readthedocs.io/)。

## 重定向 logging 日志

`logging` 是 Python 标准库中的日志模块，NoneBot 提供了一个 logging handler 用于将 `logging` 日志重定向到 `loguru` 处理。

```python
from nonebot.log import LoguruHandler

# root logger 添加 LoguruHandler
logging.basicConfig(handlers=[LoguruHandler()])
# 或者为其他 logging.Logger 添加 LoguruHandler
logger.addHandler(LoguruHandler())
```
