from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Depends

test = on_message()
test2 = on_message()

runned = False


def dependency(event: Event):
    # test cache
    global runned
    assert not runned
    runned = True
    return event


@test.handle()
@test2.handle()
async def handle(x: Event = Depends(dependency, use_cache=True)):
    # test dependency
    return x
