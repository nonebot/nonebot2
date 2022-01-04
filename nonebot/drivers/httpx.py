from typing import AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.typing import overrides
from nonebot.drivers._block_driver import BlockDriver
from nonebot.drivers import (
    Request,
    Response,
    WebSocket,
    HTTPVersion,
    ForwardMixin,
    combine_driver,
)

try:
    import httpx
except ImportError:
    raise ImportError(
        "Please install httpx by using `pip install nonebot2[httpx]`"
    ) from None


class Mixin(ForwardMixin):
    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "httpx"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        async with httpx.AsyncClient(
            http2=setup.version == HTTPVersion.H2,
            proxies=setup.proxy,
            follow_redirects=True,
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,
                data=setup.data,
                json=setup.json,
                files=setup.files,
                headers=tuple(setup.headers.items()),
                timeout=setup.timeout,
            )
            return Response(
                response.status_code,
                headers=response.headers,
                content=response.content,
                request=setup,
            )

    @overrides(ForwardMixin)
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        async with super(Mixin, self).websocket(setup) as ws:
            yield ws


Driver = combine_driver(BlockDriver, Mixin)
