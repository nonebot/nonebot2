import logging

from nonebot.typing import overrides
from nonebot.log import LoguruHandler
from nonebot.drivers import Request, Response
from nonebot.drivers._block_driver import BlockDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import ForwardMixin, combine_driver

try:
    from websockets.legacy.client import Connect, WebSocketClientProtocol
except ImportError:
    raise ImportError(
        "Please install websockets by using `pip install nonebot2[websockets]`"
    )

logger = logging.Logger("websockets.client", "INFO")
logger.addHandler(LoguruHandler())


class Mixin(ForwardMixin):
    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "websockets"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        return await super(Mixin, self).request(setup)

    @overrides(ForwardMixin)
    async def websocket(self, setup: Request) -> "WebSocket":
        ws = await Connect(
            str(setup.url),
            extra_headers=setup.headers.items(),
            open_timeout=setup.timeout,
        )
        return WebSocket(request=setup, websocket=ws)


class WebSocket(BaseWebSocket):
    @overrides(BaseWebSocket)
    def __init__(self, *, request: Request, websocket: WebSocketClientProtocol):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code, reason)

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        msg = await self.websocket.recv()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        msg = await self.websocket.recv()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send(data)


Driver = combine_driver(BlockDriver, Mixin)
