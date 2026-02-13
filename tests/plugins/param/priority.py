from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.params import Arg, Depends
from nonebot.typing import T_State


def dependency():
    return 1


async def complex_priority(
    sub: int = Depends(dependency),
    bot: Bot | None = None,
    event: Event | None = None,
    state: T_State = {},
    matcher: Matcher | None = None,
    arg: Message = Arg(),
    exception: Exception | None = None,
    default: int = 1,
): ...
