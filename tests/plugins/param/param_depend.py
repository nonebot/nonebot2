from dataclasses import dataclass

from nonebot import on_message
from nonebot.params import depends

test_depends = on_message()

runned = []


@depends
def dependency():
    runned.append(1)
    return 1


@depends
def parameterless():
    assert len(runned) == 0
    runned.append(1)


@depends
def gen_sync():
    yield 1


@depends
async def gen_async():
    yield 2


@dataclass
class ClassDependency:
    x: int = gen_sync
    y: int = gen_async


# test parameterless
@test_depends.handle(parameterless=[parameterless])
async def depends_test(x: int = dependency):
    # test dependency
    return x


@test_depends.handle()
async def depends_cache(y: int = dependency(use_cache=True)):
    # test cache
    return y


async def class_depend(c: ClassDependency = depends()):
    return c
