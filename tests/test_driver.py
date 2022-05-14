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
