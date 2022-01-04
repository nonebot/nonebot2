"""
FastAPI 驱动适配
================

本驱动同时支持服务端以及客户端连接

后端使用方法请参考: `FastAPI 文档`_

.. _FastAPI 文档:
    https://fastapi.tiangolo.com/
"""

import logging
from functools import wraps
from typing import Any, List, Tuple, Callable, Optional

import uvicorn
from pydantic import BaseSettings
from fastapi.responses import Response
from fastapi import FastAPI, Request, UploadFile, status
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from ._model import FileTypes
from nonebot.config import Env
from nonebot.typing import overrides
from nonebot.exception import WebSocketClosed
from nonebot.config import Config as NoneBotConfig
from nonebot.drivers import Request as BaseRequest
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import ReverseDriver, HTTPServerSetup, WebSocketServerSetup


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except WebSocketDisconnect as e:
            raise WebSocketClosed(e.code)

    return decorator


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
    fastapi_reload: bool = False
    """
    :类型:

      ``bool``

    :说明:

      开启/关闭冷重载
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
            name=setup.name,
            methods=[setup.method],
        )

    @overrides(ReverseDriver)
    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        async def _handle(websocket: WebSocket) -> None:
            await self._handle_ws(websocket, setup)

        self._server_app.add_api_websocket_route(
            setup.path.path,
            _handle,
            name=setup.name,
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
            reload=self.fastapi_config.fastapi_reload,
            reload_dirs=self.fastapi_config.fastapi_reload_dirs,
            reload_delay=self.fastapi_config.fastapi_reload_delay,
            reload_includes=self.fastapi_config.fastapi_reload_includes,
            reload_excludes=self.fastapi_config.fastapi_reload_excludes,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )

    async def _handle_http(
        self,
        request: Request,
        setup: HTTPServerSetup,
    ) -> Response:
        json: Any = None
        try:
            json = await request.json()
        except Exception:
            pass

        data: Optional[dict] = None
        files: Optional[List[Tuple[str, FileTypes]]] = None
        try:
            form = await request.form()
            data = {}
            files = []
            for key, value in form.multi_items():
                if isinstance(value, UploadFile):
                    files.append(
                        (key, (value.filename, value.file, value.content_type))
                    )
                else:
                    data[key] = value
        except Exception:
            pass
        http_request = BaseRequest(
            request.method,
            str(request.url),
            headers=request.headers.items(),
            cookies=request.cookies,
            content=await request.body(),
            data=data,
            json=json,
            files=files,
            version=request.scope["http_version"],
        )

        response = await setup.handle_func(http_request)
        return Response(response.content, response.status_code, dict(response.headers))

    async def _handle_ws(self, websocket: WebSocket, setup: WebSocketServerSetup):
        request = BaseRequest(
            "GET",
            str(websocket.url),
            headers=websocket.headers.items(),
            cookies=websocket.cookies,
            version=websocket.scope.get("http_version", "1.1"),
        )
        ws = FastAPIWebSocket(
            request=request,
            websocket=websocket,
        )

        await setup.handle_func(ws)


class FastAPIWebSocket(BaseWebSocket):
    @overrides(BaseWebSocket)
    def __init__(self, *, request: BaseRequest, websocket: WebSocket):
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
    async def accept(self) -> None:
        await self.websocket.accept()

    @overrides(BaseWebSocket)
    async def close(
        self, code: int = status.WS_1000_NORMAL_CLOSURE, reason: str = ""
    ) -> None:
        await self.websocket.close(code)

    @overrides(BaseWebSocket)
    @catch_closed
    async def receive(self) -> str:
        return await self.websocket.receive_text()

    @overrides(BaseWebSocket)
    @catch_closed
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        await self.websocket.send({"type": "websocket.send", "text": data})

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send({"type": "websocket.send", "bytes": data})
