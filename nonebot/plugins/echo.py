from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(message: Message = CommandArg()):
    await echo.send(message=message)
