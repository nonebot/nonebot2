from typing import Annotated

from nonebot.adapters import Message
from nonebot.params import Arg

type AliasedArg = Annotated[Message, Arg()]


async def aliased_arg(key: AliasedArg) -> Message:
    return key
