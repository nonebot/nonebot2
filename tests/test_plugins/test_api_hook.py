from nonebot.adapters import Bot


@Bot.on_calling_api
async def call(bot: Bot, api: str, data: dict):
    print(type(bot), api, data)
