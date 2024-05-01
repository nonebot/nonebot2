import TabItem from "@theme/TabItem";
import Tabs from "@theme/Tabs";

# 数据库

[`nonebot-plugin-orm`](https://github.com/nonebot/plugin-orm) 是 NoneBot 的数据库支持插件。
本插件基于 [SQLAlchemy](https://www.sqlalchemy.org/) 和 [Alembic](https://alembic.sqlalchemy.org/)，提供了许多与 NoneBot 紧密集成的功能：

- 多 Engine / Connection 支持
- Session 管理
- 关系模型管理、依赖注入支持
- 数据库迁移

## 安装

<Tabs groupId="install">
<TabItem value="cli" label="使用 nb-cli">

```shell
nb plugin install nonebot-plugin-orm
```

</TabItem>
<TabItem value="pip" label="使用 pip">

```shell
pip install nonebot-plugin-orm
```

</TabItem>

<TabItem value="pdm" label="使用 pdm">

```shell
pdm add nonebot-plugin-orm
```

</TabItem>
</Tabs>

## 数据库驱动和后端

本插件只提供了 ORM 功能，没有数据库后端，也没有直接连接数据库后端的能力。
所以你需要另行安装数据库驱动和数据库后端，并且配置数据库连接信息。

### SQLite

[SQLite](https://www.sqlite.org/) 是一个轻量级的嵌入式数据库，它的数据以单文件的形式存储在本地，不需要单独的数据库后端。
SQLite 非常适合用于开发环境和小型应用，但是不适合用于大型应用的生产环境。

虽然不需要另行安装数据库后端，但你仍然需要安装数据库驱动：

<Tabs groupId="install">
<TabItem value="pip" label="使用 pip">

```shell
pip install "nonebot-plugin-orm[sqlite]"
```

</TabItem>

<TabItem value="pdm" label="使用 pdm">

```shell
pdm add "nonebot-plugin-orm[sqlite]"
```

</TabItem>
</Tabs>

默认情况下，数据库文件为 `<data path>/nonebot-plugin-orm/db.sqlite3`（数据目录由 [nonebot-plugin-localstore](../data-storing) 提供）。
或者，你可以通过配置 `SQLALCHEMY_DATABASE_URL` 来指定数据库文件路径：

```shell
SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:///file_path
```

### PostgreSQL

[PostgreSQL](https://www.postgresql.org/) 是世界上最先进的开源关系数据库之一，对各种高级且广泛应用的功能有最好的支持，是中小型应用的首选数据库。

<Tabs groupId="install">
<TabItem value="pip" label="使用 pip">

```shell
pip install nonebot-plugin-orm[postgresql]
```

</TabItem>

<TabItem value="pdm" label="使用 pdm">

```shell
pdm add nonebot-plugin-orm[postgresql]
```

</TabItem>
</Tabs>

```shell
SQLALCHEMY_DATABASE_URL=postgresql+psycopg://user:password@host:port/dbname[?key=value&key=value...]
```

### MySQL / MariaDB

[MySQL](https://www.mysql.com/) 和 [MariaDB](https://mariadb.com/) 是经典的开源关系数据库，适合用于中小型应用。

<Tabs groupId="install">
<TabItem value="pip" label="使用 pip">

```shell
pip install nonebot-plugin-orm[mysql]
```

</TabItem>

<TabItem value="pdm" label="使用 pdm">

```shell
pdm add nonebot-plugin-orm[mysql]
```

</TabItem>
</Tabs>

```shell
SQLALCHEMY_DATABASE_URL=mysql+aiomysql://user:password@host:port/dbname[?key=value&key=value...]
```

## 使用

本插件提供了数据库迁移功能（此功能依赖于 [nb-cli 脚手架](../../quick-start#安装脚手架)）。
在安装了新的插件或机器人之后，你需要执行一次数据库迁移操作，将数据库同步至与机器人一致的状态：

```shell
nb orm upgrade
```

运行完毕后，可以检查一下：

```shell
nb orm check
```

如果输出是 `没有检测到新的升级操作`，那么恭喜你，数据库已经迁移完成了，你可以启动机器人了。
