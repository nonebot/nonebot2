# 编写插件

本章将以一个天气查询插件为例，教学如何编写自己的命令。

## 加载插件

在 [创建一个完整的项目](creating-a-project) 一章节中，我们已经创建了插件目录 `awesome_bot/plugins`，现在我们在机器人入口文件中加载它。当然，你也可以单独加载一个插件。

:::tip 提示
加载插件目录时，目录下以 `_` 下划线开头的插件将不会被加载！
:::

在 `bot.py` 文件中添加以下行：

```python{5,7}
import nonebot

nonebot.init()
# 加载单独的一个插件，参数为合法的python包名
nonebot.load_plugin("nonebot.plugins.base")
# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
nonebot.load_plugins("awesome_bot/plugins")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

尝试运行 `nb run` 或者 `python bot.py`，可以看到日志输出了类似如下内容：

```plain
09-19 21:51:59 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"
09-19 21:51:59 [INFO] nonebot | Succeeded to import "plugin_in_folder"
```

## 创建插件

现在我们已经有了一个空的插件目录，我们可以开始创建插件了！插件有两种形式

### 单文件形式

在插件目录下创建名为 `weather.py` 的 Python 文件，暂时留空，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `weather.py`
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

### 包形式

在插件目录下创建文件夹 `weather`，并在该文件夹下创建文件 `__init__.py`，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `weather`
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

这个时候 `weather` 就是一个合法的 Python 包了，同时也是合法的 NoneBot 插件，插件内容可以在 `__init__.py` 中编写。

## 编写真正的内容
