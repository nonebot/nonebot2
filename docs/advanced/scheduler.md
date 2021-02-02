# 定时任务

[`APScheduler`](https://apscheduler.readthedocs.io/en/latest/index.html) —— Advanced Python Scheduler

> Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically. You can add new jobs or remove old ones on the fly as you please. If you store your jobs in a database, they will also survive scheduler restarts and maintain their state. When the scheduler is restarted, it will then run all the jobs it should have run while it was offline.

## 从 NoneBot v1 迁移

`APScheduler` 作为 `nonebot` v1 的可选依赖，为众多 bot 提供了方便的定时任务功能。`nonebot2` 已将 `APScheduler` 独立为 `nonebot_plugin_apscheduler` 插件，你可以在 [插件广场](https://v2.nonebot.dev/plugin-store.html) 中找到它。

相比于 `nonebot` v1 ，只需要安装插件并修改 `scheduler` 的导入方式即可完成迁移。

## 安装插件

### 通过 nb-cli

如正在使用 `nb-cli` 构建项目，你可以从插件市场复制安装命令或手动输入以下命令以添加 `nonebot_plugin_apscheduler`。

```bash
nb plugin install nonebot_plugin_apscheduler
```

:::tip 提示
`nb-cli` 默认通过 `pypi` 安装，你可以添加命令参数 `-i [mirror]` 或 `--index [mirror]` 使用镜像源安装。
:::

### 通过 poetry

执行以下命令以添加 `nonebot_plugin_apscheduler`

```bash
poetry add nonebot-plugin-apscheduler
```

:::tip 提示
由于稍后我们将使用 `nonebot.require()` 方法进行导入，所以无需额外的 `nonebot.load_plugin()`
:::

## 快速上手

1. 在需要设置定时任务的插件中，通过 `nonebot.require` 从 `nonebot_plugin_apscheduler` 导入 `scheduler` 对象

2. 在该对象的基础上，根据 `APScheduler` 的使用方法进一步配置定时任务

将上述步骤归纳为最小实现的代码如下：

```python
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', hour='*/2', id='xxx', args=[1], kwargs={arg2: 2})
async def run_every_2_hour(arg1, arg2):
    pass

scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")
```

## 分步进行

### 导入 scheduler 对象

为了使插件能够实现定时任务，需要先将 `scheduler` 对象导入插件。

`nonebot2` 提供了 `nonebot.require` 方法来实现导入其他插件的内容，此处我们使用这个方法来导入 `scheduler` 对象。

`nonebot` 使用的 `scheduler` 对象为 `AsyncScheduler` 。

> 使用该方法传入的插件本身也需要有对应实现，关于该方法的更多介绍可以参阅 [这里](./export-and-require.md)

```python
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler
```

### 编写定时任务

由于本部分为标准的通过 `APScheduler` 配置定时任务，有关指南请参阅 [APScheduler 官方文档](https://apscheduler.readthedocs.io/en/latest/userguide.html#adding-jobs)。

### 配置插件选项

根据项目的 `.env` 文件设置，向 `.env.*` 或 `bot.py` 文件添加 `nonebot_plugin_apscheduler` 的可选配置项

:::warning 注意
`.env.*` 文件的编写应遵循 nonebot2 对 `.env.*` 文件的编写要求
:::

#### `apscheduler_autostart`

类型：`bool`

默认值：`True`

是否自动启动 `APScheduler`。

对于大多数情况，我们需要在 `nonebot2` 项目被启动时启动定时任务，则此处设为 `true`

### 在 `.env` 中添加

```bash
APSCHEDULER_AUTOSTART=true
```

### 在 `bot.py` 中添加

```python
nonebot.init(apscheduler_autostart=True)
```

#### `apscheduler_config`

类型：`dict`

默认值：`{"apscheduler.timezone": "Asia/Shanghai"}`

`APScheduler` 相关配置。修改/增加其中配置项需要确保 `prefix: apscheduler`。

对于 `APScheduler` 的相关配置，请参阅 [scheduler-config](https://apscheduler.readthedocs.io/en/latest/userguide.html#scheduler-config) 和 [BaseScheduler](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler)

> 官方文档在绝大多数时候能提供最准确和最具时效性的指南

### 在 `.env` 中添加

```bash
APSCHEDULER_CONFIG={"apscheduler.timezone": "Asia/Shanghai"}
```

### 在 `bot.py` 中添加

```python
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
```
