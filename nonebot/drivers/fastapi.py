"""
FastAPI 驱动适配
================

本驱动同时支持服务端以及客户端连接

后端使用方法请参考: `FastAPI 文档`_

.. _FastAPI 文档:
    https://fastapi.tiangolo.com/
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import List, Union, TypeVar, Callable, Optional, Awaitable, cast

import httpx
import uvicorn
from pydantic import BaseSettings
from fastapi.responses import Response
from websockets.exceptions import ConnectionClosed
from fastapi import FastAPI, Request, HTTPException, status
from starlette.websockets import WebSocket as FastAPIWebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect
from websockets.legacy.client import Connect, WebSocketClientProtocol

from nonebot.config import Env
from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.config import Config as NoneBotConfig
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import (
    HTTPRequest,
    ForwardDriver,
    ReverseDriver,
    WebSocketSetup,
    HTTPPollingSetup,
)

S = TypeVar("S", bound=Union[HTTPPollingSetup, WebSocketSetup])
HTTPPOLLING_SETUP = Union[HTTPPollingSetup, Callable[[], Awaitable[HTTPPollingSetup]]]
WEBSOCKET_SETUP = Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]


class Config(BaseSettings):
    """
    FastAPI 驱动框架设置，详情参考 FastAPI 文档
    """

    fastapi_openapi_url: Optional[str] = None
    """
    :类型:

      ``Optional[str]``

    :说明:

      ``openapi.json`` 地址，默认为 ``None`` 即关闭
    """
    fastapi_docs_url: Optional[str] = None
    """
    :类型:

      ``Optional[str]``

    :说明:

      ``swagger`` 地址，默认为 ``None`` 即关闭
    """
    fastapi_redoc_url: Optional[str] = None
    """
    :类型:

      ``Optional[str]``

    :说明:

      ``redoc`` 地址，默认为 ``None`` 即关闭
    """
    fastapi_reload: Optional[bool] = None
    """
    :类型:

      ``Optional[bool]``

    :说明:

      开启/关闭冷重载，默认会在配置了 app 的 debug 模式启用
    """
    fastapi_reload_dirs: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      重载监控文件夹列表，默认为 uvicorn 默认值
    """
    fastapi_reload_delay: Optional[float] = None
    """
    :类型:

      ``Optional[float]``

    :说明:

      重载延迟，默认为 uvicorn 默认值
    """
    fastapi_reload_includes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """
    fastapi_reload_excludes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """

    class Config:
        extra = "ignore"


