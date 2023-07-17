"""[AIOHTTP](https://aiohttp.readthedocs.io/en/stable/) 驱动适配器。

```bash
nb driver install aiohttp
# 或者
pip install nonebot2[aiohttp]
```

:::tip 提示
本驱动仅支持客户端连接
:::

FrontMatter:
    sidebar_position: 2
    description: nonebot.drivers.aiohttp 模块
"""

from typing_extensions import override
from typing import Type, AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.drivers import Request, Response
from nonebot.exception import WebSocketClosed
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import HTTPVersion, ForwardMixin, ForwardDriver, combine_driver

try:
    import aiohttp
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install aiohttp first to use this driver. "
        "Install with pip: `pip install nonebot2[aiohttp]`"
    ) from e


class Mixin(ForwardMixin):
    """AIOHTTP Mixin"""

    @property
    @override
    def type(self) -> str:
        return "aiohttp"

    @override
    async def request(self, setup: Request) -> Response:
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        timeout = aiohttp.ClientTimeout(setup.timeout)

        data = setup.data
        if setup.files:
            data = aiohttp.FormData(data or {})
            for name, file in setup.files:
                data.add_field(name, file[1], content_type=file[2], filename=file[0])

        cookies = {
            cookie.name: cookie.value for cookie in setup.cookies if cookie.value
        }
        async with aiohttp.ClientSession(
            cookies=cookies, version=version, trust_env=True
        ) as session:
            async with session.request(
                setup.method,
                setup.url,
                data=setup.content or data,
                json=setup.json,
                headers=setup.headers,
                timeout=timeout,
                proxy=setup.proxy,
            ) as response:
                return Response(
                    response.status,
                    headers=response.headers.copy(),
                    content=await response.read(),
                    request=setup,
                )

    @override
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        async with aiohttp.ClientSession(version=version, trust_env=True) as session:
            async with session.ws_connect(
                setup.url,
                method=setup.method,
                timeout=setup.timeout or 10,
                headers=setup.headers,
                proxy=setup.proxy,
            ) as ws:
                yield WebSocket(request=setup, session=session, websocket=ws)


class WebSocket(BaseWebSocket):
    """AIOHTTP Websocket Wrapper"""

    def __init__(
        self,
        *,
        request: Request,
        session: aiohttp.ClientSession,
        websocket: aiohttp.ClientWebSocketResponse,
    ):
        super().__init__(request=request)
        self.session = session
        self.websocket = websocket

    @property
    @override
    def closed(self):
        return self.websocket.closed

    @override
    async def accept(self):
        raise NotImplementedError

    @override
    async def close(self, code: int = 1000):
        await self.websocket.close(code=code)
        await self.session.close()

    async def _receive(self) -> aiohttp.WSMessage:
        msg = await self.websocket.receive()
        if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING):
            raise WebSocketClosed(self.websocket.close_code or 1006)
        return msg

    @override
    async def receive(self) -> str:
        msg = await self._receive()
        if msg.type not in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def receive_text(self) -> str:
        msg = await self._receive()
        if msg.type != aiohttp.WSMsgType.TEXT:
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def receive_bytes(self) -> bytes:
        msg = await self._receive()
        if msg.type != aiohttp.WSMsgType.BINARY:
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def send_text(self, data: str) -> None:
        await self.websocket.send_str(data)

    @override
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send_bytes(data)


Driver: Type[ForwardDriver] = combine_driver(NoneDriver, Mixin)  # type: ignore
"""AIOHTTP Driver"""
