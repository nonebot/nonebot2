from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.plugin import on_startswith
from nonebot.permission import SUPERUSER
from nonebot.adapters.ding import Bot as DingBot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

test_command = on_startswith("hello", to_me(), permission=SUPERUSER)


@test_command.handle()
async def test_handler(bot: CQHTTPBot):
    await test_command.finish("cqhttp hello")


@test_command.handle()
async def test_handler(bot: DingBot):
    await test_command.finish("ding hello")
