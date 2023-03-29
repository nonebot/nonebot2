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
from nonebot.drivers.none import Driver as NoneDriver
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
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install httpx by using `pip install nonebot2[httpx]`"
    ) from e


class Mixin(ForwardMixin):
    """HTTPX Mixin"""

    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "httpx"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        async with httpx.AsyncClient(
            cookies=setup.cookies.jar,
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
                headers=response.headers.multi_items(),
                content=response.content,
                request=setup,
            )

    @overrides(ForwardMixin)
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        async with super(Mixin, self).websocket(setup) as ws:
            yield ws


Driver: Type[ForwardDriver] = combine_driver(NoneDriver, Mixin)  # type: ignore
"""HTTPX Driver"""
