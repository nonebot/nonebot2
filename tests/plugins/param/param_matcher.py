from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.params import received, last_received


async def matcher(m: Matcher) -> Matcher:
    return m


async def receive_test(e: Event = received("test")) -> Event:
    return e


async def last_receive_test(e: Event = last_received()) -> Event:
    return e
