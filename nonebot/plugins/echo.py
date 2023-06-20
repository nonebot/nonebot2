from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="重复你说的话",
    usage="/echo [text]",
    type="application",
    homepage="https://github.com/nonebot/nonebot2/blob/master/nonebot/plugins/echo.py",
    config=None,
    supported_adapters=None,
)

echo = on_command("echo", to_me())


@echo.handle()
async def handle_echo(message: Message = CommandArg()):
    await echo.send(message=message)
