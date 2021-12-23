"""
AIOHTTP 驱动适配
================

本驱动仅支持客户端连接
"""

from nonebot.typing import overrides
from nonebot.drivers import Request, Response
from nonebot.drivers._block_driver import BlockDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import HTTPVersion, ForwardMixin, combine_driver

try:
    import aiohttp
except ImportError:
    raise ImportError(
        "Please install aiohttp first to use this driver. `pip install nonebot2[aiohttp]`"
    ) from None


class AiohttpMixin(ForwardMixin):
    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "aiohttp"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        timeout = aiohttp.ClientTimeout(setup.timeout)
        async with aiohttp.ClientSession(version=version) as session:
            async with session.request(
                setup.method,
                setup.url,
                data=setup.content,
                headers=setup.headers,
                timeout=timeout,
            ) as response:
                res = Response(
                    response.status,
                    headers=response.headers.copy(),
                    content=await response.read(),
                    request=setup,
                )
                return res

    @overrides(ForwardMixin)
    async def websocket(self, setup: Request) -> "WebSocket":
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        session = aiohttp.ClientSession(version=version)
        ws = await session.ws_connect(
            setup.url,
            method=setup.method,
            timeout=setup.timeout or 10,
            headers=setup.headers,
        )
        websocket = WebSocket(request=setup, session=session, websocket=ws)
        return websocket


class WebSocket(BaseWebSocket):
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
    @overrides(BaseWebSocket)
    def closed(self):
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000):
        await self.websocket.close(code=code)
        await self.session.close()

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        return await self.websocket.receive_str()

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        await self.websocket.send_str(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send_bytes(data)


Driver = combine_driver(BlockDriver, AiohttpMixin)
