from typing import Union

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


async def not_bot(b: Union[int, Bot]):
    ...
