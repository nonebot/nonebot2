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
    mdx:
        format: md
    sidebar_position: 3
    description: nonebot.drivers.httpx 模块
"""

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Optional, Union
from typing_extensions import override

from multidict import CIMultiDict

from nonebot.drivers import (
    URL,
    HTTPClientMixin,
    HTTPClientSession,
    HTTPVersion,
    Request,
    Response,
    combine_driver,
)
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.internal.driver import (
    Cookies,
    CookieTypes,
    HeaderTypes,
    QueryTypes,
    Timeout,
    TimeoutTypes,
)

try:
    import httpx
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install httpx first to use this driver. "
        "Install with pip: `pip install nonebot2[httpx]`"
    ) from e


class Session(HTTPClientSession):
    @override
    def __init__(
        self,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: TimeoutTypes = None,
        proxy: Optional[str] = None,
    ):
        self._client: Optional[httpx.AsyncClient] = None

        self._params = (
            tuple(URL.build(query=params).query.items()) if params is not None else None
        )
        self._headers = (
            tuple(CIMultiDict(headers).items()) if headers is not None else None
        )
        self._cookies = Cookies(cookies)
        self._version = HTTPVersion(version)

        if isinstance(timeout, Timeout):
            self._timeout = httpx.Timeout(
                timeout=timeout.total,
                connect=timeout.connect,
                read=timeout.read,
            )
        else:
            self._timeout = httpx.Timeout(timeout)

        self._proxy = proxy

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Session is not initialized")
        return self._client

    @override
    async def request(self, setup: Request) -> Response:
        if isinstance(setup.timeout, Timeout):
            timeout = httpx.Timeout(
                timeout=setup.timeout.total,
                connect=setup.timeout.connect,
                read=setup.timeout.read,
            )
        else:
            timeout = httpx.Timeout(setup.timeout)

        response = await self.client.request(
            setup.method,
            str(setup.url),
            content=setup.content,
            data=setup.data,
            files=setup.files,
            json=setup.json,
            # ensure the params priority
            params=setup.url.raw_query_string,
            headers=tuple(setup.headers.items()),
            cookies=setup.cookies.jar,
            timeout=timeout,
        )
        return Response(
            response.status_code,
            headers=response.headers.multi_items(),
            content=response.content,
            request=setup,
        )

    @override
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        if isinstance(setup.timeout, Timeout):
            timeout = httpx.Timeout(
                timeout=setup.timeout.total,
                connect=setup.timeout.connect,
                read=setup.timeout.read,
            )
        else:
            timeout = httpx.Timeout(setup.timeout)

        async with self.client.stream(
            setup.method,
            str(setup.url),
            content=setup.content,
            data=setup.data,
            files=setup.files,
            json=setup.json,
            # ensure the params priority
            params=setup.url.raw_query_string,
            headers=tuple(setup.headers.items()),
            cookies=setup.cookies.jar,
            timeout=timeout,
        ) as response:
            response_headers = response.headers.multi_items()
            async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                yield Response(
                    response.status_code,
                    headers=response_headers,
                    content=chunk,
                    request=setup,
                )

    @override
    async def setup(self) -> None:
        if self._client is not None:
            raise RuntimeError("Session has already been initialized")
        self._client = httpx.AsyncClient(
            params=self._params,
            headers=self._headers,
            cookies=self._cookies.jar,
            http2=self._version == HTTPVersion.H2,
            proxy=self._proxy,
            follow_redirects=True,
        )
        await self._client.__aenter__()

    @override
    async def close(self) -> None:
        try:
            if self._client is not None:
                await self._client.aclose()
        finally:
            self._client = None


class Mixin(HTTPClientMixin):
    """HTTPX Mixin"""

    @property
    @override
    def type(self) -> str:
        return "httpx"

    @override
    async def request(self, setup: Request) -> Response:
        async with self.get_session(
            version=setup.version, proxy=setup.proxy
        ) as session:
            return await session.request(setup)

    @override
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        async with self.get_session(
            version=setup.version, proxy=setup.proxy
        ) as session:
            async for response in session.stream_request(setup, chunk_size=chunk_size):
                yield response

    @override
    def get_session(
        self,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: TimeoutTypes = None,
        proxy: Optional[str] = None,
    ) -> Session:
        return Session(
            params=params,
            headers=headers,
            cookies=cookies,
            version=version,
            timeout=timeout,
            proxy=proxy,
        )


if TYPE_CHECKING:

    class Driver(Mixin, NoneDriver): ...

else:
    Driver = combine_driver(NoneDriver, Mixin)
    """HTTPX Driver"""
