import logging
from functools import wraps
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.typing import overrides
from nonebot.log import LoguruHandler
from nonebot.drivers import Request, Response
from nonebot.exception import WebSocketClosed
from nonebot.drivers._block_driver import BlockDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import ForwardMixin, combine_driver

try:
    from websockets.exceptions import ConnectionClosed
    from websockets.legacy.client import Connect, WebSocketClientProtocol
except ImportError:
    raise ImportError(
        "Please install websockets by using `pip install nonebot2[websockets]`"
    )

logger = logging.Logger("websockets.client", "INFO")
logger.addHandler(LoguruHandler())


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConnectionClosed as e:
            if e.rcvd_then_sent:
                raise WebSocketClosed(e.rcvd.code, e.rcvd.reason)
            else:
                raise WebSocketClosed(e.sent.code, e.sent.reason)

    return decorator


class Mixin(ForwardMixin):
    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "websockets"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        return await super(Mixin, self).request(setup)

    @overrides(ForwardMixin)
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        connection = Connect(
            str(setup.url),
            extra_headers=setup.headers.items(),
            open_timeout=setup.timeout,
        )
        async with connection as ws:
            yield WebSocket(request=setup, websocket=ws)


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
    @catch_closed
    async def receive(self) -> str:
        msg = await self.websocket.recv()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @overrides(BaseWebSocket)
    @catch_closed
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
