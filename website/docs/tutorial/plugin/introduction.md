---
sidebar_position: 0
description: 插件入门
---

# 插件入门

## 插件结构

在编写插件之前，首先我们需要了解一下插件的概念。

在 NoneBot 中，插件可以是 Python 的一个模块 `module` ，也可以是一个包 `package` 。NoneBot 会在导入时对这些模块或包做一些特殊的处理使得他们成为一个插件。插件间应尽量减少耦合，可以进行有限制的插件间调用，NoneBot 能够正确解析插件间的依赖关系。

下面详细介绍两种插件的结构：

### 模块插件（单文件形式）

在合适的路径创建一个 `.py` 文件即可。例如在 [创建项目](../create-project.mdx) 中创建的项目中，我们可以在 `awesome_bot/plugins/` 目录中创建一个文件 `foo.py`。

```tree title=Project {4}
📦 AweSome-Bot
├── 📂 awesome_bot
│   └── 📂 plugins
|       └── 📜 foo.py
├── 📜 .env
├── 📜 .env.dev
├── 📜 .env.prod
├── 📜 .gitignore
├── 📜 bot.py
├── 📜 docker-compose.yml
├── 📜 Dockerfile
├── 📜 pyproject.toml
└── 📜 README.md
```

这个时候它已经可以被称为一个插件了，尽管它还什么都没做。

### 包插件（文件夹形式）

在合适的路径创建一个文件夹，并在文件夹内创建文件 `__init__.py` 即可。例如在 [创建项目](../create-project.mdx) 中创建的项目中，我们可以在 `awesome_bot/plugins/` 目录中创建一个文件夹 `foo`，并在这个文件夹内创建一个文件 `__init__.py`。

```tree title=Project {4,5}
📦 AweSome-Bot
├── 📂 awesome_bot
│   └── 📂 plugins
|       └── 📂 foo.py
|           └── 📜 __init__.py
├── 📜 .env
├── 📜 .env.dev
├── 📜 .env.prod
├── 📜 .gitignore
├── 📜 bot.py
├── 📜 docker-compose.yml
├── 📜 Dockerfile
├── 📜 pyproject.toml
└── 📜 README.md
```

这个时候 `foo` 就是一个合法的 Python 包了，同时也是合法的 NoneBot 插件，插件内容可以在 `__init__.py` 中编写。

## 创建插件

:::danger 警告
请注意，插件名称不能存在重复，即所有模块插件的文件名和所有包插件的文件夹名不能存在相同。
:::

除了通过手动创建的方式以外，还可以通过 `nb-cli` 来创建插件，`nb-cli` 会为你在合适的位置创建一个模板包插件。

```bash
nb plugin create
```
