import os

import pytest

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonebug_init",
    [
        {
            "config_from_init": "init",
            "driver": "~fastapi+~httpx+~websockets",
        },
        {"config_from_init": "init", "driver": "~fastapi+~aiohttp"},
    ],
    indirect=True,
)
async def test_init(nonebug_init):
    from nonebot import get_driver

    env = get_driver().env
    assert env == "test"

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