class Driver(ReverseDriver):
    """
    FastAPI 驱动框架。包含反向 Server 功能。

    :上报地址:

      * ``/{adapter name}/``: HTTP POST 上报
      * ``/{adapter name}/http/``: HTTP POST 上报
      * ``/{adapter name}/ws``: WebSocket 上报
      * ``/{adapter name}/ws/``: WebSocket 上报
    """

    def __init__(self, env: Env, config: NoneBotConfig):
        super(Driver, self).__init__(env, config)

        self.fastapi_config: Config = Config(**config.dict())

        self._server_app = FastAPI(
            debug=config.debug,
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
        )

        self._server_app.post("/{adapter}/")(self._handle_http)
        self._server_app.post("/{adapter}/http")(self._handle_http)
        self._server_app.websocket("/{adapter}/ws")(self._handle_ws_reverse)
        self._server_app.websocket("/{adapter}/ws/")(self._handle_ws_reverse)

    @property
    @overrides(ReverseDriver)
    def type(self) -> str:
        """驱动名称: ``fastapi``"""
        return "fastapi"

    @property
    @overrides(ReverseDriver)
    def server_app(self) -> FastAPI:
        """``FastAPI APP`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def asgi(self) -> FastAPI:
        """``FastAPI APP`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def logger(self) -> logging.Logger:
        """fastapi 使用的 logger"""
        return logging.getLogger("fastapi")

    @overrides(ReverseDriver)
    def on_startup(self, func: Callable) -> Callable:
        """参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#startup-event>`_"""
        return self.server_app.on_event("startup")(func)

    @overrides(ReverseDriver)
    def on_shutdown(self, func: Callable) -> Callable:
        """参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#startup-event>`_"""
        return self.server_app.on_event("shutdown")(func)

    @overrides(ReverseDriver)
    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        app: Optional[str] = None,
        **kwargs,
    ):
        """使用 ``uvicorn`` 启动 FastAPI"""
        super().run(host, port, app, **kwargs)
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "nonebot.log.LoguruHandler",
                },
            },
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                },
            },
        }
        uvicorn.run(
            app or self.server_app,  # type: ignore
            host=host or str(self.config.host),
            port=port or self.config.port,
            reload=self.fastapi_config.fastapi_reload
            if self.fastapi_config.fastapi_reload is not None
            else (bool(app) and self.config.debug),
            reload_dirs=self.fastapi_config.fastapi_reload_dirs,
            reload_delay=self.fastapi_config.fastapi_reload_delay,
            reload_includes=self.fastapi_config.fastapi_reload_includes,
            reload_excludes=self.fastapi_config.fastapi_reload_excludes,
            debug=self.config.debug,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )

    async def _handle_http(self, adapter: str, request: Request):
        data = await request.body()

        if adapter not in self._adapters:
            logger.warning(
                f"Unknown adapter {adapter}. Please register the adapter before use."
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="adapter not found"
            )

        # 创建 Bot 对象
        BotClass = self._adapters[adapter]
        http_request = HTTPRequest(
            request.scope["http_version"],
            request.url.scheme,
            request.url.path,
            request.scope["query_string"],
            dict(request.headers),
            request.method,
            data,
        )
        x_self_id, response = await BotClass.check_permission(self, http_request)

        if not x_self_id:
            raise HTTPException(
                response and response.status or 401,
                response and response.body and response.body.decode("utf-8"),
            )

        if x_self_id in self._clients:
            logger.warning(
                "There's already a reverse websocket connection,"
                "so the event may be handled twice."
            )

        bot = BotClass(x_self_id, http_request)

        asyncio.create_task(bot.handle_message(data))
        return Response(response and response.body, response and response.status or 200)

    async def _handle_ws_reverse(self, adapter: str, websocket: FastAPIWebSocket):
        ws = WebSocket(
            websocket.scope.get("http_version", "1.1"),
            websocket.url.scheme,
            websocket.url.path,
            websocket.scope["query_string"],
            dict(websocket.headers),
            websocket,
        )

        if adapter not in self._adapters:
            logger.warning(
                f"Unknown adapter {adapter}. Please register the adapter before use."
            )
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Create Bot Object
        BotClass = self._adapters[adapter]
        self_id, _ = await BotClass.check_permission(self, ws)

        if not self_id:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if self_id in self._clients:
            logger.opt(colors=True).warning(
                "There's already a websocket connection, "
                f"<y>{escape_tag(adapter.upper())} Bot {escape_tag(self_id)}</y> ignored."
            )
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        bot = BotClass(self_id, ws)

        await ws.accept()
        logger.opt(colors=True).info(
            f"WebSocket Connection from <y>{escape_tag(adapter.upper())} "
            f"Bot {escape_tag(self_id)}</y> Accepted!"
        )

        self._bot_connect(bot)

        try:
            while not ws.closed:
                try:
                    data = await ws.receive()
                except WebSocketDisconnect:
                    logger.error("WebSocket disconnected by peer.")
                    break
                except Exception as e:
                    logger.opt(exception=e).error(
                        "Error when receiving data from websocket."
                    )
                    break

                asyncio.create_task(bot.handle_message(data.encode()))
        finally:
            self._bot_disconnect(bot)


