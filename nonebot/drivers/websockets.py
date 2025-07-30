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
    mdx:
        format: md
    sidebar_position: 4
    description: nonebot.drivers.websockets 模块
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import wraps
import logging
from types import CoroutineType
from typing import TYPE_CHECKING, Any, Callable, TypeVar, Union
from typing_extensions import ParamSpec, override

from nonebot.drivers import Request, Timeout, WebSocketClientMixin, combine_driver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.exception import WebSocketClosed
from nonebot.log import LoguruHandler

try:
    from websockets import ClientConnection, ConnectionClosed, connect
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install websockets first to use this driver. "
        "Install with pip: `pip install nonebot2[websockets]`"
    ) from e

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.Logger("websockets.client", "INFO")
logger.addHandler(LoguruHandler())


def catch_closed(
    func: Callable[P, "CoroutineType[Any, Any, T]"],
) -> Callable[P, "CoroutineType[Any, Any, T]"]:
    @wraps(func)
    async def decorator(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except ConnectionClosed as e:
            raise WebSocketClosed(e.code, e.reason)

    return decorator


class Mixin(WebSocketClientMixin):
    """Websockets Mixin"""

    @property
    @override
    def type(self) -> str:
        return "websockets"

    @override
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        if isinstance(setup.timeout, Timeout):
            timeout = setup.timeout.total or setup.timeout.connect or setup.timeout.read
        else:
            timeout = setup.timeout

        connection = connect(
            str(setup.url),
            additional_headers={**setup.headers, **setup.cookies.as_header(setup)},
            proxy=setup.proxy if setup.proxy is not None else True,
            open_timeout=timeout,
        )
        async with connection as ws:
            yield WebSocket(request=setup, websocket=ws)


class WebSocket(BaseWebSocket):
    """Websockets WebSocket Wrapper"""

    @override
    def __init__(self, *, request: Request, websocket: ClientConnection):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @override
    def closed(self) -> bool:
        return self.websocket.close_code is not None

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


if TYPE_CHECKING:

    class Driver(Mixin, NoneDriver): ...

else:
    Driver = combine_driver(NoneDriver, Mixin)
    """Websockets Driver"""
