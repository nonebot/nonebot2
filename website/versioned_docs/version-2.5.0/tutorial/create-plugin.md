---
sidebar_position: 3
description: 创建并加载自定义插件

options:
  menu:
    - category: tutorial
      weight: 50
---

# 插件编写准备

在正式编写插件之前，我们需要先了解一下插件的概念。

## 插件结构

在 NoneBot 中，插件即是 Python 的一个[模块（module）](https://docs.python.org/zh-cn/3/glossary.html#term-module)。NoneBot 会在导入时对这些模块做一些特殊的处理使得他们成为一个插件。插件间应尽量减少耦合，可以进行有限制的相互调用，NoneBot 能够正确解析插件间的依赖关系。

### 单文件插件

一个普通的 `.py` 文件即可以作为一个插件，例如创建一个 `foo.py` 文件：

```tree title=Project
📂 plugins
└── 📜 foo.py
```

这个时候模块 `foo` 已经可以被称为一个插件了，尽管它还什么都没做。

### 包插件

一个包含 `__init__.py` 的文件夹即是一个常规 Python [包 `package`](https://docs.python.org/zh-cn/3/glossary.html#term-regular-package)，例如创建一个 `foo` 文件夹：

```tree title=Project
📂 plugins
└── 📂 foo
    └── 📜 __init__.py
```

这个时候包 `foo` 同样是一个合法的插件，插件内容可以在 `__init__.py` 文件中编写。

## 创建插件

:::caution 注意
如果在之前的[快速上手](../quick-start.mdx)章节中已经使用 `bootstrap` 模板创建了项目，那么你需要做出如下修改：

1. 在项目目录中创建一个两层文件夹 `awesome_bot/plugins`

   ```tree title=Project
   📦 awesome-bot
   ├── 📂 .venv
   ├── 📂 awesome_bot
   │   └── 📂 plugins
   ├── 📜 .env.prod
   ├── 📜 pyproject.toml
   └── 📜 README.md
   ```

2. 修改 `pyproject.toml` 文件中的 `nonebot` 配置项，在 `plugin_dirs` 中添加 `awesome_bot/plugins`

   ```toml title=pyproject.toml
   [tool.nonebot]
   plugin_dirs = ["awesome_bot/plugins"]
   ```

:::

:::caution 注意
如果在之前的[创建项目](./application.mdx)章节中手动创建了相关文件，那么你需要做出如下修改：

1. 在项目目录中创建一个两层文件夹 `awesome_bot/plugins`

   ```tree title=Project
   📦 awesome-bot
   ├── 📂 awesome_bot
   │   └── 📂 plugins
   └── 📜 bot.py
   ```

2. 修改 `bot.py` 文件中的加载插件部分，取消注释或者添加如下代码

   ```python title=bot.py
   # 在这里加载插件
   nonebot.load_builtin_plugins("echo")  # 内置插件
   nonebot.load_plugins("awesome_bot/plugins")  # 本地插件
   ```

:::

创建插件可以通过 `nb-cli` 命令从完整模板创建，也可以手动新建空白文件。通过以下命令创建一个名为 `weather` 的插件：

```bash
$ nb plugin create
[?] 插件名称: weather
[?] 使用嵌套插件? (y/N) N
[?] 请输入插件存储位置: awesome_bot/plugins
```

`nb-cli` 会在 `awesome_bot/plugins` 目录下创建一个名为 `weather` 的文件夹，其中包含的文件将在稍后章节中用到。

```tree title=Project
📦 awesome-bot
├── 📂 .venv
├── 📂 awesome_bot
│   └── 📂 plugins
|       └── 📂 weather
|           ├── 📜 __init__.py
|           └── 📜 config.py
├── 📜 .env.prod
├── 📜 pyproject.toml
└── 📜 README.md
```

## 加载插件

:::danger 警告
请勿在插件被加载前 `import` 插件模块，这会导致 NoneBot 无法将其转换为插件而出现意料之外的情况。
:::

加载插件是在机器人入口文件中完成的，需要在框架初始化之后，运行之前进行。

请注意，加载的插件模块名称（插件文件名或文件夹名）**不能相同**，且每一个插件**只能被加载一次**，重复加载将会导致异常。

如果你使用 `nb-cli` 管理插件，那么你可以跳过这一节，`nb-cli` 将会自动处理加载。

如果你**使用自定义的入口文件** `bot.py`，那么你需要在 `bot.py` 中加载插件。

```python {5} title=bot.py
import nonebot

nonebot.init()

# 加载插件

nonebot.run()
```

加载插件的方式有多种，但在底层的加载逻辑是一致的。以下是为加载插件提供的几种方式：

### `load_plugin`

通过点分割模块名称或使用 [`pathlib`](https://docs.python.org/zh-cn/3/library/pathlib.html) 的 `Path` 对象来加载插件。通常用于加载第三方插件或者项目插件。例如：

```python
from pathlib import Path

nonebot.load_plugin("path.to.your.plugin")  # 加载第三方插件
nonebot.load_plugin(Path("./path/to/your/plugin.py"))  # 加载项目插件
```

:::caution 注意
请注意，本地插件的路径应该为相对机器人 **入口文件（通常为 bot.py）** 可导入的，例如在项目 `plugins` 目录下。
:::

### `load_plugins`

加载传入插件目录中的所有插件，通常用于加载一系列本地编写的项目插件。例如：

```python
nonebot.load_plugins("src/plugins", "path/to/your/plugins")
```

:::caution 注意
请注意，插件目录应该为相对机器人 **入口文件（通常为 bot.py）** 可导入的，例如在项目 `plugins` 目录下。
:::

### `load_all_plugins`

这种加载方式是以上两种方式的混合，加载所有传入的插件模块名称，以及所有给定目录下的插件。例如：

```python
nonebot.load_all_plugins(["path.to.your.plugin"], ["path/to/your/plugins"])
```

### `load_from_json`

通过 JSON 文件加载插件，是 [`load_all_plugins`](#load_all_plugins) 的 JSON 变种。通过读取 JSON 文件中的 `plugins` 字段和 `plugin_dirs` 字段进行加载。例如：

```json title=plugin_config.json
{
  "plugins": ["path.to.your.plugin"],
  "plugin_dirs": ["path/to/your/plugins"]
}
```

```python
nonebot.load_from_json("plugin_config.json", encoding="utf-8")
```

:::tip 提示
如果 JSON 配置文件中的字段无法满足你的需求，可以使用 [`load_all_plugins`](#load_all_plugins) 方法自行读取配置来加载插件。
:::

### `load_from_toml`

通过 TOML 文件加载插件，是 [`load_all_plugins`](#load_all_plugins) 的 TOML 变种。通过读取 TOML 文件中的 `[tool.nonebot]` Table 中的 `plugin_dirs` Array 与
`[tool.nonebot.plugins]` Table 中的多个 Array 进行加载。例如：

```toml title=plugin_config.toml
[tool.nonebot]
plugin_dirs = ["path/to/your/plugins"]

[tool.nonebot.plugins]
"@local" = ["path.to.your.plugin"]  # 本地插件等非插件商店来源的插件
"nonebot-plugin-someplugin" = ["nonebot_plugin_someplugin"]  # 插件商店来源的插件
```

```python
nonebot.load_from_toml("plugin_config.toml", encoding="utf-8")
```

:::tip 提示
如果 TOML 配置文件中的字段无法满足你的需求，可以使用 [`load_all_plugins`](#load_all_plugins) 方法自行读取配置来加载插件。
:::

### `load_builtin_plugin`

加载一个内置插件，传入的插件名必须为 NoneBot 内置插件。该方法是 [`load_plugin`](#load_plugin) 的封装。例如：

```python
nonebot.load_builtin_plugin("echo")
```

### `load_builtin_plugins`

加载传入插件列表中的所有内置插件。例如：

```python
nonebot.load_builtin_plugins("echo", "single_session")
```

### 其他加载方式

有关其他插件加载的方式，可参考[跨插件访问](../advanced/requiring.md)和[嵌套插件](../advanced/plugin-nesting.md)。
