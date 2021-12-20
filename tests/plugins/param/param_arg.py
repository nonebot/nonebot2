from nonebot.adapters import Event, Message
from nonebot.params import Arg, ArgStr, ArgEvent


async def arg(key: Message = Arg()) -> Message:
    return key


async def arg_str(key: str = ArgStr()) -> str:
    return key


async def arg_event(key: Event = ArgEvent()) -> Event:
    return key
