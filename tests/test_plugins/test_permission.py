from nonebot.rule import to_me
from nonebot.typing import State
from nonebot.plugin import on_startswith
from nonebot.permission import GROUP_ADMIN
from nonebot.adapters.ding import Bot as DingBot, Event as DingEvent
from nonebot.adapters.cqhttp import Bot as CQHTTPBot, Event as CQHTTPEvent

test_command = on_startswith("hello", to_me(), permission=GROUP_ADMIN)


@test_command.handle()
async def test_handler(bot: CQHTTPBot, event: CQHTTPEvent, state: State):
    await test_command.finish("cqhttp hello")


@test_command.handle()
async def test_handler(bot: DingBot, event: DingEvent, state: State):
    await test_command.finish("ding hello")
