import pytest
from nonebug import App

from utils import load_plugin, make_fake_event


@pytest.mark.asyncio
async def test_depends(app: App, load_plugin):
    from nonebot.params import EventParam, DependParam

    from plugins.depends import runned, depends, test_depends

    async with app.test_dependent(
        depends, allow_types=[EventParam, DependParam]
    ) as ctx:
        event = make_fake_event()()
        ctx.pass_params(event=event)
        ctx.should_return(event)

    assert len(runned) == 1 and runned[0] == event

    runned.clear()

    async with app.test_matcher(test_depends) as ctx:
        bot = ctx.create_bot()
        event_next = make_fake_event()()
        ctx.receive_event(bot, event_next)

    assert len(runned) == 1 and runned[0] == event_next
