---
sidebar_position: 9
---

# NoneBot.log 模块

## 日志

NoneBot 使用 [loguru](https://github.com/Delgan/loguru) 来记录日志信息。

自定义 logger 请参考 [loguru](https://github.com/Delgan/loguru) 文档。

## `logger`

- **说明**

  NoneBot 日志记录器对象。

- **默认信息**

  - 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`

  - 等级: `INFO` ，根据 `config.log_level` 配置改变

  - 输出: 输出至 stdout

- **用法**

```python
from nonebot.log import logger
```
