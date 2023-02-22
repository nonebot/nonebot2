import pytest
from nonebug import App

from nonebot.permission import User
from nonebot.message import _check_matcher
from nonebot.matcher import Matcher, matchers
from utils import make_fake_event, make_fake_message


@pytest.mark.asyncio
async def test_matcher(app: App):
    from plugins.matcher.matcher_process import (
        test_got,
        test_handle,
        test_preset,
        test_combine,
        test_receive,
        test_overload,
    )

    message = make_fake_message()("text")
    event = make_fake_event(_message=message)()
    message_next = make_fake_message()("text_next")
    event_next = make_fake_event(_message=message_next)()

    assert len(test_handle.handlers) == 1
    async with app.test_matcher(test_handle) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "send", "result", at_sender=True)
        ctx.should_finished()

    assert len(test_got.handlers) == 1
    async with app.test_matcher(test_got) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "prompt key1", "result1")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "prompt key2", "result2")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "reject", "result3", at_sender=True)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)

    assert len(test_receive.handlers) == 1
    async with app.test_matcher(test_receive) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "pause", "result", at_sender=True)
        ctx.should_paused()

    assert len(test_receive.handlers) == 1
    async with app.test_matcher(test_combine) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)

    assert len(test_preset.handlers) == 2
    async with app.test_matcher(test_preset) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)

    assert len(test_overload.handlers) == 2
    async with app.test_matcher(test_overload) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_type_updater(app: App):
    from plugins.matcher.matcher_type import test_type_updater, test_custom_updater

    event = make_fake_event()()

    assert test_type_updater.type == "test"
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_type_updater()
        new_type = await matcher.update_type(bot, event)
        assert new_type == "message"

    assert test_custom_updater.type == "test"
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_custom_updater()
        new_type = await matcher.update_type(bot, event)
        assert new_type == "custom"


@pytest.mark.asyncio
async def test_permission_updater(app: App):
    from plugins.matcher.matcher_permission import (
        default_permission,
        test_custom_updater,
        test_permission_updater,
        test_user_permission_updater,
    )

    event = make_fake_event(_session_id="test")()

    assert test_permission_updater.permission is default_permission
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_permission_updater()
        new_perm = await matcher.update_permission(bot, event)
        assert len(new_perm.checkers) == 1
        checker = list(new_perm.checkers)[0].call
        assert isinstance(checker, User)
        assert checker.users == ("test",)
        assert checker.perm is default_permission

    user_permission = list(test_user_permission_updater.permission.checkers)[0].call
    assert isinstance(user_permission, User)
    assert user_permission.perm is default_permission
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_user_permission_updater()
        new_perm = await matcher.update_permission(bot, event)
        assert len(new_perm.checkers) == 1
        checker = list(new_perm.checkers)[0].call
        assert isinstance(checker, User)
        assert checker.users == ("test",)
        assert checker.perm is default_permission

    assert test_custom_updater.permission is default_permission
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_custom_updater()
        new_perm = await matcher.update_permission(bot, event)
        assert new_perm is default_permission


@pytest.mark.asyncio
async def test_run(app: App):
    with app.provider.context({}):
        assert not matchers
        event = make_fake_event()()

        async def reject():
            await Matcher.reject()

        test_reject = Matcher.new(handlers=[reject])

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            await test_reject().run(bot, event, {})
            assert len(matchers[0]) == 1
            assert len(matchers[0][0].handlers) == 1

        del matchers[0]

        async def pause():
            await Matcher.pause()

        test_pause = Matcher.new(handlers=[pause])

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            await test_pause().run(bot, event, {})
            assert len(matchers[0]) == 1
            assert len(matchers[0][0].handlers) == 0


@pytest.mark.asyncio
async def test_expire(app: App):
    from plugins.matcher.matcher_expire import (
        test_temp_matcher,
        test_datetime_matcher,
        test_timedelta_matcher,
    )

    event = make_fake_event(_type="test")()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_temp_matcher in matchers[test_temp_matcher.priority]
        await _check_matcher(test_temp_matcher, bot, event, {})
        assert test_temp_matcher not in matchers[test_temp_matcher.priority]

    event = make_fake_event()()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_datetime_matcher in matchers[test_datetime_matcher.priority]
        await _check_matcher(test_datetime_matcher, bot, event, {})
        assert test_datetime_matcher not in matchers[test_datetime_matcher.priority]

    event = make_fake_event()()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_timedelta_matcher in matchers[test_timedelta_matcher.priority]
        await _check_matcher(test_timedelta_matcher, bot, event, {})
        assert test_timedelta_matcher not in matchers[test_timedelta_matcher.priority]
