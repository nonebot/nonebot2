from typing import Any, Dict, Optional

import pytest
from nonebug import App

from nonebot.adapters import Bot
from nonebot.exception import MockApiException


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_bot_calling_api_hook_simple(app: App):
    runned: bool = False

    async def calling_api_hook(bot: Bot, api: str, data: Dict[str, Any]):
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


@pytest.mark.asyncio
async def test_bot_calling_api_hook_mock(app: App):
    runned: bool = False

    async def calling_api_hook(bot: Bot, api: str, data: Dict[str, Any]):
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


@pytest.mark.asyncio
async def test_bot_called_api_hook_simple(app: App):
    runned: bool = False

    async def called_api_hook(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: Dict[str, Any],
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


@pytest.mark.asyncio
async def test_bot_called_api_hook_mock(app: App):
    runned: bool = False

    async def called_api_hook(
        bot: Bot,
        exception: Optional[Exception],
        api: str,
        data: Dict[str, Any],
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
