from typing import Annotated

from nonebot.adapters import Message
from nonebot.params import Arg, ArgStr, ArgPlainText


async def arg(key: Message = Arg()) -> Message:
    return key


async def arg_str(key: str = ArgStr()) -> str:
    return key


async def arg_plain_text(key: str = ArgPlainText()) -> str:
    return key


async def arg_annotated(key: Annotated[Message, Arg()]) -> Message:
    return key


async def arg_str_annotated(key: Annotated[str, ArgStr()]) -> str:
    return key


async def arg_plain_text_annotated(key: Annotated[str, ArgPlainText()]) -> str:
    return key
