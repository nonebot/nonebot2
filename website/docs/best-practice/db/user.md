---
sidebar_position: 2
description: 用户指南
---

# 用户指南

`nonebot-plugin-orm` 功能强大但又复杂，有较大门槛。
不过，对于插件或机器人用户而言，只需要掌握部分功能即可。

## 配置

### sqlalchemy_database_url

默认数据库连接 URL。参见 [数据库服务](.#数据库服务) 和 [引擎配置 — SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)。

```shell
SQLALCHEMY_DATABASE_URL=dialect+driver://username:password@host:port/database
```

### sqlalchemy_bind

bind keys（一般为 [插件模块名](../../developer/plugin-publishing#插件命名规范)）到数据库连接 URL、[`create_async_engine()`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) 参数字典或 [`AsyncEngine`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncEngine) 实例的字典。
例如，我们想要让 `nonebot_plugin_user` 插件使用一个 SQLite 数据库，并开启 [Echo 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) 便于 debug，而其他插件使用默认的 PostgreSQL 数据库，可以这样配置：

```shell
SQLALCHEMY_BINDS='{
    "": "postgresql+psycopg://scott:tiger@localhost/mydatabase",
    "nonebot_plugin_user": {
        "url": "sqlite+aiosqlite://",
        "echo": true
    }
}'
```

### sqlalchemy_echo

开启 [Echo 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo) 和 [Echo Pool 选项](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo_pool) 便于 debug。

```shell
SQLALCHEMY_ECHO=true
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

:::danger 警告
以上配置有覆盖关系，遵循特殊优先于一般的原则，具体为 [`sqlalchemy_database_url`](#sqlalchemy_database_url) > [`sqlalchemy_bind`](#sqlalchemy_bind) > [`sqlalchemy_echo`](#sqlalchemy_echo) > [`sqlalchemy_engine_options`](#sqlalchemy_engine_options)。
但覆盖顺序并非显而易见，出于清晰考虑，请只配置必要的选项。
:::
