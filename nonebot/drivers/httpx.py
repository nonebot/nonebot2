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

from typing_extensions import override
from typing import TYPE_CHECKING, Union, Optional

from multidict import CIMultiDict

from nonebot.drivers.none import Driver as NoneDriver
from nonebot.internal.driver import Cookies, QueryTypes, CookieTypes, HeaderTypes
from nonebot.drivers import (
    URL,
    Request,
    Response,
    HTTPVersion,
    HTTPClientMixin,
    HTTPClientSession,
    combine_driver,
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
        timeout: Optional[float] = None,
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
        self._timeout = timeout
        self._proxy = proxy

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Session is not initialized")
        return self._client

    @override
    async def request(self, setup: Request) -> Response:
        response = await self.client.request(
            setup.method,
            str(setup.url),
            content=setup.content,
            data=setup.data,
            files=setup.files,
            json=setup.json,
            headers=tuple(setup.headers.items()),
            cookies=setup.cookies.jar,
            timeout=setup.timeout,
        )
        return Response(
            response.status_code,
            headers=response.headers.multi_items(),
            content=response.content,
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
            proxies=self._proxy,
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
    def get_session(
        self,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: Optional[float] = None,
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