class FullDriver(ForwardDriver, Driver):
    """
    完整的 FastAPI 驱动框架，包含正向 Client 支持和反向 Server 支持。

    :使用方法:

    .. code-block:: dotenv

        DRIVER=nonebot.drivers.fastapi:FullDriver
    """

    def __init__(self, env: Env, config: NoneBotConfig):
        super(FullDriver, self).__init__(env, config)

        self.http_pollings: List[HTTPPOLLING_SETUP] = []
        self.websockets: List[WEBSOCKET_SETUP] = []
        self.shutdown: asyncio.Event = asyncio.Event()
        self.connections: List[asyncio.Task] = []

        self.on_startup(self._run_forward)
        self.on_shutdown(self._shutdown_forward)

    @property
    @overrides(ForwardDriver)
    def type(self) -> str:
        """驱动名称: ``fastapi_full``"""
        return "fastapi_full"

    @overrides(ForwardDriver)
    def setup_http_polling(self, setup: HTTPPOLLING_SETUP) -> None:
        """
        :说明:

          注册一个 HTTP 轮询连接，如果传入一个函数，则该函数会在每次连接时被调用

        :参数:

          * ``setup: Union[HTTPPollingSetup, Callable[[], Awaitable[HTTPPollingSetup]]]``
        """
        self.http_pollings.append(setup)

    @overrides(ForwardDriver)
    def setup_websocket(self, setup: WEBSOCKET_SETUP) -> None:
        """
        :说明:

          注册一个 WebSocket 连接，如果传入一个函数，则该函数会在每次重连时被调用

        :参数:

          * ``setup: Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]``
        """
        self.websockets.append(setup)

    def _run_forward(self):
        for setup in self.http_pollings:
            self.connections.append(asyncio.create_task(self._http_loop(setup)))
        for setup in self.websockets:
            self.connections.append(asyncio.create_task(self._ws_loop(setup)))

    def _shutdown_forward(self):
        self.shutdown.set()
        for task in self.connections:
            if not task.done():
                task.cancel()

    async def _prepare_setup(
        self, setup: Union[S, Callable[[], Awaitable[S]]]
    ) -> Optional[S]:
        try:
            if callable(setup):
                return await setup()
            else:
                return setup
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error while parsing setup "
                f"{escape_tag(repr(setup))}.</bg #f8bbd0></r>"
            )
            return

    def _build_http_request(self, setup: HTTPPollingSetup) -> Optional[HTTPRequest]:
        url = httpx.URL(setup.url)
        if not url.netloc:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>Error parsing url {escape_tag(str(url))}</bg #f8bbd0></r>"
            )
            return
        return HTTPRequest(
            setup.http_version,
            url.scheme,
            url.path,
            url.query,
            setup.headers,
            setup.method,
            setup.body,
        )

    async def _http_loop(self, _setup: HTTPPOLLING_SETUP):

        http2: bool = False
        bot: Optional[Bot] = None
        request: Optional[HTTPRequest] = None
        client: Optional[httpx.AsyncClient] = None

        # FIXME: seperate const values from setup (self_id, adapter)
        # logger.opt(colors=True).info(
        #     f"Start http polling for <y>{escape_tag(_setup.adapter.upper())} "
        #     f"Bot {escape_tag(_setup.self_id)}</y>"
        # )

        try:
            while not self.shutdown.is_set():

                setup = await self._prepare_setup(_setup)
                if not setup:
                    await asyncio.sleep(3)
                    continue
                request = self._build_http_request(setup)
                if not request:
                    await asyncio.sleep(setup.poll_interval)
                    continue

                if not client:
                    client = httpx.AsyncClient(http2=setup.http_version == "2", follow_redirects=True)
                elif http2 != (setup.http_version == "2"):
                    await client.aclose()
                    client = httpx.AsyncClient(http2=setup.http_version == "2", follow_redirects=True)
                http2 = setup.http_version == "2"

                if not bot:
                    BotClass = self._adapters[setup.adapter]
                    bot = BotClass(setup.self_id, request)
                    self._bot_connect(bot)
                else:
                    bot.request = request

                logger.debug(
                    f"Bot {setup.self_id} from adapter {setup.adapter} request {setup.url}"
                )
                try:
                    response = await client.request(
                        request.method,
                        setup.url,
                        content=request.body,
                        headers=request.headers,
                        timeout=30.0,
                    )
                    response.raise_for_status()
                    data = response.read()
                    asyncio.create_task(bot.handle_message(data))
                except httpx.HTTPError as e:
                    logger.opt(colors=True, exception=e).error(
                        f"<r><bg #f8bbd0>Error occurred while requesting {escape_tag(setup.url)}. "
                        "Try to reconnect...</bg #f8bbd0></r>"
                    )

                await asyncio.sleep(setup.poll_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while http polling</bg #f8bbd0></r>"
            )
        finally:
            if bot:
                self._bot_disconnect(bot)
            if client:
                await client.aclose()

    async def _ws_loop(self, _setup: WEBSOCKET_SETUP):
        bot: Optional[Bot] = None

        try:
            while True:

                setup = await self._prepare_setup(_setup)
                if not setup:
                    await asyncio.sleep(3)
                    continue

                url = httpx.URL(setup.url)
                if not url.netloc:
                    logger.opt(colors=True).error(
                        f"<r><bg #f8bbd0>Error parsing url {escape_tag(str(url))}</bg #f8bbd0></r>"
                    )
                    return

                logger.debug(
                    f"Bot {setup.self_id} from adapter {setup.adapter} connecting to {url}"
                )
                try:
                    connection = Connect(setup.url, extra_headers=setup.headers)
                    async with connection as ws:
                        logger.opt(colors=True).info(
                            f"WebSocket Connection to <y>{escape_tag(setup.adapter.upper())} "
                            f"Bot {escape_tag(setup.self_id)}</y> succeeded!"
                        )
                        request = WebSocket(
                            "1.1", url.scheme, url.path, url.query, setup.headers, ws
                        )

                        BotClass = self._adapters[setup.adapter]
                        bot = BotClass(setup.self_id, request)
                        self._bot_connect(bot)
                        while not self.shutdown.is_set():
                            # use try except instead of "request.closed" because of queued message
                            try:
                                msg = await request.receive_bytes()
                                asyncio.create_task(bot.handle_message(msg))
                            except ConnectionClosed:
                                logger.opt(colors=True).error(
                                    "<r><bg #f8bbd0>WebSocket connection closed. "
                                    "Try to reconnect...</bg #f8bbd0></r>"
                                )
                                break
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        f"<r><bg #f8bbd0>Error while connecting to {url}. "
                        "Try to reconnect...</bg #f8bbd0></r>"
                    )
                finally:
                    if bot:
                        self._bot_disconnect(bot)
                    bot = None

                if not setup.reconnect:
                    logger.info(f"WebSocket reconnect disabled for bot {setup.self_id}")
                    break
                await asyncio.sleep(setup.reconnect_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while websocket loop</bg #f8bbd0></r>"
            )


