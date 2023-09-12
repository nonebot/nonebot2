import sys
from pathlib import Path

import pytest
from nonebug import App

from nonebot.rule import Rule
from nonebot import get_plugin
from nonebot.matcher import Matcher, matchers
from utils import FakeMessage, make_fake_event
from nonebot.permission import User, Permission
from nonebot.message import _check_matcher, check_and_run_matcher


@pytest.mark.asyncio
async def test_matcher_info(app: App):
    from plugins.matcher.matcher_info import matcher

    assert issubclass(matcher, Matcher)
    assert matcher.type == "message"
    assert matcher.priority == 1
    assert matcher.temp is False
    assert matcher.expire_time is None
    assert matcher.block is True

    assert matcher._source

    assert matcher._source.module_name == "plugins.matcher.matcher_info"
    assert matcher.module is sys.modules["plugins.matcher.matcher_info"]
    assert matcher.module_name == "plugins.matcher.matcher_info"

    assert matcher._source.plugin_name == "matcher_info"
    assert matcher.plugin is get_plugin("matcher_info")
    assert matcher.plugin_name == "matcher_info"

    assert (
        matcher._source.file
        == (Path(__file__).parent.parent / "plugins/matcher/matcher_info.py").absolute()
    )

    assert matcher._source.lineno == 3


@pytest.mark.asyncio
async def test_matcher_check(app: App):
    async def falsy():
        return False

    async def truthy():
        return True

    async def error():
        raise RuntimeError

    event = make_fake_event(_type="test")()
    with app.provider.context({}):
        test_perm_falsy = Matcher.new(permission=Permission(falsy))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_perm_falsy, bot, event, {}) is False

        test_perm_truthy = Matcher.new(permission=Permission(truthy))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_perm_truthy, bot, event, {}) is True

        test_perm_error = Matcher.new(permission=Permission(error))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_perm_error, bot, event, {}) is False

        test_rule_falsy = Matcher.new(rule=Rule(falsy))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_rule_falsy, bot, event, {}) is False

        test_rule_truthy = Matcher.new(rule=Rule(truthy))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_rule_truthy, bot, event, {}) is True

        test_rule_error = Matcher.new(rule=Rule(error))
        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            assert await _check_matcher(test_rule_error, bot, event, {}) is False


@pytest.mark.asyncio
async def test_matcher_handle(app: App):
    from plugins.matcher.matcher_process import test_handle

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()

    assert len(test_handle.handlers) == 1
    async with app.test_matcher(test_handle) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "send", "result", at_sender=True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_matcher_got(app: App):
    from plugins.matcher.matcher_process import test_got

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()
    message_next = FakeMessage("text_next")
    event_next = make_fake_event(_message=message_next)()

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


@pytest.mark.asyncio
async def test_matcher_receive(app: App):
    from plugins.matcher.matcher_process import test_receive

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()

    assert len(test_receive.handlers) == 1
    async with app.test_matcher(test_receive) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "pause", "result", at_sender=True)
        ctx.should_paused()


@pytest.mark.asyncio
async def test_matcher_combine(app: App):
    from plugins.matcher.matcher_process import test_combine

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()
    message_next = FakeMessage("text_next")
    event_next = make_fake_event(_message=message_next)()

    assert len(test_combine.handlers) == 1
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


@pytest.mark.asyncio
async def test_matcher_preset(app: App):
    from plugins.matcher.matcher_process import test_preset

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()
    message_next = FakeMessage("text_next")
    event_next = make_fake_event(_message=message_next)()

    assert len(test_preset.handlers) == 2
    async with app.test_matcher(test_preset) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.receive_event(bot, event)
        ctx.should_rejected()
        ctx.receive_event(bot, event_next)


@pytest.mark.asyncio
async def test_matcher_overload(app: App):
    from plugins.matcher.matcher_process import test_overload

    message = FakeMessage("text")
    event = make_fake_event(_message=message)()

    assert len(test_overload.handlers) == 2
    async with app.test_matcher(test_overload) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, event)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_matcher_destroy(app: App):
    from plugins.matcher.matcher_process import test_destroy

    async with app.test_matcher(test_destroy):
        assert len(matchers) == 1
        assert len(matchers[test_destroy.priority]) == 1
        assert matchers[test_destroy.priority][0] is test_destroy

        test_destroy.destroy()

        assert len(matchers[test_destroy.priority]) == 0


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
async def test_default_permission_updater(app: App):
    from plugins.matcher.matcher_permission import (
        default_permission,
        test_permission_updater,
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


@pytest.mark.asyncio
async def test_user_permission_updater(app: App):
    from plugins.matcher.matcher_permission import (
        default_permission,
        test_user_permission_updater,
    )

    event = make_fake_event(_session_id="test")()
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


@pytest.mark.asyncio
async def test_custom_permission_updater(app: App):
    from plugins.matcher.matcher_permission import (
        new_permission,
        default_permission,
        test_custom_updater,
    )

    event = make_fake_event(_session_id="test")()
    assert test_custom_updater.permission is default_permission
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        matcher = test_custom_updater()
        new_perm = await matcher.update_permission(bot, event)
        assert new_perm is new_permission


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
async def test_temp(app: App):
    from plugins.matcher.matcher_expire import test_temp_matcher

    event = make_fake_event(_type="test")()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_temp_matcher in matchers[test_temp_matcher.priority]
        await check_and_run_matcher(test_temp_matcher, bot, event, {})
        assert test_temp_matcher not in matchers[test_temp_matcher.priority]


@pytest.mark.asyncio
async def test_datetime_expire(app: App):
    from plugins.matcher.matcher_expire import test_datetime_matcher

    event = make_fake_event()()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_datetime_matcher in matchers[test_datetime_matcher.priority]
        await check_and_run_matcher(test_datetime_matcher, bot, event, {})
        assert test_datetime_matcher not in matchers[test_datetime_matcher.priority]


@pytest.mark.asyncio
async def test_timedelta_expire(app: App):
    from plugins.matcher.matcher_expire import test_timedelta_matcher

    event = make_fake_event()()
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert test_timedelta_matcher in matchers[test_timedelta_matcher.priority]
        await check_and_run_matcher(test_timedelta_matcher, bot, event, {})
        assert test_timedelta_matcher not in matchers[test_timedelta_matcher.priority]
