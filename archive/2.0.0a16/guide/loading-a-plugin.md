# 加载插件

在 [创建一个完整的项目](creating-a-project) 一章节中，我们已经创建了插件目录 `awesome_bot/plugins`，现在我们在机器人入口文件中加载它。当然，你也可以单独加载一个插件。

## 加载内置插件

在 `bot.py` 文件中添加以下行：

```python{8}
import nonebot
from nonebot.adapters.cqhttp import Bot

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot) # 注册 CQHTTP 的 Adapter
nonebot.load_builtin_plugins() # 加载 nonebot 内置插件

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

::: warning
目前, 内建插件仅支持 CQHTTP 的 Adapter

如果您使用的是其他 Adapter, 请移步该 Adapter 相应的文档
:::

这将会加载 nonebot 内置的插件，它包含：

- 命令 `say`：可由**superuser**使用，可以将消息内容由特殊纯文本转为富文本
- 命令 `echo`：可由任何人使用，将消息原样返回

以上命令均需要指定机器人，即私聊、群聊内@机器人、群聊内称呼机器人昵称。参考 [Rule: to_me](../api/rule.md#to-me)

## 加载插件目录

在 `bot.py` 文件中添加以下行：

```python{6}
import nonebot

nonebot.init()

# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
nonebot.load_plugins("awesome_bot/plugins")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

:::tip 提示
加载插件目录时，目录下以 `_` 下划线开头的插件将不会被加载！
:::

:::warning 提示
**不能存在相同名称的插件！**
:::

:::danger 警告
插件间不应该存在过多的耦合，如果确实需要导入某个插件内的数据，可以参考 [进阶-跨插件访问](../advanced/export-and-require.md)
:::

## 加载单个插件

在 `bot.py` 文件中添加以下行：

```python{6,8}
import nonebot

nonebot.init()

# 加载一个 pip 安装的插件
nonebot.load_plugin("nonebot_plugin_status")
# 加载本地的单独插件
nonebot.load_plugin("awesome_bot.plugins.xxx")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

## 从 json 文件中加载插件

在 `bot.py` 文件中添加以下行：

```python{6}
import nonebot

nonebot.init()

# 从 plugin.json 加载插件
nonebot.load_from_json("plugin.json")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

**json 文件示例**

```json
{
  "plugins": ["nonebot_plugin_status", "awesome_bot.plugins.xxx"],
  "plugin_dirs": ["awesome_bot/plugins"]
}
```

## 从 toml 文件中加载插件

在 `bot.py` 文件中添加以下行：

```python{6}
import nonebot

nonebot.init()

# 从 pyproject.toml 加载插件
nonebot.load_from_toml("pyproject.toml")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

**toml 文件示例：**

```toml
[nonebot.plugins]
plugins = ["nonebot_plugin_status", "awesome_bot.plugins.xxx"]
plugin_dirs = ["awesome_bot/plugins"]
```

::: tip
nb-cli 默认使用 `pyproject.toml` 加载插件。
:::

## 子插件(嵌套插件)

在插件中同样可以加载子插件，例如如下插件目录结构：

<!-- prettier-ignore-start -->
:::vue
foo_plugin
├── `plugins`
│   ├── `sub_plugin1`
│   │  └── \_\_init\_\_.py
│   └── `sub_plugin2.py`
├── `__init__.py`
└── config.py
:::
<!-- prettier-ignore-end -->

在插件目录下的 `__init__.py` 中添加如下代码：

```python
from pathlib import Path

import nonebot

# store all subplugins
_sub_plugins = set()
# load sub plugins
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve()))
```

插件将会被加载并存储于 `_sub_plugins` 中。

## 运行结果

尝试运行 `nb run` 或者 `python bot.py`，可以看到日志输出了类似如下内容：

```plain
09-19 21:51:59 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"
09-19 21:51:59 [INFO] nonebot | Succeeded to import "plugin_in_folder"
```
