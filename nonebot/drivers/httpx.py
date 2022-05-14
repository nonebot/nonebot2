"""[HTTPX](https://www.python-httpx.org/) 驱动适配

```bash
nb driver install httpx
# 或者
pip install nonebot2[httpx]
```

:::tip 提示
本驱动仅支持客户端 HTTP 连接
:::

FrontMatter:
    sidebar_position: 3
    description: nonebot.drivers.httpx 模块
"""
from typing import Type, AsyncGenerator
from contextlib import asynccontextmanager

from nonebot.typing import overrides
from nonebot.drivers._block_driver import BlockDriver
from nonebot.drivers import (
    Request,
    Response,
    WebSocket,
    HTTPVersion,
    ForwardMixin,
    ForwardDriver,
    combine_driver,
)

try:
    import httpx
except ImportError:
    raise ImportError(
        "Please install httpx by using `pip install nonebot2[httpx]`"
    ) from None


class Mixin(ForwardMixin):
    """HTTPX Mixin"""

    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "httpx"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        async with httpx.AsyncClient(
            http2=setup.version == HTTPVersion.H2,
            proxies=setup.proxy,  # type: ignore
            follow_redirects=True,
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,  # type: ignore
                data=setup.data,  # type: ignore
                json=setup.json,
                files=setup.files,  # type: ignore
                headers=tuple(setup.headers.items()),
                timeout=setup.timeout,
            )
            return Response(
                response.status_code,
                headers=response.headers.multi_items(),
                content=response.content,
                request=setup,
            )

    @overrides(ForwardMixin)
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        async with super(Mixin, self).websocket(setup) as ws:
            yield ws


Driver: Type[ForwardDriver] = combine_driver(BlockDriver, Mixin)  # type: ignore
"""HTTPX Driver"""
