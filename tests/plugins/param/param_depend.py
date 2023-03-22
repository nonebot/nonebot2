from dataclasses import dataclass
from typing_extensions import Annotated

from nonebot import on_message
from nonebot.params import Depends

test_depends = on_message()

runned = []


def dependency():
    runned.append(1)
    return 1


def parameterless():
    assert len(runned) == 0
    runned.append(1)


def gen_sync():
    yield 1


async def gen_async():
    yield 2


@dataclass
class ClassDependency:
    x: int = Depends(gen_sync)
    y: int = Depends(gen_async)


# test parameterless
@test_depends.handle(parameterless=[Depends(parameterless)])
async def depends(x: int = Depends(dependency)):
    # test dependency
    return x


@test_depends.handle()
async def depends_cache(y: int = Depends(dependency, use_cache=True)):
    # test cache
    return y


async def class_depend(c: ClassDependency = Depends()):
    return c


async def annotated_depend(x: Annotated[int, Depends(dependency)]):
    return x
