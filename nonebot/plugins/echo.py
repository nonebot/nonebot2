from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

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
    if any((not seg.is_text()) or str(seg) for seg in message):
        await echo.send(message=message)
