"""
计划任务
========

计划任务使用第三方库 `APScheduler`_ ，使用文档请参考 `APScheduler使用文档`_ 。

.. _APScheduler:
    https://github.com/agronholm/apscheduler
.. _APScheduler使用文档:
    https://apscheduler.readthedocs.io/en/latest/
"""

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    AsyncIOScheduler = None

if AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    """
    :类型:
      ``Optional[apscheduler.schedulers.asyncio.AsyncIOScheduler]``
    :说明:
      当可选依赖 ``APScheduler`` 未安装时，``scheduler`` 为 None

      使用 ``pip install nonebot[scheduler]`` 安装可选依赖

    :常用示例:

    .. code-block:: python

        from nonebot import scheduler

        @scheduler.scheduled_job("cron", hour="*/2", id="xxx", args=[1], kwargs={arg2: 2})
        async def run_every_2_hour(arg1, arg2):
            pass

        scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")

    """
else:
    scheduler = None
