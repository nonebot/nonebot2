from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.plugin import on_command
from nonebot.params import EventMessage

echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(message: Message = EventMessage()):
    await echo.send(message=message)
