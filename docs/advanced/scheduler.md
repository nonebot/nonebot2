# 定时任务

本文撰写完成之时，`nonebot2` 已将 `APScheduler` 独立为 `nonebot_plugin_apscheduler` 插件，您可以在 [插件广场](https://v2.nonebot.dev/plugin-store.html) 中找到。

本文将以 `nonebot_plugin_apscheduler` 的 `README.md` 为基础，对 `nonebot2` 的定时任务实现提供指南。

我们推荐通过 [插件广场](https://v2.nonebot.dev/plugin-store.html) 的 `nonebot_plugin_apscheduler` 插件，辅以 `nonebot.require()` 方法来实现传入和进一步配置。

## 简单地说

1. 为了实现定时任务，我们需要向 `nonebot2` 项目环境添加 `nonebot_plugin_apscheduler`

1. 在需要设置定时任务的插件中，通过 `from nonebot import require` 从 `nonebot_plugin_apscheduler` 传入 `scheduler` 对象

1. 在该对象的基础上，根据 `APScheduler` 的使用方法进一步配置定时任务

排除添加依赖的部分，将上述步骤归纳为最小实现的代码如下：

```python
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', hour='*/2', id='xxx', args=[1], kwargs={arg2: 2})
async def run_every_2_hour(arg1, arg2):
    pass
```

## 分步进行

### 添加依赖 - 通过 poetry

我们推荐使用 `poetry` 实现虚拟环境和依赖管理，在 `nonebot2` 项目目录中执行以下命令以添加 `nonebot_plugin_apscheduler`

```bash
poetry add nonebot_plugin_apscheduler
```

由于稍后我们将使用 `nonebot.require()` 方法进行导入，所以无需额外的 `nonebot.load_plugin()`

### 添加依赖 - 通过 nb-cli

如正在使用 `nb-cli` 构建项目，也可以使用以下命令以添加 `nonebot_plugin_apscheduler`

```bash
nb plugin install nonebot_plugin_apscheduler
```

### 传入 scheduler 对象

为了使插件能够实现定时任务，需要先将 `scheduler` 对象传入插件

`nonebot2` 提供了 `nonebot.require()` 方法来实现 `nonebot2` 插件内容的传入，此处我们使用这个方法来传入 `scheduler` 对象

> 使用该方法传入的插件本身也需要有对应实现，关于该方法的更多介绍可以参阅 [这里](https://v2.nonebot.dev/api/plugin.html#require-name)

```python
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler
```

### 配置定时任务

由于本部分为标准的通过 `APScheduler` 配置定时任务，有关指南请参阅 [官方文档](https://apscheduler.readthedocs.io/en/latest/userguide.html#adding-jobs)

### 向 .env.* 文件添加可选配置项

:::warning 注意 .env.* 文件的编写应遵循 nonebot2 对 .env.* 文件的编写要求 :::

根据项目的 `.env` 文件设置，向 `.env.*` 文件添加 `nonebot_plugin_apscheduler` 的可选配置项

* `apscheduler_autostart` `bool` 是否自动启动 `APScheduler`

对于大多数情况，我们需要在 `nonebot2` 项目被启动时启动定时任务，则此处设为 `true`

```bash
apscheduler_autostart = true
```

* `apscheduler_config` `dict` `APScheduler` 相关配置

对于 `APScheduler` 的相关配置，请参阅 [scheduler-config](https://apscheduler.readthedocs.io/en/latest/userguide.html#scheduler-config) 和 [BaseScheduler](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler)

> 官方文档在绝大多数时候能提供最准确和最具时效性的指南

```bash
apscheduler_config = {"apscheduler.timezone": "Asia/Shanghai"}
```

`nonebot_plugin_apscheduler` 提供了时区的默认值 `Asia/Shanghai`，增加其中配置项需要确保 `prefix: apscheduler.`
