---
sidebar_position: 2
description: 规范定义插件配置项
---

# 定义插件配置

通常，插件可以从配置文件中读取自己的配置项，但是由于额外的全局配置项没有预先定义的问题，导致开发时编辑器无法提示字段与类型，以及运行时没有对配置项直接进行检查。那么就需要一种方式来规范定义插件配置项。

## 定义配置模型

在 NoneBot2 中，我们使用强大高效的 [Pydantic](https://pydantic-docs.helpmanual.io/) 来定义配置模型，这个模型可以被用于配置的读取和类型检查等。例如，我们可以定义一个配置模型包含一个 string 类型的配置项：

```python title=config.py {3,4}
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    token: str
```

:::important 参考
更多丰富的模型定义方法（默认值、自定义 validator 等），请参考 [Pydantic](https://pydantic-docs.helpmanual.io/) 文档。
:::

## 读取配置

定义完成配置模型后，我们可以在插件加载时获取全局配置，导入插件自身的配置模型：

```python title=__init__.py {5}
from nonebot import get_driver

from .config import Config

plugin_config = Config.parse_obj(get_driver().config)
```

至此，插件已经成功读取了自身所需的配置项，并且具有字段和类型提示，也可以对配置进行运行时修改。
