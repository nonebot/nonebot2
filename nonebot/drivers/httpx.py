import httpx

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


class HttpxMixin(ForwardMixin):
    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "httpx"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        async with httpx.AsyncClient(
            http2=setup.version == HTTPVersion.H2, follow_redirects=True
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,
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
    async def websocket(self, setup: Request) -> WebSocket:
        return await super(HttpxMixin, self).websocket(setup)


Driver = combine_driver(BlockDriver, HttpxMixin)
