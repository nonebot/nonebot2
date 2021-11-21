from nonebot.log import logger
from nonebot.dependencies import Depends
from nonebot import on_command, on_message

test = on_command("123")


def depend(state: dict):
    print("==== depends running =====")
    return state


@test.got("a", prompt="a")
@test.got("b", prompt="b")
@test.receive()
@test.got("c", prompt="c")
async def _(x: dict = Depends(depend)):
    logger.info(f"=======, {x}")


test_cache1 = on_message()
test_cache2 = on_message()


@test_cache1.handle()
@test_cache2.handle()
async def _(x: dict = Depends(depend)):
    logger.info(f"======= test, {x}")
