---
sidebar_position: 0
description: 定时执行任务
---

# 定时任务

[APScheduler](https://apscheduler.readthedocs.io/en/3.x/) (Advanced Python Scheduler) 是一个 Python 第三方库，其强大的定时任务功能被广泛应用于各个场景。在 NoneBot 中，定时任务作为一个额外功能，依赖于基于 APScheduler 开发的 [`nonebot-plugin-apscheduler`](https://github.com/nonebot/plugin-apscheduler) 插件进行支持。

## 安装插件

在使用前请先安装 `nonebot-plugin-apscheduler` 插件至项目环境中，可参考[获取商店插件](../tutorial/store.mdx#安装插件)来了解并选择安装插件的方式。如：

在**项目目录**下执行以下命令：

```bash
nb plugin install nonebot-plugin-apscheduler
```

## 使用插件

`nonebot-plugin-apscheduler` 本质上是对 [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) 进行了封装以适用于 NoneBot 开发，因此其使用方式与 APScheduler 本身并无显著区别。在此我们会简要介绍其调用方法，更多的使用方面的功能请参考[APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/userguide.html)。

### 导入调度器

由于 `nonebot_plugin_apscheduler` 作为插件，因此需要在使用前对其进行**加载**并**导入**其中的 `scheduler` 调度器来创建定时任务。使用 `require` 方法可轻松完成这一过程，可参考 [跨插件访问](../advanced/requiring.md) 一节进行了解。

```python
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
```

### 添加定时任务

在 [APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/userguide.html#adding-jobs) 中提供了以下两种直接添加任务的方式：

```python
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

# 基于装饰器的方式
@scheduler.scheduled_job("cron", hour="*/2", id="job_0", args=[1], kwargs={arg2: 2})
async def run_every_2_hour(arg1: int, arg2: int):
    pass

# 基于 add_job 方法的方式
def run_every_day(arg1: int, arg2: int):
    pass

scheduler.add_job(
    run_every_day, "interval", days=1, id="job_1", args=[1], kwargs={arg2: 2}
)
```

:::caution 注意
由于 APScheduler 的定时任务并不是**由事件响应器所触发的事件**，因此其任务函数无法同[事件处理函数](../tutorial/handler.mdx#事件处理函数)一样通过[依赖注入](../tutorial/event-data.mdx#认识依赖注入)获取上下文信息，也无法通过事件响应器对象的方法进行任何操作，因此我们需要使用[调用平台 API](../appendices/api-calling.mdx#调用平台-api)的方式来获取信息或收发消息。

相对于事件处理依赖而言，编写定时任务更像是编写普通的函数，需要我们自行获取信息以及发送信息，请**不要**将事件处理依赖的特殊语法用于定时任务！
:::

关于 APScheduler 的更多使用方法，可以参考 [APScheduler 官方文档](https://apscheduler.readthedocs.io/en/3.x/index.html) 进行了解。

### 配置项

#### apscheduler_autostart

- **类型**: `bool`
- **默认值**: `True`

是否自动启动 `scheduler` ，若不启动需要自行调用 `scheduler.start()`。

#### apscheduler_log_level

- **类型**: `int`
- **默认值**: `30`

apscheduler 输出的日志等级

- `WARNING` = `30` (默认)
- `INFO` = `20`
- `DEBUG` = `10` (只有在开启 nonebot 的 debug 模式才会显示 debug 日志)

#### apscheduler_config

- **类型**: `dict`
- **默认值**: `{ "apscheduler.timezone": "Asia/Shanghai" }`

`apscheduler` 的相关配置。参考[配置调度器](https://apscheduler.readthedocs.io/en/latest/userguide.html#scheduler-config), [配置参数](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler)

配置需要包含 `apscheduler.` 作为前缀，例如 `apscheduler.timezone`。
