# 计划任务

nonebot 内置了 apscheduler，
通过`from nonebot import scheduler`获取，
这是一个`AsyncIOScheduler`的实例，
详细用法可见[官方文档](https://apscheduler.readthedocs.io/)。

这里列出一些常见的用法。

## 固定的计划任务

利用固定的*触发器*（trigger）来触发某些任务

### 一次性任务

`date`触发器
[完整文档](https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html#module-apscheduler.triggers.date)

固定时间触发，仅触发一次

```python
from datetime import datetime

@nonebot.scheduler.scheduled_job(
    'cron',
    run_date=datetime(2021, 1, 1, 0, 0),
    # timezone=None,
    )
async def _():
    await bot.send_group_msg(group_id=672076603,
                             message="2021，新年快乐！")
```

### 定期任务

`cron`触发器
[完整文档](https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html#module-apscheduler.triggers.cron)

从`start_date`开始，每一个固定时间触发，到`end_date`结束

比如每小时、每个工作日早上8点

```python
@nonebot.scheduler.scheduled_job(
    'cron',
    # year=None,
    # month=None,
    # day=None,
    # week=None,
    day_of_week="mon,tue,wed,thu,fri",
    hour=7,
    # minute=None,
    # second=None,
    # start_date=None,
    # end_date=None,
    # timezone=None,
    )
async def _():
    await bot.send_group_msg(group_id=672076603,
                             message="起床啦！")
```

### 间隔任务

`interval`触发器
[完整文档](https://apscheduler.readthedocs.io/en/stable/modules/triggers/interval.html#module-apscheduler.triggers.interval)

从`start_date`开始，每间隔一段时间触发，到`end_date`结束

```python
@nonebot.scheduler.scheduled_job(
    'interval',
    # weeks=0,
    # days=0,
    # hours=0,
    minutes=5,
    # seconds=0,
    # start_date=time.now(),
    # end_date=None,
    )
async def _():
    has_new_item = check_new_item()
    if has_new_item:
        await bot.send_group_msg(group_id=672076603,
                                 message="RC更新啦！")
```

## 动态的计划任务

有时，我们需要机器人在运行的过程中，添加一些计划任务，
那么我们就需要 `scheduler.add_job` 来帮忙

这里，我们以*一次性任务*为例，其他类型的任务可以用相同的方法

```python
import datetime

from apscheduler.triggers.date import DateTrigger # 一次性触发器
# from apscheduler.triggers.cron import CronTrigger # 定期触发器
# from apscheduler.triggers.interval import IntervalTrigger # 间隔触发器
from nonebot import on_command, scheduler

@on_command('赖床')
async def _(session: CommandSession):
    await session.send('我会在5分钟后再喊你')

    # 制作一个“5分钟后”触发器
    delta = datetime.timedelta(minutes=5)
    trigger = DateTrigger(
        run_date=datetime.datetime.now() + delta
    )

    # 添加任务
    scheduler.add_job(
        func=session.send, # 要添加任务的函数，不要带参数
        trigger=trigger, # 触发器
        args=('不要再赖床啦！',), # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
        # kwargs=None,
        misfire_grace_time=60, # 允许的误差时间，建议不要省略
        # jobstore='default', # 任务储存库，在下一小节中说明
    )
```

## 储存任务

有时，我们动态添加的一些计划任务需要长时间储存，
而普通储存的任务会在重启后丢失，
那么我们就需要 `jobstore` 来帮忙

apscheduler 可以将任务存储在内存中或数据库中，
默认 jobstore 将所有任务储存在内存中，关闭后即丢失。

这里，我们以 SQLite 为例，将任务添加到数据库中，

我们先创建一个数据库

```python
import asyncio
import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from nonebot import on_command, scheduler, get_bot

database_path = os.path.join(os.path.dirname(__file__), 'job_store.db')

store = SQLAlchemyJobStore(url='sqlite:///'+database_path)

scheduler.add_jobstore(store, alias='my_job_store')
```

之后，我们在添加新任务时，可以指定任务的储存库

```python
bot = get_bot()

def alarm(*args, **kwargs):
    asyncio.run(bot.send(*args, **kwargs))

@on_command('提醒收菜')
async def _(session: CommandSession):
    await session.send('我会在一天后提醒你收菜')
    delta = datetime.timedelta(days=1)
    trigger = DateTrigger(
        run_date=datetime.datetime.now() + delta
    )

    # 添加任务
    scheduler.add_job(
        func=alarm,
        trigger=trigger,
        kwargs = {
            'context': session.ctx,
            'message': '起床收菜啦！',
        },
        misfire_grace_time=60,
        jobstore='my_job_store', # 任务储存库，指定为刚才创建的储存库
    )
```

**踩坑预警：**

由于 `apscheduler` 自带的 jobstore 无法将协程任务储存进数据库，
所以必须将任务转化为同步任务再储存。
并且 `apscheduler` 中的 `AsyncIOScheduler` 在执行同步任务时，会新建一个执行器（executor），
导致这个任务里无法使用 `asyncio.get_running_loop()` 来获取事件循环，
只能使用 `asyncio.run(...)` 来运行异步函数。
