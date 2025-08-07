from nonebot.adapters import Bot

type AliasedBot = Bot


async def get_aliased_bot(b: AliasedBot) -> Bot:
    return b