@dataclass
class WebSocket(BaseWebSocket):
    websocket: Union[FastAPIWebSocket, WebSocketClientProtocol] = None  # type: ignore

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        if isinstance(self.websocket, FastAPIWebSocket):
            return (
                self.websocket.client_state == WebSocketState.DISCONNECTED
                or self.websocket.application_state == WebSocketState.DISCONNECTED
            )
        else:
            return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        if isinstance(self.websocket, FastAPIWebSocket):
            await self.websocket.accept()
        else:
            raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = status.WS_1000_NORMAL_CLOSURE):
        await self.websocket.close(code)

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        if isinstance(self.websocket, FastAPIWebSocket):
            return await self.websocket.receive_text()
        else:
            msg = await self.websocket.recv()
            return msg.decode("utf-8") if isinstance(msg, bytes) else msg

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        if isinstance(self.websocket, FastAPIWebSocket):
            return await self.websocket.receive_bytes()
        else:
            msg = await self.websocket.recv()
            return msg.encode("utf-8") if isinstance(msg, str) else msg

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        if isinstance(self.websocket, FastAPIWebSocket):
            await self.websocket.send({"type": "websocket.send", "text": data})
        else:
            await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        if isinstance(self.websocket, FastAPIWebSocket):
            await self.websocket.send({"type": "websocket.send", "bytes": data})
        else:
            await self.websocket.send(data)
