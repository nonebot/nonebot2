"""[websockets](https://websockets.readthedocs.io/) 驱动适配

```bash
nb driver install websockets
# 或者
pip install nonebot2[websockets]
```

:::tip 提示
本驱动仅支持客户端 WebSocket 连接
:::

FrontMatter:
    sidebar_position: 4
    description: nonebot.drivers.websockets 模块
"""

import logging
from functools import wraps
from contextlib import asynccontextmanager
from typing_extensions import ParamSpec, override
from typing import Type, Union, TypeVar, Callable, Awaitable, AsyncGenerator

from nonebot.log import LoguruHandler
from nonebot.drivers import Request, Response
from nonebot.exception import WebSocketClosed
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import ForwardMixin, ForwardDriver, combine_driver

try:
    from websockets.exceptions import ConnectionClosed
    from websockets.legacy.client import Connect, WebSocketClientProtocol
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install websockets first to use this driver. "
        "Install with pip: `pip install nonebot2[websockets]`"
    ) from e

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.Logger("websockets.client", "INFO")
logger.addHandler(LoguruHandler())


def catch_closed(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def decorator(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except ConnectionClosed as e:
            if e.rcvd_then_sent:
                raise WebSocketClosed(e.rcvd.code, e.rcvd.reason)  # type: ignore
            else:
                raise WebSocketClosed(e.sent.code, e.sent.reason)  # type: ignore

    return decorator


class Mixin(ForwardMixin):
    """Websockets Mixin"""

    @property
    @override
    def type(self) -> str:
        return "websockets"

    @override
    async def request(self, setup: Request) -> Response:
        return await super(Mixin, self).request(setup)

    @override
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        connection = Connect(
            str(setup.url),
            extra_headers={**setup.headers, **setup.cookies.as_header(setup)},
            open_timeout=setup.timeout,
        )
        async with connection as ws:
            yield WebSocket(request=setup, websocket=ws)


class WebSocket(BaseWebSocket):
    """Websockets WebSocket Wrapper"""

    @override
    def __init__(self, *, request: Request, websocket: WebSocketClientProtocol):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @override
    def closed(self) -> bool:
        return self.websocket.closed

    @override
    async def accept(self):
        raise NotImplementedError

    @override
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code, reason)

    @override
    @catch_closed
    async def receive(self) -> Union[str, bytes]:
        return await self.websocket.recv()

    @override
    @catch_closed
    async def receive_text(self) -> str:
        msg = await self.websocket.recv()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @override
    @catch_closed
    async def receive_bytes(self) -> bytes:
        msg = await self.websocket.recv()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @override
    async def send_text(self, data: str) -> None:
        await self.websocket.send(data)

    @override
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send(data)


Driver: Type[ForwardDriver] = combine_driver(NoneDriver, Mixin)  # type: ignore
"""Websockets Driver"""
