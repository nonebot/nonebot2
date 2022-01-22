---
sidebar_position: 0
description: 创建并运行项目

options:
  menu:
    weight: 20
    category: guide
---

# 创建项目

可以使用 `nb-cli` 或者自行创建完整的项目目录：

```bash
nb create
```

## 目录结构

```tree title=Project
📦 AweSome-Bot
├── 📂 awesome_bot         # 或是 src
│   └── 📜 plugins
├── 📜 .env                # 可选的
├── 📜 .env.dev            # 可选的
├── 📜 .env.prod           # 可选的
├── 📜 .gitignore
├── 📜 bot.py
├── 📜 docker-compose.yml
├── 📜 Dockerfile
├── 📜 pyproject.toml
└── 📜 README.md
```

- `awesome_bot/plugins` 或 `src/plugins`: 用于存放编写的 bot 插件
- `.env`, `.env.dev`, `.env.prod`: 各环境配置文件
- `bot.py`: bot 入口文件
- `pyproject.toml`: 项目插件配置文件
- `Dockerfile`, `docker-compose.yml`: Docker 镜像配置文件

## 启动 Bot

:::warning 提示
如果您使用如 `VSCode` / `PyCharm` 等 IDE 启动 nonebot，请检查 IDE 当前工作空间目录是否与当前侧边栏打开目录一致。

> 注意：在二者不一致的环境下可能导致 nonebot 读取配置文件和插件等不符合预期

:::

1. 通过 `nb-cli`

   ```bash
   nb run [--file=bot.py] [--app=app]
   ```

   其中 `--file` 参数可以指定 bot 入口文件，默认为 `bot.py`，`--app` 参数可以指定 asgi server，默认为 `app`。

2. 直接通过 `python` 启动

   ```bash
   python bot.py
   ```

:::tip 提示
如果在 bot 入口文件内定义了 asgi server， `nb-cli` 将会为你启动**冷重载模式**（当文件发生变动时自动重启 NoneBot 实例）
:::
