from typing import Union, TypeVar

from nonebot.adapters import Bot


async def get_bot(b: Bot) -> Bot:
    return b


async def legacy_bot(bot):
    return bot


async def not_legacy_bot(bot: int):
    ...


class FooBot(Bot):
    ...


async def sub_bot(b: FooBot) -> FooBot:
    return b


class BarBot(Bot):
    ...


async def union_bot(b: Union[FooBot, BarBot]) -> Union[FooBot, BarBot]:
    return b


B = TypeVar("B", bound=Bot)


async def generic_bot(b: B) -> B:
    return b


CB = TypeVar("CB", Bot, None)


async def generic_bot_none(b: CB) -> CB:
    return b


async def not_bot(b: Union[int, Bot]):
    ...
