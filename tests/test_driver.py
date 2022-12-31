import json
import asyncio
from typing import cast

import pytest
from nonebug import App


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonebug_init",
    [
        pytest.param({"driver": "nonebot.drivers.fastapi:Driver"}, id="fastapi"),
        pytest.param({"driver": "nonebot.drivers.quart:Driver"}, id="quart"),
    ],
    indirect=True,
)
async def test_reverse_driver(app: App):
    import nonebot
    from nonebot.exception import WebSocketClosed
    from nonebot.drivers import (
        URL,
        Request,
        Response,
        WebSocket,
        ReverseDriver,
        HTTPServerSetup,
        WebSocketServerSetup,
    )

    driver = cast(ReverseDriver, nonebot.get_driver())

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

    async with app.test_server() as ctx:
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
    "nonebug_init",
    [
        pytest.param({"driver": "nonebot.drivers.httpx:Driver"}, id="httpx"),
        pytest.param({"driver": "nonebot.drivers.aiohttp:Driver"}, id="aiohttp"),
    ],
    indirect=True,
)
async def test_http_driver(app: App):
    import nonebot
    from nonebot.drivers import Request, ForwardDriver

    driver = cast(ForwardDriver, nonebot.get_driver())

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
    "nonebug_init, driver_type",
    [
        pytest.param(
            {"driver": "nonebot.drivers.fastapi:Driver+nonebot.drivers.aiohttp:Mixin"},
            "fastapi+aiohttp",
            id="fastapi+aiohttp",
        ),
        pytest.param(
            {"driver": "~httpx:Driver+~websockets"},
            "none+httpx+websockets",
            id="httpx+websockets",
        ),
    ],
    indirect=["nonebug_init"],
)
async def test_combine_driver(app: App, driver_type: str):
    import nonebot

    driver = nonebot.get_driver()
    assert driver.type == driver_type
