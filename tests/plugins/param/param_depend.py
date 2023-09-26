from dataclasses import dataclass
from typing_extensions import Annotated

from pydantic import Field

from nonebot import on_message
from nonebot.adapters import Bot
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


class FooBot(Bot):
    ...


async def sub_bot(b: FooBot) -> FooBot:
    return b


# test parameterless
@test_depends.handle(parameterless=[Depends(parameterless)])
async def depends(x: int = Depends(dependency)):
    # test dependency
    return x


@test_depends.handle()
async def depends_cache(y: int = Depends(dependency, use_cache=True)):
    # test cache
    return y


# test class dependency
async def class_depend(c: ClassDependency = Depends()):
    return c


# test annotated dependency
async def annotated_depend(x: Annotated[int, Depends(dependency)]):
    return x


# test annotated class dependency
async def annotated_class_depend(c: Annotated[ClassDependency, Depends()]):
    return c


# test dependency priority
async def annotated_prior_depend(
    x: Annotated[int, Depends(lambda: 2)] = Depends(dependency)
):
    return x


async def annotated_multi_depend(
    x: Annotated[Annotated[int, Depends(lambda: 2)], Depends(dependency)]
):
    return x


# test sub dependency type mismatch
async def sub_type_mismatch(b: FooBot = Depends(sub_bot)):
    return b


# test type validate
async def validate(x: int = Depends(lambda: "1", validate=True)):
    return x


async def validate_fail(x: int = Depends(lambda: "not_number", validate=True)):
    return x


# test FieldInfo validate
async def validate_field(x: int = Depends(lambda: "1", validate=Field(gt=0))):
    return x


async def validate_field_fail(x: int = Depends(lambda: "0", validate=Field(gt=0))):
    return x
