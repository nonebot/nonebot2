# 部署

## 基本部署

NoneBot 所基于的 python-aiocqhttp 库使用的 web 框架是 Quart，因此 NoneBot 的部署方法和 Quart 一致（[Deploying Quart](https://pgjones.gitlab.io/quart/deployment.html)）。

Quart 官方建议使用 Hypercorn 来部署，这需要一个 ASGI app 对象，在 NoneBot 中，可使用 `nonebot.get_bot().asgi` 获得 ASGI app 对象。

具体地，通常在项目根目录下创建一个 `run.py` 文件如下：

```python
import os
import sys

import nonebot

import config

nonebot.init(config)
bot = nonebot.get_bot()
app = bot.asgi

if __name__ == '__main__':
    bot.run()
```

然后使用下面命令部署：

```python
hypercorn run:app
```

另外，NoneBot 配置文件的 `DEBUG` 项默认为 `True`，在生产环境部署时请注意修改为 `False` 以提高性能。

## 使用 Docker Compose 与 酷Q 同时部署
