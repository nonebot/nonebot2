---
sidebar_position: 2
description: 填写与获取插件相关的信息

options:
  menu:
    - category: advanced
      weight: 30
---

# 插件信息

NoneBot 是一个插件化的框架，可以通过加载插件来扩展功能。同时，我们也可以通过 NoneBot 的插件系统来获取相关信息，例如插件的名称、使用方法，用于收集帮助信息等。下面我们将介绍如何为插件添加元数据，以及如何获取插件信息。

## 插件元数据

在 NoneBot 中，插件 [`Plugin`](../api/plugin/model.md#Plugin) 对象中存储了插件系统所需要的一系列信息。包括插件的索引名称、插件模块、插件中的事件响应器、插件父子关系等。通常，只有插件开发者才需要关心这些信息，而插件使用者或者机器人用户想要看到的是插件使用方法等帮助信息。因此，我们可以为插件添加插件元数据 `PluginMetadata`，它允许插件开发者为插件添加一些额外的信息。这些信息编写于插件模块的顶层，可以直接通过源码查看，或者通过 NoneBot 插件系统获取收集到的信息，通过其他方式发送给机器人用户等。

现在，假设我们有一个插件 `example`, 它的模块结构如下：

```tree {4-6} title=Project
📦 awesome-bot
├── 📂 awesome_bot
│   └── 📂 plugins
|       └── 📂 example
|           ├── 📜 __init__.py
|           └── 📜 config.py
├── 📜 pyproject.toml
└── 📜 README.md
```

我们需要在插件顶层模块 `example/__init__.py` 中添加插件元数据，如下所示：

```python {1,5-12} title=example/__init__.py
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="示例插件",
    description="这是一个示例插件",
    usage="没什么用",
    type="application",
    config=Config,
    extra={},
)
```

我们可以看到，插件元数据 `PluginMetadata` 有三个基本属性：插件名称、插件描述、插件使用方法。除此之外，还有几个可选的属性（具体填写见[发布插件](../developer/plugin-publishing.mdx#填写插件元数据)章节）：

- `type`：插件类别，发布插件必填。当前有效类别有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）；
- `homepage`：插件项目主页，发布插件必填；
- `config`：插件的[配置类](../appendices/config.mdx#插件配置)，如无配置类可不填；
- `supported_adapters`：支持的适配器模块名集合，若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写；
- `extra`：一个字典，可以用于存储任意信息。其他插件可以通过约定 `extra` 字典的键名来达成收集某些特殊信息的目的。

请注意，这里的**插件名称**是供使用者或机器人用户查看的，与插件索引名称无关。**插件索引名称（插件模块名称）**仅用于 NoneBot 插件系统**内部索引**。

## 获取插件信息

NoneBot 提供了多种获取插件对象的方法，例如获取当前所有已导入的插件：

```python
import nonebot

plugins: set[Plugin] = nonebot.get_loaded_plugins()
```

也可以通过插件索引名称获取插件对象：

```python
import nonebot

plugin: Plugin | None = nonebot.get_plugin("example")
```

或者通过模块路径获取插件对象：

```python
import nonebot

plugin: Plugin | None = nonebot.get_plugin_by_module_name("awesome_bot.plugins.example")
```

如果需要获取所有当前声明的插件名称（可能还未加载），可以使用 `get_available_plugin_names` 函数：

```python
import nonebot

plugin_names: set[str] = nonebot.get_available_plugin_names()
```

插件对象 `Plugin` 中包含了多个属性：

- `name`：插件索引名称
- `module`：插件模块
- `module_name`：插件模块路径
- `manager`：插件管理器
- `matcher`：插件中定义的事件响应器
- `parent_plugin`：插件的父插件
- `sub_plugins`：插件的子插件集合
- `metadata`：插件元数据

通过这些属性以及插件元数据，我们就可以收集所需要的插件信息了。
