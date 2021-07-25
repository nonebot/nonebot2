"""
FastAPI 驱动适配
================

后端使用方法请参考: `FastAPI 文档`_

.. _FastAPI 文档:
    https://fastapi.tiangolo.com/
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import List, Dict, Union, Optional, Callable

import httpx
import uvicorn
from pydantic import BaseSettings
from fastapi.responses import Response
from websockets.exceptions import ConnectionClosed
from fastapi import status, Request, FastAPI, HTTPException
from websockets.legacy.client import Connect, WebSocketClientProtocol
from starlette.websockets import (WebSocketState, WebSocketDisconnect, WebSocket
                                  as FastAPIWebSocket)

from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.typing import overrides
from nonebot.config import Env, Config as NoneBotConfig
from nonebot.drivers import ReverseDriver, ForwardDriver
from nonebot.drivers import HTTPRequest, WebSocket as BaseWebSocket


@dataclass
class HTTPPollingSetup:
    adapter: str
    self_id: str
    url: str
    method: str
    body: bytes
    headers: Dict[str, str]
    http_version: str
    poll_interval: float


@dataclass
class WebSocketSetup:
    adapter: str
    self_id: str
    url: str
    headers: Dict[str, str]
    http_version: str
    reconnect_interval: float


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
    fastapi_reload_dirs: List[str] = []
    """
    :类型:

      ``List[str]``

    :说明:

      ``debug`` 模式下重载监控文件夹列表，默认为 uvicorn 默认值
    """

    class Config:
        extra = "ignore"


class Driver(ReverseDriver, ForwardDriver):
    """
    FastAPI 驱动框架

    :上报地址:

      * ``/{adapter name}/``: HTTP POST 上报
      * ``/{adapter name}/http/``: HTTP POST 上报
      * ``/{adapter name}/ws``: WebSocket 上报
      * ``/{adapter name}/ws/``: WebSocket 上报
    """

    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self.fastapi_config: Config = Config(**config.dict())
        self.http_pollings: List[HTTPPollingSetup] = []
        self.websockets: List[WebSocketSetup] = []
        self.shutdown: asyncio.Event = asyncio.Event()
        self.connections: List[asyncio.Task] = []

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

        self.on_startup(self._run_forward)
        self.on_shutdown(self._shutdown_forward)

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

    @overrides(ForwardDriver)
    def setup_http_polling(self,
                           adapter: str,
                           self_id: str,
                           url: str,
                           polling_interval: float = 3.,
                           method: str = "GET",
                           body: bytes = b"",
                           headers: Dict[str, str] = {},
                           http_version: str = "1.1") -> None:
        self.http_pollings.append(
            HTTPPollingSetup(adapter, self_id, url, method, body, headers,
                             http_version, polling_interval))

    @overrides(ForwardDriver)
    def setup_websocket(self,
                        adapter: str,
                        self_id: str,
                        url: str,
                        reconnect_interval: float = 3.,
                        headers: Dict[str, str] = {},
                        http_version: str = "1.1") -> None:
        self.websockets.append(
            WebSocketSetup(adapter, self_id, url, headers, http_version,
                           reconnect_interval))

    @overrides(ReverseDriver)
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            *,
            app: Optional[str] = None,
            **kwargs):
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
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": "INFO"
                },
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
            reload=bool(app) and self.config.debug,
            reload_dirs=self.fastapi_config.fastapi_reload_dirs or None,
            debug=self.config.debug,
            log_config=LOGGING_CONFIG,
            **kwargs)

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

    async def _handle_http(self, adapter: str, request: Request):
        data = await request.body()

        if adapter not in self._adapters:
            logger.warning(
                f"Unknown adapter {adapter}. Please register the adapter before use."
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="adapter not found")

        # 创建 Bot 对象
        BotClass = self._adapters[adapter]
        http_request = HTTPRequest(request.scope["http_version"],
                                   request.url.scheme, request.url.path,
                                   request.scope["query_string"],
                                   dict(request.headers), request.method, data)
        x_self_id, response = await BotClass.check_permission(
            self, http_request)

        if not x_self_id:
            raise HTTPException(
                response and response.status or 401, response and
                response.body and response.body.decode("utf-8"))

        if x_self_id in self._clients:
            logger.warning("There's already a reverse websocket connection,"
                           "so the event may be handled twice.")

        bot = BotClass(x_self_id, http_request)

        asyncio.create_task(bot.handle_message(data))
        return Response(response and response.body,
                        response and response.status or 200)

    async def _handle_ws_reverse(self, adapter: str,
                                 websocket: FastAPIWebSocket):
        ws = WebSocket(websocket.scope.get("http_version",
                                           "1.1"), websocket.url.scheme,
                       websocket.url.path, websocket.scope["query_string"],
                       dict(websocket.headers), websocket)

        if adapter not in self._adapters:
            logger.warning(
                f"Unknown adapter {adapter}. Please register the adapter before use."
            )
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Create Bot Object
        BotClass = self._adapters[adapter]
        x_self_id, _ = await BotClass.check_permission(self, ws)

        if not x_self_id:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if x_self_id in self._clients:
            logger.opt(colors=True).warning(
                "There's already a reverse websocket connection, "
                f"<y>{adapter.upper()} Bot {x_self_id}</y> ignored.")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        bot = BotClass(x_self_id, ws)

        await ws.accept()
        logger.opt(colors=True).info(
            f"WebSocket Connection from <y>{adapter.upper()} "
            f"Bot {x_self_id}</y> Accepted!")

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
                        "Error when receiving data from websocket.")
                    break

                asyncio.create_task(bot.handle_message(data.encode()))
        finally:
            self._bot_disconnect(bot)

    async def _http_loop(self, setup: HTTPPollingSetup):
        url = httpx.URL(setup.url)
        if not url.netloc:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>")
            return
        request = HTTPRequest(
            setup.http_version, url.scheme, url.path, url.query, {
                **setup.headers, "host": url.netloc.decode("ascii")
            }, setup.method, setup.body)

        BotClass = self._adapters[setup.adapter]
        bot = BotClass(setup.self_id, request)
        self._bot_connect(bot)
        logger.opt(colors=True).info(
            f"Start http polling for <y>{setup.adapter.upper()} "
            f"Bot {setup.self_id}</y>")

        headers = request.headers
        http2: bool = False
        if request.http_version == "2":
            http2 = True

        try:
            async with httpx.AsyncClient(headers=headers,
                                         timeout=30.,
                                         http2=http2) as session:
                while not self.shutdown.is_set():
                    logger.debug(
                        f"Bot {setup.self_id} from adapter {setup.adapter} request {url}"
                    )
                    try:
                        response = await session.request(request.method,
                                                         url,
                                                         content=request.body)
                        response.raise_for_status()
                        data = response.read()
                        asyncio.create_task(bot.handle_message(data))
                    except httpx.HTTPError as e:
                        logger.opt(colors=True, exception=e).error(
                            f"<r><bg #f8bbd0>Error occurred while requesting {url}. "
                            "Try to reconnect...</bg #f8bbd0></r>")

                    await asyncio.sleep(setup.poll_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while http polling</bg #f8bbd0></r>")
        finally:
            self._bot_disconnect(bot)

    async def _ws_loop(self, setup: WebSocketSetup):
        url = httpx.URL(setup.url)
        if not url.netloc:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>")
            return

        headers = {**setup.headers, "host": url.netloc.decode("ascii")}

        bot: Optional[Bot] = None
        try:
            while True:
                logger.debug(
                    f"Bot {setup.self_id} from adapter {setup.adapter} connecting to {url}"
                )
                try:
                    connection = Connect(setup.url)
                    async with connection as ws:
                        logger.opt(colors=True).info(
                            f"WebSocket Connection to <y>{setup.adapter.upper()} "
                            f"Bot {setup.self_id}</y> succeeded!")
                        request = WebSocket(setup.http_version, url.scheme,
                                            url.path, url.query, headers, ws)

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
                                    "<r><bg #f8bbd0>WebSocket connection closed by peer. "
                                    "Try to reconnect...</bg #f8bbd0></r>")
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        f"<r><bg #f8bbd0>Error while connecting to {url}. "
                        "Try to reconnect...</bg #f8bbd0></r>")
                finally:
                    if bot:
                        self._bot_disconnect(bot)
                    bot = None
                await asyncio.sleep(setup.reconnect_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while websocket loop</bg #f8bbd0></r>")


@dataclass
class WebSocket(BaseWebSocket):
    websocket: Union[FastAPIWebSocket,
                     WebSocketClientProtocol] = None  # type: ignore

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        if isinstance(self.websocket, FastAPIWebSocket):
            return (
                self.websocket.client_state == WebSocketState.DISCONNECTED or
                self.websocket.application_state == WebSocketState.DISCONNECTED)
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
