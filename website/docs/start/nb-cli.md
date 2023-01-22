---
sidebar_position: 90
description: 使用 nb-cli 帮助开发

options:
  menu:
    weight: 11
    category: guide
---

# 使用脚手架

`nb-cli` 详细参考文档已移至 <https://cli.nonebot.dev>。

## 安装

```bash
pipx install nb-cli
```

## 初次使用

在安装完成之后，即可在命令行使用 nb-cli 的命令 `nb` 进行开发：

```bash
nb
```

:::warning 注意
通常情况下，你可以直接在命令行使用 `nb` 命令。如果出现无法找到命令的情况（例如：`Command not found`），请参考 [pipx 文档](https://pypa.github.io/pipx/) 检查你的环境变量。
:::

## 使用方式

nb-cli 具有两种使用方式：

1. 命令行指令

   查看帮助信息：

   ```bash
   $ nb --help
   Usage: nb [OPTIONS] COMMAND [ARGS]...

   Options:
     -V, --version  Show the version and exit.
     --help         Show this message and exit.

   ...
   ```

   查看子命令帮助：

   ```bash
   $ nb plugin --help
   Usage: nb plugin [OPTIONS] COMMAND [ARGS]...

     Manage Bot Plugin.

   Options:
     --help  Show this message and exit.

   ...
   ```

2. 交互式选择（支持鼠标）

   交互式选择菜单：

   ```bash
   $ nb
   Welcome to NoneBot CLI!
   [?] What do you want to do? (Use ↑ and ↓ to choose, Enter to submit)
   ...
   ```

   交互式子命令菜单：

   ```bash
   $ nb plugin
   [?] What do you want to do? (Use ↑ and ↓ to choose, Enter to submit)
   ...
   ```
