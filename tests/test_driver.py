from http.cookies import SimpleCookie
import json
from typing import Any, Optional

import anyio
from nonebug import App
import pytest

from nonebot.adapters import Bot
from nonebot.dependencies import Dependent
from nonebot.drivers import (
    URL,
    ASGIMixin,
    Driver,
    HTTPClientMixin,
    HTTPServerSetup,
    Request,
    Response,
    WebSocket,
    WebSocketClientMixin,
    WebSocketServerSetup,
)
from nonebot.exception import WebSocketClosed
from nonebot.params import Depends
from utils import FakeAdapter


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver", [pytest.param("nonebot.drivers.none:Driver", id="none")], indirect=True
)
async def test_lifespan(driver: Driver):
    adapter = FakeAdapter(driver)

    start_log = []
    ready_log = []
    shutdown_log = []

    @driver.on_startup
    async def _startup1():
        assert start_log == []
        start_log.append(1)

    @driver.on_startup
    async def _startup2():
        assert start_log == [1]
        start_log.append(2)

    @adapter.on_ready
    def _ready1():
        assert start_log == [1, 2]
        assert ready_log == []
        ready_log.append(1)

    @adapter.on_ready
    def _ready2():
        assert ready_log == [1]
        ready_log.append(2)

    @driver.on_shutdown
    async def _shutdown1():
        assert shutdown_log == [2]
        shutdown_log.append(1)

    @driver.on_shutdown
    async def _shutdown2():
        assert shutdown_log == []
        shutdown_log.append(2)

    async with driver._lifespan:
        assert start_log == [1, 2]
        assert ready_log == [1, 2]

    assert shutdown_log == [2, 1]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.fastapi:Driver", id="fastapi"),
        pytest.param("nonebot.drivers.quart:Driver", id="quart"),
    ],
    indirect=True,
)
async def test_http_server(app: App, driver: Driver):
    assert isinstance(driver, ASGIMixin)

    async def _handle_http(request: Request) -> Response:
        assert request.content in (b"test", "test")
        return Response(200, content="test")

    http_setup = HTTPServerSetup(URL("/http_test"), "POST", "http_test", _handle_http)
    driver.setup_http_server(http_setup)

    async with app.test_server(driver.asgi) as ctx:
        client = ctx.get_client()
        response = await client.post("/http_test", data="test")
        assert response.status_code == 200
        assert response.text == "test"

    await anyio.sleep(1)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.fastapi:Driver", id="fastapi"),
        pytest.param("nonebot.drivers.quart:Driver", id="quart"),
    ],
    indirect=True,
)
async def test_websocket_server(app: App, driver: Driver):
    assert isinstance(driver, ASGIMixin)

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

        with pytest.raises(WebSocketClosed, match=r"code=1000"):
            await ws.receive()

    ws_setup = WebSocketServerSetup(URL("/ws_test"), "ws_test", _handle_ws)
    driver.setup_websocket_server(ws_setup)

    async with app.test_server(driver.asgi) as ctx:
        client = ctx.get_client()

        async with client.websocket_connect("/ws_test") as ws:
            await ws.send_text("ping")
            assert await ws.receive_text() == "pong"
            await ws.send_bytes(b"ping")
            assert await ws.receive_bytes() == b"pong"

            await ws.send_text("ping")
            assert await ws.receive_text() == "pong"

            await ws.send_bytes(b"ping")
            assert await ws.receive_bytes() == b"pong"

            await ws.close(code=1000)

    await anyio.sleep(1)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.fastapi:Driver", id="fastapi"),
        pytest.param("nonebot.drivers.quart:Driver", id="quart"),
    ],
    indirect=True,
)
async def test_cross_context(app: App, driver: Driver):
    assert isinstance(driver, ASGIMixin)

    ws: Optional[WebSocket] = None
    ws_ready = anyio.Event()
    ws_should_close = anyio.Event()

    # create a background task before the ws connection established
    async def background_task():
        try:
            await ws_ready.wait()
            assert ws is not None

            await ws.send("ping")
            data = await ws.receive()
            assert data == "pong"
        finally:
            ws_should_close.set()

    async def _handle_ws(websocket: WebSocket) -> None:
        nonlocal ws
        await websocket.accept()
        ws = websocket
        ws_ready.set()

        await ws_should_close.wait()
        await websocket.close()

    ws_setup = WebSocketServerSetup(URL("/ws_test"), "ws_test", _handle_ws)
    driver.setup_websocket_server(ws_setup)

    async with anyio.create_task_group() as tg, app.test_server(driver.asgi) as ctx:
        tg.start_soon(background_task)

        client = ctx.get_client()

        async with client.websocket_connect("/ws_test") as websocket:
            try:
                data = await websocket.receive_text()
                assert data == "ping"
                await websocket.send_text("pong")
            except Exception as e:
                if not e.args or "websocket.close" not in str(e.args[0]):
                    raise

    await anyio.sleep(1)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.httpx:Driver", id="httpx"),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_http_client(driver: Driver, server_url: URL):
    assert isinstance(driver, HTTPClientMixin)

    # simple post with query, headers, cookies and content
    request = Request(
        "POST",
        server_url,
        params={"param": "test"},
        headers={"X-Test": "test"},
        cookies={"session": "test"},
        content="test",
    )
    response = await driver.request(request)
    assert server_url.host is not None
    request_raw_url = Request(
        "POST",
        (
            server_url.scheme.encode("ascii"),
            server_url.host.encode("ascii"),
            server_url.port,
            server_url.path.encode("ascii"),
        ),
        params={"param": "test"},
        headers={"X-Test": "test"},
        cookies={"session": "test"},
        content="test",
    )
    assert request.url == request_raw_url.url, (
        "request.url should be equal to request_raw_url.url"
    )
    assert response.status_code == 200
    assert response.content
    data = json.loads(response.content)
    assert data["method"] == "POST"
    assert data["args"] == {"param": "test"}
    assert data["headers"].get("X-Test") == "test"
    assert data["headers"].get("Cookie") == "session=test"
    assert data["data"] == "test"

    # post with data body
    request = Request("POST", server_url, data={"form": "test"})
    response = await driver.request(request)
    assert response.status_code == 200
    assert response.content
    data = json.loads(response.content)
    assert data["method"] == "POST"
    assert data["form"] == {"form": "test"}

    # post with json body
    request = Request("POST", server_url, json={"json": "test"})
    response = await driver.request(request)
    assert response.status_code == 200
    assert response.content
    data = json.loads(response.content)
    assert data["method"] == "POST"
    assert data["json"] == {"json": "test"}

    # post with files and form data
    request = Request(
        "POST",
        server_url,
        data={"form": "test"},
        files=[
            ("test1", b"test"),
            ("test2", ("test.txt", b"test")),
            ("test3", ("test.txt", b"test", "text/plain")),
        ],
    )
    response = await driver.request(request)
    assert response.status_code == 200
    assert response.content
    data = json.loads(response.content)
    assert data["method"] == "POST"
    assert data["form"] == {"form": "test"}
    assert data["files"] == {
        "test1": "test",
        "test2": "test",
        "test3": "test",
    }, "file parsing error"

    await anyio.sleep(1)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.httpx:Driver", id="httpx"),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_http_client_session(driver: Driver, server_url: URL):
    assert isinstance(driver, HTTPClientMixin)

    session = driver.get_session(
        params={"session": "test"},
        headers={"X-Session": "test"},
        cookies={"session": "test"},
    )
    request = Request("GET", server_url)
    with pytest.raises(RuntimeError):
        await session.request(request)

    with pytest.raises(RuntimeError):  # noqa: PT012
        async with session:
            async with session:
                ...

    async with session as session:
        # simple post with query, headers, cookies and content
        request = Request(
            "POST",
            server_url,
            params={"param": "test"},
            headers={"X-Test": "test"},
            cookies={"cookie": "test"},
            content="test",
        )
        response = await session.request(request)
        assert response.status_code == 200
        assert response.content
        data = json.loads(response.content)
        assert data["method"] == "POST"
        assert data["args"] == {"session": "test", "param": "test"}
        assert data["headers"].get("X-Session") == "test"
        assert data["headers"].get("X-Test") == "test"
        assert {
            key: cookie.value
            for key, cookie in SimpleCookie(data["headers"].get("Cookie")).items()
        } == {
            "session": "test",
            "cookie": "test",
        }
        assert data["data"] == "test"

        # post with data body
        request = Request("POST", server_url, data={"form": "test"})
        response = await session.request(request)
        assert response.status_code == 200
        assert response.content
        data = json.loads(response.content)
        assert data["method"] == "POST"
        assert data["args"] == {"session": "test"}
        assert data["headers"].get("X-Session") == "test"
        assert {
            key: cookie.value
            for key, cookie in SimpleCookie(data["headers"].get("Cookie")).items()
        } == {"session": "test"}
        assert data["form"] == {"form": "test"}

        # post with json body
        request = Request("POST", server_url, json={"json": "test"})
        response = await session.request(request)
        assert response.status_code == 200
        assert response.content
        data = json.loads(response.content)
        assert data["method"] == "POST"
        assert data["args"] == {"session": "test"}
        assert data["headers"].get("X-Session") == "test"
        assert {
            key: cookie.value
            for key, cookie in SimpleCookie(data["headers"].get("Cookie")).items()
        } == {"session": "test"}
        assert data["json"] == {"json": "test"}

        # post with files and form data
        request = Request(
            "POST",
            server_url,
            data={"form": "test"},
            files=[
                ("test1", b"test"),
                ("test2", ("test.txt", b"test")),
                ("test3", ("test.txt", b"test", "text/plain")),
            ],
        )
        response = await session.request(request)
        assert response.status_code == 200
        assert response.content
        data = json.loads(response.content)
        assert data["method"] == "POST"
        assert data["args"] == {"session": "test"}
        assert data["headers"].get("X-Session") == "test"
        assert {
            key: cookie.value
            for key, cookie in SimpleCookie(data["headers"].get("Cookie")).items()
        } == {"session": "test"}
        assert data["form"] == {"form": "test"}
        assert data["files"] == {
            "test1": "test",
            "test2": "test",
            "test3": "test",
        }, "file parsing error"

    await anyio.sleep(1)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "driver",
    [
        pytest.param("nonebot.drivers.websockets:Driver", id="websockets"),
        pytest.param("nonebot.drivers.aiohttp:Driver", id="aiohttp"),
    ],
    indirect=True,
)
async def test_websocket_client(driver: Driver, server_url: URL):
    assert isinstance(driver, WebSocketClientMixin)

    request = Request("GET", server_url.with_scheme("ws"))
    async with driver.websocket(request) as ws:
        await ws.send("test")
        assert await ws.receive() == "test"

        await ws.send(b"test")
        assert await ws.receive() == b"test"

        await ws.send_text("test")
        assert await ws.receive_text() == "test"

        await ws.send_bytes(b"test")
        assert await ws.receive_bytes() == b"test"

        await ws.send("quit")
        with pytest.raises(WebSocketClosed, match=r"code=1000"):
            await ws.receive()

    await anyio.sleep(1)


