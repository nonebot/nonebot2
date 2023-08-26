import pytest
from nonebug import App

import nonebot
from nonebot.drivers import Driver, ASGIMixin, ReverseDriver
from nonebot import (
    get_app,
    get_bot,
    get_asgi,
    get_bots,
    get_driver,
    get_adapter,
    get_adapters,
)


@pytest.mark.asyncio
async def test_init():
    env = nonebot.get_driver().env
    assert env == "test"

    config = nonebot.get_driver().config
    assert config.nickname == {"test"}
    assert config.superusers == {"test", "fake:faketest"}
    assert config.api_timeout is None

    assert config.simple_none is None
    assert config.config_from_env == {"test": "test"}
    assert config.config_override == "new"
    assert config.config_from_init == "init"
    assert config.common_config == "common"
    assert config.common_override == "new"
    assert config.nested_dict == {"a": 1, "b": 2, "c": {"d": 3}}
    assert config.nested_missing_dict == {"a": 1, "b": {"c": 2}}
    assert config.not_nested == "some string"


@pytest.mark.asyncio
async def test_get_driver(app: App, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(nonebot, "_driver", None)
        with pytest.raises(ValueError, match="initialized"):
            get_driver()


@pytest.mark.asyncio
async def test_get_asgi(app: App, monkeypatch: pytest.MonkeyPatch):
    driver = get_driver()
    assert isinstance(driver, ReverseDriver)
    assert isinstance(driver, ASGIMixin)
    assert get_asgi() == driver.asgi


@pytest.mark.asyncio
async def test_get_app(app: App, monkeypatch: pytest.MonkeyPatch):
    driver = get_driver()
    assert isinstance(driver, ReverseDriver)
    assert isinstance(driver, ASGIMixin)
    assert get_app() == driver.server_app


@pytest.mark.asyncio
async def test_get_adapter(app: App, monkeypatch: pytest.MonkeyPatch):
    async with app.test_api() as ctx:
        adapter = ctx.create_adapter()
        adapter_name = adapter.get_name()

        with monkeypatch.context() as m:
            m.setattr(Driver, "_adapters", {adapter_name: adapter})
            assert get_adapters() == {adapter_name: adapter}
            assert get_adapter(adapter_name) is adapter
            assert get_adapter(adapter.__class__) is adapter
            with pytest.raises(ValueError, match="registered"):
                get_adapter("not exist")


@pytest.mark.asyncio
async def test_run(app: App, monkeypatch: pytest.MonkeyPatch):
    runned = False

    def mock_run(*args, **kwargs):
        nonlocal runned
        runned = True
        assert args == ("arg",)
        assert kwargs == {"kwarg": "kwarg"}

    driver = get_driver()

    with monkeypatch.context() as m:
        m.setattr(driver, "run", mock_run)
        nonebot.run("arg", kwarg="kwarg")

    assert runned


@pytest.mark.asyncio
async def test_get_bot(app: App, monkeypatch: pytest.MonkeyPatch):
    driver = get_driver()

    with pytest.raises(ValueError, match="no bots"):
        get_bot()

    with monkeypatch.context() as m:
        m.setattr(driver, "_bots", {"test": "test"})
        assert get_bot() == "test"
        assert get_bot("test") == "test"
        assert get_bots() == {"test": "test"}
