from nonebot.adapters import Event, Message
from nonebot.params import Arg, ArgStr, ArgPlainText


async def arg(key: Message = Arg()) -> Message:
    return key


async def arg_str(key: str = ArgStr()) -> str:
    return key


async def arg_plain_text(key: str = ArgPlainText()) -> str:
    return key