@pytest.mark.parametrize(
    ("driver", "driver_type"),
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
def test_combine_driver(driver: Driver, driver_type: str):
    assert driver.type == driver_type


@pytest.mark.anyio
async def test_bot_connect_hook(app: App, driver: Driver):
    with pytest.MonkeyPatch.context() as m:
        conn_hooks: set[Dependent[Any]] = set()
        disconn_hooks: set[Dependent[Any]] = set()
        m.setattr(Driver, "_bot_connection_hook", conn_hooks)
        m.setattr(Driver, "_bot_disconnection_hook", disconn_hooks)

        conn_should_be_called = False
        disconn_should_be_called = False
        dependency_should_be_run = False
        dependency_should_be_cleaned = False

        async def dependency():
            nonlocal dependency_should_be_run, dependency_should_be_cleaned
            dependency_should_be_run = True
            try:
                yield 1
            finally:
                dependency_should_be_cleaned = True

        @driver.on_bot_connect
        async def conn_hook(foo: Bot, dep: int = Depends(dependency), default: int = 1):
            nonlocal conn_should_be_called

            if foo is not bot:
                pytest.fail("on_bot_connect hook called with wrong bot")
            if dep != 1:
                pytest.fail("on_bot_connect hook called with wrong dependency")
            if default != 1:
                pytest.fail("on_bot_connect hook called with wrong default value")

            conn_should_be_called = True

        @driver.on_bot_disconnect
        async def disconn_hook(
            foo: Bot, dep: int = Depends(dependency), default: int = 1
        ):
            nonlocal disconn_should_be_called

            if foo is not bot:
                pytest.fail("on_bot_disconnect hook called with wrong bot")
            if dep != 1:
                pytest.fail("on_bot_connect hook called with wrong dependency")
            if default != 1:
                pytest.fail("on_bot_connect hook called with wrong default value")

            disconn_should_be_called = True

        if conn_hook not in {hook.call for hook in conn_hooks}:  # type: ignore
            pytest.fail("on_bot_connect hook not registered")
        if disconn_hook not in {hook.call for hook in disconn_hooks}:  # type: ignore
            pytest.fail("on_bot_disconnect hook not registered")

        async with app.test_api() as ctx:
            bot = ctx.create_bot()

        await anyio.sleep(1)

        if not conn_should_be_called:
            pytest.fail("on_bot_connect hook not called")
        if not disconn_should_be_called:
            pytest.fail("on_bot_disconnect hook not called")
        if not dependency_should_be_run:
            pytest.fail("dependency not run")
        if not dependency_should_be_cleaned:
            pytest.fail("dependency not cleaned")
