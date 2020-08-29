from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

say = on_command("say", to_me())


@say.handle()
async def repeat(bot: Bot, event: Event, state: dict):
    await bot.send(message=event.message, event=event)
