import nonebot
from nonebot.adapters import Bot

driver = nonebot.get_driver()


@driver.on_bot_connect
async def connect(bot: Bot) -> None:
    print("Connect", bot)


@driver.on_bot_disconnect
async def disconnect(bot: Bot) -> None:
    print("Disconnect", bot)
