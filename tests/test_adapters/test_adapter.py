from typing import Optional
from contextlib import asynccontextmanager

import pytest
from nonebug import App

from utils import FakeAdapter
from nonebot.adapters import Bot
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    HTTPServerSetup,
    WebSocketServerSetup,
)


@pytest.mark.asyncio
async def test_adapter_connect(app: App, driver: Driver):
    last_connect_bot: Optional[Bot] = None
    last_disconnect_bot: Optional[Bot] = None

    def _fake_bot_connect(bot: Bot):
        nonlocal last_connect_bot
        last_connect_bot = bot

    def _fake_bot_disconnect(bot: Bot):
        nonlocal last_disconnect_bot
        last_disconnect_bot = bot

    with pytest.MonkeyPatch.context() as m:
        m.setattr(driver, "_bot_connect", _fake_bot_connect)
        m.setattr(driver, "_bot_disconnect", _fake_bot_disconnect)

        adapter = FakeAdapter(driver)

        async with app.test_api() as ctx:
            bot = ctx.create_bot(adapter=adapter)
            assert last_connect_bot is bot
            assert adapter.bots[bot.self_id] is bot

        assert last_disconnect_bot is bot
        assert bot.self_id not in adapter.bots


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.fastapi:Driver", id="fastapi"),
        pytest.param("nonebot.drivers.quart:Driver", id="quart"),
        pytest.param(
            "nonebot.drivers.httpx:Driver",
            id="httpx",
            marks=pytest.mark.xfail(
                reason="not a server", raises=TypeError, strict=True
            ),
        ),
        pytest.param(
            "nonebot.drivers.websockets:Driver",
            id="websockets",
            marks=pytest.mark.xfail(
                reason="not a server", raises=TypeError, strict=True
            ),
        ),
        pytest.param(
            "nonebot.drivers.aiohttp:Driver",
            id="aiohttp",
            marks=pytest.mark.xfail(
                reason="not a server", raises=TypeError, strict=True
            ),
        ),
    ],
    indirect=True,
)
async def test_adapter_server(driver: Driver):
    last_http_setup: Optional[HTTPServerSetup] = None
    last_ws_setup: Optional[WebSocketServerSetup] = None

    def _fake_setup_http_server(setup: HTTPServerSetup):
        nonlocal last_http_setup
        last_http_setup = setup

    def _fake_setup_websocket_server(setup: WebSocketServerSetup):
        nonlocal last_ws_setup
        last_ws_setup = setup

    with pytest.MonkeyPatch.context() as m:
        m.setattr(driver, "setup_http_server", _fake_setup_http_server, raising=False)
        m.setattr(
            driver,
            "setup_websocket_server",
            _fake_setup_websocket_server,
            raising=False,
        )

        async def handle_http(request: Request):
            return Response(200, content="test")

        async def handle_ws(ws: WebSocket):
            ...

        adapter = FakeAdapter(driver)

        setup = HTTPServerSetup(URL("/test"), "GET", "test", handle_http)
        adapter.setup_http_server(setup)
        assert last_http_setup is setup

        setup = WebSocketServerSetup(URL("/test"), "test", handle_ws)
        adapter.setup_websocket_server(setup)
        assert last_ws_setup is setup


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param(
            "nonebot.drivers.fastapi:Driver",
            id="fastapi",
            marks=pytest.mark.xfail(
                reason="not a http client", raises=TypeError, strict=True
            ),
        ),
        pytest.param(
            "nonebot.drivers.quart:Driver",
            id="quart",
            marks=pytest.mark.xfail(
                reason="not a http client", raises=TypeError, strict=True
            ),
        ),
        pytest.param("nonebot.drivers.httpx:Driver", id="httpx"),
        pytest.param(
            "nonebot.drivers.websockets:Driver",
            id="websockets",
            marks=pytest.mark.xfail(
                reason="not a http client", raises=TypeError, strict=True
            ),
        ),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_adapter_http_client(driver: Driver):
    last_request: Optional[Request] = None

    async def _fake_request(request: Request):
        nonlocal last_request
        last_request = request

    with pytest.MonkeyPatch.context() as m:
        m.setattr(driver, "request", _fake_request, raising=False)

        adapter = FakeAdapter(driver)

        request = Request("GET", URL("/test"))
        await adapter.request(request)
        assert last_request is request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param(
            "nonebot.drivers.fastapi:Driver",
            id="fastapi",
            marks=pytest.mark.xfail(
                reason="not a websocket client", raises=TypeError, strict=True
            ),
        ),
        pytest.param(
            "nonebot.drivers.quart:Driver",
            id="quart",
            marks=pytest.mark.xfail(
                reason="not a websocket client", raises=TypeError, strict=True
            ),
        ),
        pytest.param(
            "nonebot.drivers.httpx:Driver",
            id="httpx",
            marks=pytest.mark.xfail(
                reason="not a websocket client", raises=TypeError, strict=True
            ),
        ),
        pytest.param("nonebot.drivers.websockets:Driver", id="websockets"),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_adapter_websocket_client(driver: Driver):
    _fake_ws = object()
    _last_request: Optional[Request] = None

    @asynccontextmanager
    async def _fake_websocket(setup: Request):
        nonlocal _last_request
        _last_request = setup
        yield _fake_ws

    with pytest.MonkeyPatch.context() as m:
        m.setattr(driver, "websocket", _fake_websocket, raising=False)

        adapter = FakeAdapter(driver)

        request = Request("GET", URL("/test"))
        async with adapter.websocket(request) as ws:
            assert _last_request is request
            assert ws is _fake_ws
