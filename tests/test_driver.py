import json
import asyncio
from typing import cast

import pytest
from nonebug import App

import nonebot
from nonebot.config import Env
from nonebot import _resolve_combine_expr
from nonebot.exception import WebSocketClosed
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)


@pytest.fixture(name="driver")
def load_driver(request: pytest.FixtureRequest) -> Driver:
    driver_name = getattr(request, "param", None)
    global_driver = nonebot.get_driver()
    if driver_name is None:
        return global_driver

    DriverClass = _resolve_combine_expr(driver_name)
    return DriverClass(Env(environment=global_driver.env), global_driver.config)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.fastapi:Driver", id="fastapi"),
        pytest.param("nonebot.drivers.quart:Driver", id="quart"),
    ],
    indirect=True,
)
async def test_reverse_driver(app: App, driver: Driver):
    driver = cast(ReverseDriver, driver)

    async def _handle_http(request: Request) -> Response:
        assert request.content in (b"test", "test")
        return Response(200, content="test")

    async def _handle_ws(ws: WebSocket) -> None:
        await ws.accept()
        data = await ws.receive()
        assert data == "ping"
        await ws.send("pong")

        data = await ws.receive()
        assert data == b"ping"
        await ws.send(b"pong")

        data = await ws.receive_text()
        assert data == "ping"
        await ws.send("pong")

        data = await ws.receive_bytes()
        assert data == b"ping"
        await ws.send(b"pong")

        with pytest.raises(WebSocketClosed):
            await ws.receive()

    http_setup = HTTPServerSetup(URL("/http_test"), "POST", "http_test", _handle_http)
    driver.setup_http_server(http_setup)

    ws_setup = WebSocketServerSetup(URL("/ws_test"), "ws_test", _handle_ws)
    driver.setup_websocket_server(ws_setup)

    async with app.test_server(driver.asgi) as ctx:
        client = ctx.get_client()
        response = await client.post("/http_test", data="test")
        assert response.status_code == 200
        assert response.text == "test"

        async with client.websocket_connect("/ws_test") as ws:
            await ws.send_text("ping")
            assert await ws.receive_text() == "pong"
            await ws.send_bytes(b"ping")
            assert await ws.receive_bytes() == b"pong"

            await ws.send_text("ping")
            assert await ws.receive_text() == "pong"

            await ws.send_bytes(b"ping")
            assert await ws.receive_bytes() == b"pong"

            await ws.close()

    await asyncio.sleep(1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.httpx:Driver", id="httpx"),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_http_driver(driver: Driver):
    driver = cast(ForwardDriver, driver)

    request = Request(
        "POST",
        "https://httpbin.org/post",
        params={"param": "test"},
        headers={"X-Test": "test"},
        cookies={"session": "test"},
        content="test",
    )
    response = await driver.request(request)
    assert response.status_code == 200 and response.content
    data = json.loads(response.content)
    assert data["args"] == {"param": "test"}
    assert data["headers"].get("X-Test") == "test"
    assert data["headers"].get("Cookie") == "session=test"
    assert data["data"] == "test"

    request = Request("POST", "https://httpbin.org/post", data={"form": "test"})
    response = await driver.request(request)
    assert response.status_code == 200 and response.content
    data = json.loads(response.content)
    assert data["form"] == {"form": "test"}

    request = Request("POST", "https://httpbin.org/post", json={"json": "test"})
    response = await driver.request(request)
    assert response.status_code == 200 and response.content
    data = json.loads(response.content)
    assert data["json"] == {"json": "test"}

    request = Request(
        "POST", "https://httpbin.org/post", files={"test": ("test.txt", b"test")}
    )
    response = await driver.request(request)
    assert response.status_code == 200 and response.content
    data = json.loads(response.content)
    assert data["files"] == {"test": "test"}

    await asyncio.sleep(1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "driver, driver_type",
    [
        pytest.param(
            "nonebot.drivers.fastapi:Driver+nonebot.drivers.aiohttp:Mixin",
            "fastapi+aiohttp",
            id="fastapi+aiohttp",
        ),
        pytest.param(
            "~httpx:Driver+~websockets",
            "none+httpx+websockets",
            id="httpx+websockets",
        ),
    ],
    indirect=["driver"],
)
async def test_combine_driver(driver: Driver, driver_type: str):
    assert driver.type == driver_type


@pytest.mark.asyncio
async def test_bot_connect_hook(app: App, driver: Driver):
    with pytest.MonkeyPatch.context() as m:
        conn_hooks = set()
        disconn_hooks = set()
        m.setattr(Driver, "_bot_connection_hook", conn_hooks)
        m.setattr(Driver, "_bot_disconnection_hook", disconn_hooks)

        conn_should_be_called = False
        disconn_should_be_called = False

        @driver.on_bot_connect
        async def conn_hook():
            nonlocal conn_should_be_called
            conn_should_be_called = True

        @driver.on_bot_disconnect
        async def disconn_hook():
            nonlocal disconn_should_be_called
            disconn_should_be_called = True

        if conn_hook not in conn_hooks:
            pytest.fail("on_bot_connect hook not registered")
        if disconn_hook not in disconn_hooks:
            pytest.fail("on_bot_disconnect hook not registered")

        async with app.test_api() as ctx:
            ctx.create_bot()

        if not conn_should_be_called:
            pytest.fail("on_bot_connect hook not called")
        if not disconn_should_be_called:
            pytest.fail("on_bot_disconnect hook not called")
