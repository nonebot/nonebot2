from typing import Any, Optional

import anyio
from nonebug import App
import pytest

from nonebot.adapters import Bot
from nonebot.exception import MockApiException


@pytest.mark.anyio
async def test_bot_call_api(app: App):
    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        ctx.should_call_api("test", {}, True)
        result = await bot.call_api("test")

    assert result is True

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        ctx.should_call_api("test", {}, exception=RuntimeError("test"))
        with pytest.raises(RuntimeError, match="test"):
            await bot.call_api("test")


@pytest.mark.anyio
async def test_bot_calling_api_hook_simple(app: App):
    runned: bool = False

    async def calling_api_hook(bot: Bot, api: str, data: dict[str, Any]):
        nonlocal runned
        runned = True

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_calling_api_hook", hooks)

        Bot.on_calling_api(calling_api_hook)

        assert hooks == {calling_api_hook}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            ctx.should_call_api("test", {}, True)
            result = await bot.call_api("test")

        assert runned is True
        assert result is True


@pytest.mark.anyio
async def test_bot_calling_api_hook_mock(app: App):
    runned: bool = False

    async def calling_api_hook(bot: Bot, api: str, data: dict[str, Any]):
        nonlocal runned
        runned = True

        raise MockApiException(False)

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_calling_api_hook", hooks)

        Bot.on_calling_api(calling_api_hook)

        assert hooks == {calling_api_hook}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            result = await bot.call_api("test")

        assert runned is True
        assert result is False


@pytest.mark.anyio
async def test_bot_calling_api_hook_multi_mock(app: App):
    runned1: bool = False
    runned2: bool = False
    event = anyio.Event()

    async def calling_api_hook1(bot: Bot, api: str, data: dict[str, Any]):
        nonlocal runned1
        runned1 = True
        event.set()

        raise MockApiException(1)

    async def calling_api_hook2(bot: Bot, api: str, data: dict[str, Any]):
        nonlocal runned2
        runned2 = True
        with anyio.fail_after(1):
            await event.wait()

        raise MockApiException(2)

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_calling_api_hook", hooks)

        Bot.on_calling_api(calling_api_hook1)
        Bot.on_calling_api(calling_api_hook2)

        assert hooks == {calling_api_hook1, calling_api_hook2}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            result = await bot.call_api("test")

        assert runned1 is True
        assert runned2 is True
        assert result == 1


@pytest.mark.anyio
async def test_bot_called_api_hook_simple(app: App):
    runned: bool = False

    async def called_api_hook(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: dict[str, Any],
        result: Any,
    ):
        nonlocal runned
        runned = True

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_called_api_hook", hooks)

        Bot.on_called_api(called_api_hook)

        assert hooks == {called_api_hook}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            ctx.should_call_api("test", {}, True)
            result = await bot.call_api("test")

        assert runned is True
        assert result is True


@pytest.mark.anyio
async def test_bot_called_api_hook_mock(app: App):
    runned: bool = False

    async def called_api_hook(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: dict[str, Any],
        result: Any,
    ):
        nonlocal runned
        runned = True

        raise MockApiException(False)

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_called_api_hook", hooks)

        Bot.on_called_api(called_api_hook)

        assert hooks == {called_api_hook}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            ctx.should_call_api("test", {}, True)
            result = await bot.call_api("test")

        assert runned is True
        assert result is False

        runned = False

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            ctx.should_call_api("test", {}, exception=RuntimeError("test"))
            result = await bot.call_api("test")

        assert runned is True
        assert result is False


@pytest.mark.anyio
async def test_bot_called_api_hook_multi_mock(app: App):
    runned1: bool = False
    runned2: bool = False
    event = anyio.Event()

    async def called_api_hook1(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: dict[str, Any],
        result: Any,
    ):
        nonlocal runned1
        runned1 = True
        event.set()

        raise MockApiException(1)

    async def called_api_hook2(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: dict[str, Any],
        result: Any,
    ):
        nonlocal runned2
        runned2 = True
        with anyio.fail_after(1):
            await event.wait()

        raise MockApiException(2)

    hooks = set()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(Bot, "_called_api_hook", hooks)

        Bot.on_called_api(called_api_hook1)
        Bot.on_called_api(called_api_hook2)

        assert hooks == {called_api_hook1, called_api_hook2}

        async with app.test_api() as ctx:
            bot = ctx.create_bot()
            ctx.should_call_api("test", {}, True)
            result = await bot.call_api("test")

        assert runned1 is True
        assert runned2 is True
        assert result == 1
