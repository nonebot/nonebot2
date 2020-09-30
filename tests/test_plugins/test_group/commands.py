from nonebot.typing import Bot, Event
from nonebot.permission import GROUP_OWNER

from . import test

test_1 = test.command("1", aliases={"test"}, permission=GROUP_OWNER)


@test_1.handle()
async def test1(bot: Bot, event: Event, state: dict):
    await test_1.finish(event.raw_message)
