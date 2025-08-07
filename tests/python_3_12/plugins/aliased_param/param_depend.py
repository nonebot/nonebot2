from typing import Annotated

from nonebot import on_message
from nonebot.params import Depends

test_depends = on_message()

runned = []


def dependency():
    runned.append(1)
    return 1


type AliasedDepends = Annotated[int, Depends(dependency)]


@test_depends.handle()
async def aliased_depends(x: AliasedDepends):
    return x
