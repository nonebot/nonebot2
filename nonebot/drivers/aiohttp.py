"""[AIOHTTP](https://aiohttp.readthedocs.io/en/stable/) 驱动适配器。

```bash
nb driver install aiohttp
# 或者
pip install nonebot2[aiohttp]
```

:::tip 提示
本驱动仅支持客户端连接
:::

FrontMatter:
    sidebar_position: 2
    description: nonebot.drivers.aiohttp 模块
"""

from typing_extensions import override
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Union, Optional

from multidict import CIMultiDict

from nonebot.exception import WebSocketClosed
from nonebot.drivers import URL, Request, Response
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.internal.driver import Cookies, QueryTypes, CookieTypes, HeaderTypes
from nonebot.drivers import (
    HTTPVersion,
    HTTPClientMixin,
    HTTPClientSession,
    WebSocketClientMixin,
    combine_driver,
)

try:
    import aiohttp
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install aiohttp first to use this driver. "
        "Install with pip: `pip install nonebot2[aiohttp]`"
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
        self._client: Optional[aiohttp.ClientSession] = None

        self._params = URL.build(query=params).query if params is not None else None

        self._headers = CIMultiDict(headers) if headers is not None else None
        self._cookies = tuple(
            (cookie.name, cookie.value)
            for cookie in Cookies(cookies)
            if cookie.value is not None
        )

        version = HTTPVersion(version)
        if version == HTTPVersion.H10:
            self._version = aiohttp.HttpVersion10
        elif version == HTTPVersion.H11:
            self._version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {version}")

        self._timeout = timeout
        self._proxy = proxy

    @property
    def client(self) -> aiohttp.ClientSession:
        if self._client is None:
            raise RuntimeError("Session is not initialized")
        return self._client

    @override
    async def request(self, setup: Request) -> Response:
        if self._params:
            params = self._params.copy()
            params.update(setup.url.query)
            url = setup.url.with_query(params)
        else:
            url = setup.url

        data = setup.data
        if setup.files:
            data = aiohttp.FormData(data or {}, quote_fields=False)
            for name, file in setup.files:
                data.add_field(name, file[1], content_type=file[2], filename=file[0])

        cookies = (
            (cookie.name, cookie.value)
            for cookie in setup.cookies
            if cookie.value is not None
        )

        timeout = aiohttp.ClientTimeout(setup.timeout)

        async with await self.client.request(
            setup.method,
            url,
            data=setup.content or data,
            json=setup.json,
            cookies=cookies,
            headers=setup.headers,
            proxy=setup.proxy or self._proxy,
            timeout=timeout,
        ) as response:
            return Response(
                response.status,
                headers=response.headers.copy(),
                content=await response.read(),
                request=setup,
            )

    @override
    async def setup(self) -> None:
        if self._client is not None:
            raise RuntimeError("Session has already been initialized")
        self._client = aiohttp.ClientSession(
            cookies=self._cookies,
            headers=self._headers,
            version=self._version,
            timeout=self._timeout,
            trust_env=True,
        )
        await self._client.__aenter__()

    @override
    async def close(self) -> None:
        try:
            if self._client is not None:
                await self._client.close()
        finally:
            self._client = None


class Mixin(HTTPClientMixin, WebSocketClientMixin):
    """AIOHTTP Mixin"""

    @property
    @override
    def type(self) -> str:
        return "aiohttp"

    @override
    async def request(self, setup: Request) -> Response:
        async with self.get_session() as session:
            return await session.request(setup)

    @override
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        async with aiohttp.ClientSession(version=version, trust_env=True) as session:
            async with session.ws_connect(
                setup.url,
                method=setup.method,
                timeout=setup.timeout or 10,
                headers=setup.headers,
                proxy=setup.proxy,
            ) as ws:
                yield WebSocket(request=setup, session=session, websocket=ws)

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


class WebSocket(BaseWebSocket):
    """AIOHTTP Websocket Wrapper"""

    def __init__(
        self,
        *,
        request: Request,
        session: aiohttp.ClientSession,
        websocket: aiohttp.ClientWebSocketResponse,
    ):
        super().__init__(request=request)
        self.session = session
        self.websocket = websocket

    @property
    @override
    def closed(self):
        return self.websocket.closed

    @override
    async def accept(self):
        raise NotImplementedError

    @override
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code=code, message=reason.encode("utf-8"))
        await self.session.close()

    async def _receive(self) -> aiohttp.WSMessage:
        msg = await self.websocket.receive()
        if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING):
            raise WebSocketClosed(self.websocket.close_code or 1006)
        return msg

    @override
    async def receive(self) -> str:
        msg = await self._receive()
        if msg.type not in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def receive_text(self) -> str:
        msg = await self._receive()
        if msg.type != aiohttp.WSMsgType.TEXT:
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def receive_bytes(self) -> bytes:
        msg = await self._receive()
        if msg.type != aiohttp.WSMsgType.BINARY:
            raise TypeError(
                f"WebSocket received unexpected frame type: {msg.type}, {msg.data!r}"
            )
        return msg.data

    @override
    async def send_text(self, data: str) -> None:
        await self.websocket.send_str(data)

    @override
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send_bytes(data)


if TYPE_CHECKING:

    class Driver(Mixin, NoneDriver): ...

else:
    Driver = combine_driver(NoneDriver, Mixin)
    """AIOHTTP Driver"""
