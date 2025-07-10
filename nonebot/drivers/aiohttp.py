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
    mdx:
        format: md
    sidebar_position: 2
    description: nonebot.drivers.aiohttp 模块
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
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
    WebSocketClientMixin,
    combine_driver,
)
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers.none import Driver as NoneDriver
from nonebot.exception import WebSocketClosed
from nonebot.internal.driver import (
    Cookies,
    CookieTypes,
    HeaderTypes,
    QueryTypes,
    Timeout,
    TimeoutTypes,
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
        timeout: TimeoutTypes = None,
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

        if isinstance(timeout, Timeout):
            self._timeout = aiohttp.ClientTimeout(
                total=timeout.total,
                connect=timeout.connect,
                sock_read=timeout.read,
            )
        else:
            self._timeout = aiohttp.ClientTimeout(timeout)

        self._proxy = proxy

    @property
    def client(self) -> aiohttp.ClientSession:
        if self._client is None:
            raise RuntimeError("Session is not initialized")
        return self._client

    @override
    async def request(self, setup: Request) -> Response:
        if self._params:
            url = setup.url.with_query({**self._params, **setup.url.query})
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

        if isinstance(setup.timeout, Timeout):
            timeout = aiohttp.ClientTimeout(
                total=setup.timeout.total,
                connect=setup.timeout.connect,
                sock_read=setup.timeout.read,
            )
        else:
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
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        if self._params:
            url = setup.url.with_query({**self._params, **setup.url.query})
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

        if isinstance(setup.timeout, Timeout):
            timeout = aiohttp.ClientTimeout(
                total=setup.timeout.total,
                connect=setup.timeout.connect,
                sock_read=setup.timeout.read,
            )
        else:
            timeout = aiohttp.ClientTimeout(setup.timeout)

        async with self.client.request(
            setup.method,
            url,
            data=setup.content or data,
            json=setup.json,
            cookies=cookies,
            headers=setup.headers,
            proxy=setup.proxy or self._proxy,
            timeout=timeout,
        ) as response:
            response_headers = response.headers.copy()
            async for chunk in response.content.iter_chunked(chunk_size):
                yield Response(
                    response.status,
                    headers=response_headers,
                    content=chunk,
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
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        async with self.get_session() as session:
            async for response in session.stream_request(setup, chunk_size=chunk_size):
                yield response

    @override
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        if setup.version == HTTPVersion.H10:
            version = aiohttp.HttpVersion10
        elif setup.version == HTTPVersion.H11:
            version = aiohttp.HttpVersion11
        else:
            raise RuntimeError(f"Unsupported HTTP version: {setup.version}")

        if isinstance(setup.timeout, Timeout):
            timeout = aiohttp.ClientWSTimeout(
                ws_receive=setup.timeout.read,  # type: ignore
                ws_close=setup.timeout.total,  # type: ignore
            )
        else:
            timeout = aiohttp.ClientWSTimeout(ws_close=setup.timeout or 10.0)  # type: ignore

        async with aiohttp.ClientSession(version=version, trust_env=True) as session:
            async with session.ws_connect(
                setup.url,
                method=setup.method,
                timeout=timeout,
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
