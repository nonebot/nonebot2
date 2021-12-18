"""
FastAPI 驱动适配
================

本驱动同时支持服务端以及客户端连接

后端使用方法请参考: `FastAPI 文档`_

.. _FastAPI 文档:
    https://fastapi.tiangolo.com/
"""

import logging
from functools import partial
from dataclasses import dataclass
from typing import Any, List, Union, Callable, Optional, Awaitable

import httpx
import uvicorn
from pydantic import BaseSettings
from fastapi.responses import Response
from fastapi import FastAPI, Request, status
from starlette.websockets import WebSocket, WebSocketState
from websockets.legacy.client import Connect, WebSocketClientProtocol

from nonebot.config import Env
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.config import Config as NoneBotConfig
from nonebot.drivers import Request as GenericRequest
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import Response as GenericResponse
from nonebot.drivers import (
    HTTPVersion,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)


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
    """FastAPI 驱动框架。包含反向 Server 功能。"""

    def __init__(self, env: Env, config: NoneBotConfig):
        super(Driver, self).__init__(env, config)

        self.fastapi_config: Config = Config(**config.dict())

        self._server_app = FastAPI(
            debug=config.debug,
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
        )

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
    def setup_http_server(self, setup: HTTPServerSetup):
        async def _handle(request: Request) -> Response:
            return await self._handle_http(request, setup)

        self._server_app.add_api_route(
            setup.path.path,
            _handle,
            methods=[setup.method],
        )

    @overrides(ReverseDriver)
    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        async def _handle(websocket: WebSocket):
            await self._handle_ws(websocket, setup)

        self._server_app.add_api_websocket_route(
            setup.path.path,
            _handle,
        )

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

    async def _handle_http(
        self,
        request: Request,
        setup: HTTPServerSetup,
    ):
        http_request = GenericRequest(
            request.method,
            str(request.url),
            headers=request.headers.items(),
            cookies=request.cookies,
            content=await request.body(),
            version=request.scope["http_version"],
        )

        response = await setup.handle_func(http_request)
        return Response(response.content, response.status_code, dict(response.headers))

    async def _handle_ws(self, websocket: WebSocket, setup: WebSocketServerSetup):
        request = GenericRequest(
            "GET",
            str(websocket.url),
            headers=websocket.headers.items(),
            cookies=websocket.cookies,
            version=websocket.scope["http_version"],
        )
        ws = FastAPIWebSocket(
            request=request,
            websocket=websocket,
        )

        await setup.handle_func(ws)


class FullDriver(ForwardDriver, Driver):
    """
    完整的 FastAPI 驱动框架，包含正向 Client 支持和反向 Server 支持。

    :使用方法:

    .. code-block:: dotenv

        DRIVER=nonebot.drivers.fastapi:FullDriver
    """

    @property
    @overrides(Driver)
    def type(self) -> str:
        """驱动名称: ``fastapi_full``"""
        return "fastapi_full"

    @overrides(ForwardDriver)
    async def request(self, setup: "GenericRequest") -> Any:
        async with httpx.AsyncClient(
            http2=setup.version == HTTPVersion.H2, follow_redirects=True
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,
                headers=tuple(setup.headers.items()),
                timeout=30.0,
            )
            return GenericResponse(
                response.status_code,
                headers=response.headers,
                content=response.content,
                request=setup,
            )

    @overrides(ForwardDriver)
    async def websocket(self, setup: "GenericRequest") -> Any:
        ws = await Connect(str(setup.url), extra_headers=setup.headers.items())
        return WebSocketsWS(request=setup, websocket=ws)


class WebSocketsWS(BaseWebSocket):
    @overrides(BaseWebSocket)
    def __init__(self, *, request: GenericRequest, websocket: WebSocketClientProtocol):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        # if isinstance(self.websocket, WebSocket):
        #     return (
        #         self.websocket.client_state == WebSocketState.DISCONNECTED
        #         or self.websocket.application_state == WebSocketState.DISCONNECTED
        #     )
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        # if isinstance(self.websocket, WebSocket):
        #     await self.websocket.accept()
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000):
        await self.websocket.close(code)

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        # if isinstance(self.websocket, WebSocket):
        #     return await self.websocket.receive_text()
        msg = await self.websocket.recv()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        # if isinstance(self.websocket, WebSocket):
        #     return await self.websocket.receive_bytes()
        msg = await self.websocket.recv()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        # if isinstance(self.websocket, WebSocket):
        # await self.websocket.send({"type": "websocket.send", "text": data})
        await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        # if isinstance(self.websocket, WebSocket):
        #     await self.websocket.send({"type": "websocket.send", "bytes": data})
        await self.websocket.send(data)


class FastAPIWebSocket(BaseWebSocket):
    @overrides(BaseWebSocket)
    def __init__(self, *, request: GenericRequest, websocket: WebSocket):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return (
            self.websocket.client_state == WebSocketState.DISCONNECTED
            or self.websocket.application_state == WebSocketState.DISCONNECTED
        )

    @overrides(BaseWebSocket)
    async def accept(self):
        await self.websocket.accept()

    @overrides(BaseWebSocket)
    async def close(self, code: int = status.WS_1000_NORMAL_CLOSURE):
        await self.websocket.close(code)

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        return await self.websocket.receive_text()

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        await self.websocket.send({"type": "websocket.send", "text": data})

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send({"type": "websocket.send", "bytes": data})
