from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import Received, LastReceived


async def matcher(m: Matcher) -> Matcher:
    return m


async def receive(e: Event = Received("test")) -> Event:
    return e


async def last_receive(e: Event = LastReceived()) -> Event:
    return e
