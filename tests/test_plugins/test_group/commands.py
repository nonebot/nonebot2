from . import cmd
from nonebot.adapters import Bot, Event

test_1 = cmd.command("1", aliases={"test"})


@test_1.handle()
async def test1(bot: Bot, event: Event):
    await test_1.finish(event.get_message())
