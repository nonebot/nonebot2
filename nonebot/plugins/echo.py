from nonebot.rule import to_me
from nonebot.adapters import Event
from nonebot.plugin import on_command

echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(event: Event):
    await echo.send(message=event.get_message())
