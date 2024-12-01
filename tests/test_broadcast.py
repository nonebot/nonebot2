import sys
from typing import Optional

from nonebug import App
import pytest

from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.log import default_filter, default_format, logger
from nonebot.matcher import Matcher
import nonebot.message as message
from nonebot.message import (
    event_postprocessor,
    event_preprocessor,
    run_postprocessor,
    run_preprocessor,
)
from nonebot.params import Depends
from nonebot.typing import T_State
from utils import make_fake_event


async def _dependency() -> int:
    return 1


@pytest.mark.anyio
async def test_event_preprocessor(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_event_preprocessors", set())

        runned = False

        @event_preprocessor
        async def test_preprocessor(
            bot: Bot,
            event: Event,
            state: T_State,
            sub: int = Depends(_dependency),
            default: int = 1,
        ):
            nonlocal runned
            runned = True

        assert test_preprocessor in {
            dependent.call for dependent in message._event_preprocessors
        }

        with app.provider.context({}):
            matcher = on_message()

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)

        assert runned, "event_preprocessor should runned"


@pytest.mark.anyio
async def test_event_preprocessor_ignore(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_event_preprocessors", set())

        @event_preprocessor
        async def test_preprocessor():
            raise IgnoredException("pass")

        assert test_preprocessor in {
            dependent.call for dependent in message._event_preprocessors
        }

        runned = False

        async def handler():
            nonlocal runned
            runned = True

        with app.provider.context({}):
            matcher = on_message(handlers=[handler])

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)

        assert not runned, "matcher should not runned"


@pytest.mark.anyio
async def test_event_preprocessor_exception(
    app: App, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    with monkeypatch.context() as m:
        m.setattr(message, "_event_preprocessors", set())

        @event_preprocessor
        async def test_preprocessor():
            raise RuntimeError("test")

        assert test_preprocessor in {
            dependent.call for dependent in message._event_preprocessors
        }

        runned = False

        async def handler():
            nonlocal runned
            runned = True

        handler_id = logger.add(
            sys.stdout,
            level=0,
            diagnose=False,
            filter=default_filter,
            format=default_format,
        )

        try:
            with app.provider.context({}):
                matcher = on_message(handlers=[handler])

                async with app.test_matcher(matcher) as ctx:
                    bot = ctx.create_bot()
                    event = make_fake_event()()
                    ctx.receive_event(bot, event)
        finally:
            logger.remove(handler_id)

        assert not runned, "matcher should not runned"
        assert "RuntimeError: test" in capsys.readouterr().out


@pytest.mark.anyio
async def test_event_postprocessor(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_event_postprocessors", set())

        runned = False

        @event_postprocessor
        async def test_postprocessor(
            bot: Bot,
            event: Event,
            state: T_State,
            sub: int = Depends(_dependency),
            default: int = 1,
        ):
            nonlocal runned
            runned = True

        assert test_postprocessor in {
            dependent.call for dependent in message._event_postprocessors
        }

        with app.provider.context({}):
            matcher = on_message()

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)

        assert runned, "event_postprocessor should runned"


@pytest.mark.anyio
async def test_event_postprocessor_exception(
    app: App, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    with monkeypatch.context() as m:
        m.setattr(message, "_event_postprocessors", set())

        @event_postprocessor
        async def test_postprocessor():
            raise RuntimeError("test")

        assert test_postprocessor in {
            dependent.call for dependent in message._event_postprocessors
        }

        handler_id = logger.add(
            sys.stdout,
            level=0,
            diagnose=False,
            filter=default_filter,
            format=default_format,
        )

        try:
            with app.provider.context({}):
                matcher = on_message()

                async with app.test_matcher(matcher) as ctx:
                    bot = ctx.create_bot()
                    event = make_fake_event()()
                    ctx.receive_event(bot, event)
        finally:
            logger.remove(handler_id)

        assert "RuntimeError: test" in capsys.readouterr().out


@pytest.mark.anyio
async def test_run_preprocessor(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_run_preprocessors", set())

        runned = False

        @run_preprocessor
        async def test_preprocessor(
            bot: Bot,
            event: Event,
            state: T_State,
            matcher: Matcher,
            sub: int = Depends(_dependency),
            default: int = 1,
        ):
            nonlocal runned
            runned = True

            await matcher.send("test")

        assert test_preprocessor in {
            dependent.call for dependent in message._run_preprocessors
        }

        with app.provider.context({}):
            matcher = on_message()

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)
                ctx.should_call_send(event, "test", True, bot=bot)

        assert runned, "run_preprocessor should runned"


@pytest.mark.anyio
async def test_run_preprocessor_ignore(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_run_preprocessors", set())

        @run_preprocessor
        async def test_preprocessor():
            raise IgnoredException("pass")

        assert test_preprocessor in {
            dependent.call for dependent in message._run_preprocessors
        }

        runned = False

        async def handler():
            nonlocal runned
            runned = True

        with app.provider.context({}):
            matcher = on_message(handlers=[handler])

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)

        assert not runned, "matcher should not runned"


@pytest.mark.anyio
async def test_run_preprocessor_exception(
    app: App, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    with monkeypatch.context() as m:
        m.setattr(message, "_run_preprocessors", set())

        @run_preprocessor
        async def test_preprocessor():
            raise RuntimeError("test")

        assert test_preprocessor in {
            dependent.call for dependent in message._run_preprocessors
        }

        runned = False

        async def handler():
            nonlocal runned
            runned = True

        handler_id = logger.add(
            sys.stdout,
            level=0,
            diagnose=False,
            filter=default_filter,
            format=default_format,
        )

        try:
            with app.provider.context({}):
                matcher = on_message(handlers=[handler])

                async with app.test_matcher(matcher) as ctx:
                    bot = ctx.create_bot()
                    event = make_fake_event()()
                    ctx.receive_event(bot, event)
        finally:
            logger.remove(handler_id)

        assert not runned, "matcher should not runned"
        assert "RuntimeError: test" in capsys.readouterr().out


@pytest.mark.anyio
async def test_run_postprocessor(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(message, "_run_postprocessors", set())

        runned = False

        @run_postprocessor
        async def test_postprocessor(
            bot: Bot,
            event: Event,
            state: T_State,
            matcher: Matcher,
            exception: Optional[Exception],
            sub: int = Depends(_dependency),
            default: int = 1,
        ):
            nonlocal runned
            runned = True

            await matcher.send("test")

        assert test_postprocessor in {
            dependent.call for dependent in message._run_postprocessors
        }

        with app.provider.context({}):
            matcher = on_message()

            async with app.test_matcher(matcher) as ctx:
                bot = ctx.create_bot()
                event = make_fake_event()()
                ctx.receive_event(bot, event)
                ctx.should_call_send(event, "test", True, bot=bot)

        assert runned, "run_postprocessor should runned"


@pytest.mark.anyio
async def test_run_postprocessor_exception(
    app: App, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    with monkeypatch.context() as m:
        m.setattr(message, "_run_postprocessors", set())

        @run_postprocessor
        async def test_postprocessor():
            raise RuntimeError("test")

        assert test_postprocessor in {
            dependent.call for dependent in message._run_postprocessors
        }

        handler_id = logger.add(
            sys.stdout,
            level=0,
            diagnose=False,
            filter=default_filter,
            format=default_format,
        )

        try:
            with app.provider.context({}):
                matcher = on_message()

                async with app.test_matcher(matcher) as ctx:
                    bot = ctx.create_bot()
                    event = make_fake_event()()
                    ctx.receive_event(bot, event)
        finally:
            logger.remove(handler_id)

        assert "RuntimeError: test" in capsys.readouterr().out
