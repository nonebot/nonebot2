from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Depends

test_depends = on_message()

runned = []


def dependency(event: Event):
    # test cache
    runned.append(event)
    return event


@test_depends.handle()
async def depends(x: Event = Depends(dependency)):
    # test dependency
    return x


@test_depends.handle()
async def depends_cache(y: Event = Depends(dependency, use_cache=True)):
    return y
