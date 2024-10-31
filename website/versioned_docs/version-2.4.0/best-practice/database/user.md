---
sidebar_position: 2
description: 用户指南
---

# 用户指南

`nonebot-plugin-orm` 功能强大且复杂，使用上有一定难度。
不过，对于用户而言，只需要掌握部分功能即可。

:::caution 注意
请注意区分插件的项目名（如：`nonebot-plugin-wordcloud`）和模块名（如：`nonebot_plugin_wordcloud`）。`nonebot-plugin-orm` 中统一使用插件模块名。参见 [插件命名规范](../../developer/plugin-publishing#插件命名规范)。
:::

## 示例

### 创建新机器人

我们想要创建一个机器人，并安装 `nonebot-plugin-wordcloud` 插件，只需要执行以下命令：

```shell
nb init  # 初始化项目文件夹

pip install nonebot-plugin-orm[sqlite]  # 安装 nonebot-plugin-orm，并附带 SQLite 支持

nb plugin install nonebot-plugin-wordcloud  # 安装插件

# nb orm heads  # 查看有什么插件使用到了数据库（可选）

nb orm upgrade  # 升级数据库

# nb orm check  # 检查一下数据库模式是否与模型定义一致（可选）

nb run  # 启动机器人
```

### 卸载插件

我们已经安装了 `nonebot-plugin-wordcloud` 插件，但是现在想要卸载它，并且**删除它的数据**，只需要执行以下命令：

```shell
nb plugin uninstall nonebot-plugin-wordcloud  # 卸载插件

# nb orm heads  # 查看有什么插件使用到了数据库。（可选）

nb orm downgrade nonebot_plugin_wordcloud@base  # 降级数据库，删除数据

# nb orm check  # 检查一下数据库模式是否与模型定义一致（可选）
```

## CLI

接下来，让我们了解下示例中出现的 CLI 命令的含义：

### heads

显示所有的分支头。一般一个分支对应一个插件。

```shell
nb orm heads
```

输出格式为 `<迁移 ID> (<插件模块名>) (<头部类型>)`：

```
46327b837dd8 (nonebot_plugin_chatrecorder) (head)
9492159f98f7 (nonebot_plugin_user) (head)
71a72119935f (nonebot_plugin_session_orm) (effective head)
ade8cdca5470 (nonebot_plugin_wordcloud) (head)
```

### upgrade

升级数据库。每次安装新的插件或更新插件版本后，都需要执行此命令。

```shell
nb orm upgrade <插件模块名>@<迁移 ID>
```

其中，`<插件模块名>@<迁移 ID>` 是可选参数。如果不指定，则会将所有分支升级到最新版本，这也是最常见的用法：

```shell
nb orm upgrade
```

### downgrade

降级数据库。当需要回滚插件版本或删除插件时，可以执行此命令。

```shell
nb orm downgrade <插件模块名>@<迁移 ID>
```

其中，`<迁移 ID>` 也可以是 `base`，即回滚到初始状态。常用于卸载插件后删除其数据：

```shell
nb orm downgrade <插件模块名>@base
```

### check

检查数据库模式是否与模型定义一致。机器人启动前会自动运行此命令（`ALEMBIC_STARTUP_CHECK=true` 时），并在检查失败时阻止启动。

```shell
nb orm check
```

## 配置

### sqlalchemy_database_url

默认数据库连接 URL。参见 [数据库驱动和后端](.#数据库驱动和后端) 和 [引擎配置 — SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)。

```shell
SQLALCHEMY_DATABASE_URL=dialect+driver://username:password@host:port/database
```

### sqlalchemy_bind

bind keys（一般为插件模块名）到数据库连接 URL、[`create_async_engine()`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) 参数字典或 [`AsyncEngine`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine) 实例的字典。
例如，我们想要让 `nonebot-plugin-wordcloud` 插件使用一个 SQLite 数据库，并开启 [Echo 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) 便于 debug，而其他插件使用默认的 PostgreSQL 数据库，可以这样配置：

```shell
SQLALCHEMY_BINDS='{
    "": "postgresql+psycopg://scott:tiger@localhost/mydatabase",
    "nonebot_plugin_wordcloud": {
        "url": "sqlite+aiosqlite://",
        "echo": true
    }
}'
```

### sqlalchemy_engine_options

[`create_async_engine()`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) 默认参数字典。

```shell
SQLALCHEMY_ENGINE_OPTIONS='{
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": true
}'
```

### sqlalchemy_echo

开启 [Echo 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) 和 [Echo Pool 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo_pool) 便于 debug。

```shell
SQLALCHEMY_ECHO=true
```

:::caution 注意
以上配置之间有覆盖关系，遵循特殊优先于一般的原则，具体为 [`sqlalchemy_database_url`](#sqlalchemy_database_url) > [`sqlalchemy_bind`](#sqlalchemy_bind) > [`sqlalchemy_echo`](#sqlalchemy_echo) > [`sqlalchemy_engine_options`](#sqlalchemy_engine_options)。
但覆盖顺序并非显而易见，出于清晰考虑，请只配置必要的选项。
:::
