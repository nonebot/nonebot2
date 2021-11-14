from nonebot import on_command
from nonebot.log import logger
from nonebot.processor import Depends

test = on_command("123")


def depend(state: dict):
    return state


@test.got("a", prompt="a")
@test.got("b", prompt="b")
@test.receive()
@test.got("c", prompt="c")
async def _(state: dict = Depends(depend)):
    logger.info(f"=======, {state}")
