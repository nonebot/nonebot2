from nonebot.adapters import Bot


async def get_bot(b: Bot) -> Bot:
    return b


class SubBot(Bot):
    ...


async def sub_bot(b: SubBot) -> SubBot:
    return b
