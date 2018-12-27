# 日志

`nonebot.log` 模块提供了一个 `logger` 对象，可用于日志。

使用 `nonebot.init()` 配置 NoneBot 时，`logger` 对象的日志级别会随 `DEBUG` 配置项的不同而不同，如果 `DEBUG` 为 `True`，则日志级别为 `DEBUG`，否则为 `INFO`。你也可以在 `nonebot.init()` 调用之后自行设置 `logger` 的日志级别。

举例：

```python
import logging

import nonebot
from nonebot.log import logger

import config


nonebot.init(config)
# logger.setLevel(logging.WARNING)

logger.info('Starting')
nonebot.run()
```
