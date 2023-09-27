---
sidebar_position: 0
description: 创建一个 NoneBot 项目

options:
  menu:
    - category: tutorial
      weight: 20
---

# 手动创建项目

在[快速上手](../quick-start.mdx)中，我们已经介绍了如何安装和使用 `nb-cli` 创建一个项目。在本章节中，我们将简要介绍如何在不使用 `nb-cli` 的方式创建一个机器人项目的**最小实例**并启动。如果你想要了解 NoneBot 的启动流程，也可以阅读本章节。

:::caution
我们十分不推荐直接创建机器人项目，请优先考虑使用 nb-cli 进行项目创建。
:::

一个机器人项目的**最小实例**中**至少**需要包含以下内容:

- 入口文件：初始化并运行机器人的 Python 文件
- 配置文件：存储机器人启动所需的配置
- 插件：为机器人提供具体的功能

下面我们创建一个项目文件夹，来存放项目所需文件，以下步骤均在该文件夹中进行。

## 安装依赖

在创建项目前，我们首先需要将项目所需依赖安装至环境中。

1. （可选）创建虚拟环境，以 venv 为例

   ```bash
   python -m venv .venv --prompt nonebot2
   # windows
   .venv\Scripts\activate
   # linux/macOS
   source .venv/bin/activate
   ```

2. 安装 nonebot2 以及驱动器

   ```bash
   pip install 'nonebot2[fastapi]'
   ```

   驱动器包名可以在 [驱动器商店](/store/drivers) 中找到。

3. 安装适配器

   ```bash
   pip install nonebot-adapter-console
   ```

   适配器包名可以在 [适配器商店](/store/adapters) 中找到。

## 创建配置文件

配置文件用于存放 NoneBot 运行所需要的配置项，使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及 [`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。配置项需符合 dotenv 格式，复杂类型数据需使用 JSON 格式填写。具体可选配置方式以及配置项详情参考[配置](../appendices/config.mdx)。

在**项目文件夹**中创建一个 `.env` 文本文件，并写入以下内容:

```bash title=.env
HOST=0.0.0.0  # 配置 NoneBot 监听的 IP / 主机名
PORT=8080  # 配置 NoneBot 监听的端口
COMMAND_START=["/"]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符
```

## 创建入口文件

入口文件（ Entrypoint ）顾名思义，是用来初始化并运行机器人的 Python 文件。入口文件需要完成框架的初始化、注册适配器、加载插件等工作。

:::tip 提示
如果你使用 `nb-cli` 创建项目，入口文件不会被创建，该文件功能会被 `nb run` 命令代替。
:::

在**项目文件夹**中创建一个 `bot.py` 文件，并写入以下内容:

```python title=bot.py
import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter  # 避免重复命名

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
# nonebot.load_plugins("awesome_bot/plugins")  # 本地插件

if __name__ == "__main__":
    nonebot.run()
```

我们暂时不需要了解其中内容的含义，这些将会在稍后的章节中逐一介绍。在创建完成以上文件并确认已安装所需适配器和插件后，即可运行机器人。

## 运行机器人

在**项目文件夹**中，使用配置好环境的 Python 解释器运行入口文件（如果使用虚拟环境，请先激活虚拟环境）:

```bash
python bot.py
```

如果你后续使用了 `nb-cli` ，你仍可以使用 `nb run` 命令来运行机器人，`nb-cli` 会自动检测入口文件 `bot.py` 是否存在并运行。
