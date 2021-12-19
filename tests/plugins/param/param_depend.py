from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Depends

test_depends = on_message()

runned = []


def dependency():
    runned.append(1)
    return 1


def parameterless():
    assert len(runned) == 0
    runned.append(1)


# test parameterless
@test_depends.handle(parameterless=[Depends(parameterless)])
async def depends(x: int = Depends(dependency)):
    # test dependency
    return x


@test_depends.handle()
async def depends_cache(y: int = Depends(dependency, use_cache=True)):
    # test cache
    return y
