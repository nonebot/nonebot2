from nonebug import App
import pytest

from utils import FakeMessage, FakeMessageSegment, make_fake_event


@pytest.mark.anyio
async def test_echo(app: App):
    from nonebot.plugins.echo import echo

    async with app.test_matcher(echo) as ctx:
        bot = ctx.create_bot()

        message = FakeMessage("/echo 123")
        event = make_fake_event(_message=message)()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, FakeMessage("123"), True, bot=bot)

        message = FakeMessageSegment.text("/echo 123") + FakeMessageSegment.image(
            "test"
        )
        event = make_fake_event(_message=message)()
        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            FakeMessageSegment.text("123") + FakeMessageSegment.image("test"),
            True,
            bot=bot,
        )

        message = FakeMessage("/echo")
        event = make_fake_event(_message=message)()
        ctx.receive_event(bot, event)
