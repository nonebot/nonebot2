# 创建一个完整的项目

上一章中我们已经运行了一个简单的 NoneBot 实例，在这一章，我们将从零开始一个完整的项目。

## 目录结构

可以使用 `nb-cli` 或者自行创建完整的项目目录：

```bash
nb create
```

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── `awesome_bot` _(**或是 src**)_
│   └── `plugins`
├── `.env` _(**可选的**)_
├── `.env.dev` _(**可选的**)_
├── `.env.prod` _(**可选的**)_
├── .gitignore
├── `bot.py`
├── docker-compose.yml
├── Dockerfile
├── `pyproject.toml`
└── README.md
:::
<!-- prettier-ignore-end -->

- `awesome_bot/plugins` 或 `src/plugins`: 用于存放编写的 bot 插件
- `.env`, `.env.dev`, `.env.prod`: 各环境配置文件
- `bot.py`: bot 入口文件
- `pyproject.toml`: 项目依赖管理文件，默认使用 [poetry](https://python-poetry.org/)

## 启动 Bot

:::warning 提示
如果您使用如 `VSCode` / `PyCharm` 等 IDE 启动 nonebot，请检查 IDE 当前工作空间目录是否与当前侧边栏打开目录一致。

- 注意：在二者不一致的环境下可能导致 nonebot 读取配置文件和插件等不符合预期

:::

通过 `nb-cli`

```bash
nb run [--file=bot.py] [--app=app]
```

或

```bash
python bot.py
```

:::tip 提示
如果在 bot 入口文件内定义了 asgi server， `nb-cli` 将会为你启动**冷重载模式**（当文件发生变动时自动重启 NoneBot 实例）
:::
