try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    # APScheduler is not installed
    AsyncIOScheduler = None

if AsyncIOScheduler:
    class Scheduler(AsyncIOScheduler):
        pass
else:
    Scheduler = None
