import os
import sys
from re import A
from typing import TYPE_CHECKING, Set

import pytest

from utils import load_plugin

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonebug_init",
    [{"config_from_init": "init", "driver": "nonebot.drivers.fastapi:FullDriver"}],
    indirect=True,
)
async def test_init(nonebug_init):
    from nonebot import get_driver
    from nonebot.drivers.fastapi import FullDriver

    env = get_driver().env
    assert env == "test"

    assert isinstance(get_driver(), FullDriver)

    config = get_driver().config
    assert config.config_from_env == {"test": "test"}
    assert config.config_from_init == "init"
    assert config.common_config == "common"


@pytest.mark.asyncio
async def test_get(monkeypatch: pytest.MonkeyPatch, nonebug_clear):
    import nonebot
    from nonebot.drivers import ForwardDriver, ReverseDriver
    from nonebot import get_app, get_bot, get_asgi, get_bots, get_driver

    try:
        get_driver()
        assert False, "Driver can only be got after initialization"
    except ValueError:
        assert True

    nonebot.init(driver="nonebot.drivers.fastapi")

    driver = get_driver()
    assert isinstance(driver, ReverseDriver)
    assert get_asgi() == driver.asgi
    assert get_app() == driver.server_app

    runned = False

    def mock_run(*args, **kwargs):
        nonlocal runned
        runned = True
        assert args == ("arg",) and kwargs == {"kwarg": "kwarg"}

    monkeypatch.setattr(driver, "run", mock_run)
    nonebot.run("arg", kwarg="kwarg")
    assert runned

    try:
        get_bot()
        assert False
    except ValueError:
        assert True

    monkeypatch.setattr(driver, "_clients", {"test": "test"})
    assert get_bot() == "test"
    assert get_bot("test") == "test"
    assert get_bots() == {"test": "test"}


@pytest.mark.asyncio
async def test_load_plugin(load_plugin: Set["Plugin"]):
    import nonebot

    assert nonebot.get_loaded_plugins() == load_plugin
    plugin = nonebot.get_plugin("depends")
    assert plugin
    assert plugin.module_name == "plugins.depends"
    assert "plugins.depends" in sys.modules
