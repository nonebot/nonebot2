# 创建插件

如果之前使用 `nb-cli` 生成了项目结构，那我们已经有了一个空的插件目录 `Awesome-Bot/awesome_bot/plugins`，并且它已在 `bot.py` 中被加载，我们现在可以开始创建插件了！

插件通常有两种形式，下面分别介绍

## 单文件形式

在插件目录下创建名为 `foo.py` 的 Python 文件，暂时留空，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `foo.py`
├── .env
├── .env.dev
├── .env.prod
├── .gitignore
├── bot.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
:::
<!-- prettier-ignore-end -->

这个时候它已经可以被称为一个插件了，尽管它还什么都没做。

## 包形式(推荐)

在插件目录下创建文件夹 `foo`，并在该文件夹下创建文件 `__init__.py`，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `foo`
│         └── `__init__.py`
├── .env
├── .env.dev
├── .env.prod
├── .gitignore
├── bot.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
:::
<!-- prettier-ignore-end -->

这个时候 `foo` 就是一个合法的 Python 包了，同时也是合法的 NoneBot 插件，插件内容可以在 `__init__.py` 中编写。

### 推荐结构(仅供参考)

<!-- prettier-ignore-start -->
:::vue
foo
├── `__init__.py`
├── `config.py`
├── `data_source.py`
└── `model.py`
:::
<!-- prettier-ignore-end -->

#### \_\_init\_\_.py

在该文件中编写各类事件响应及处理逻辑。

#### config.py

在该文件中使用 `pydantic` 定义插件所需要的配置项以及类型。

示例：

```python
from pydantic import BaseSetting


class Config(BaseSetting):

    # plugin custom config
    plugin_setting: str = "default"

    class Config:
        extra = "ignore"
```

并在 `__init__.py` 文件中添加以下行

```python
import nonebot
from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
```

此时就可以通过 `plugin_config.plugin_setting` 获取到插件所需要的配置项了。

#### data_source.py

在该文件中编写数据获取函数。

:::warning 警告
数据获取应尽量使用**异步**处理！例如使用 [httpx](https://www.python-httpx.org/) 而非 [requests](https://requests.readthedocs.io/en/master/)
:::

#### model.py

在该文件中编写数据库模型。
