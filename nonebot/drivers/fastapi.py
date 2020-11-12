"""
FastAPI 驱动适配
================

后端使用方法请参考: `FastAPI 文档`_

.. _FastAPI 文档:
    https://fastapi.tiangolo.com/
"""

import hmac
import json
import asyncio
import logging

import uvicorn
from fastapi.responses import Response
from fastapi import Body, status, Header, Request, FastAPI, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect, WebSocket as FastAPIWebSocket

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.utils import DataclassEncoder
from nonebot.exception import RequestDenied
from nonebot.drivers import BaseDriver, BaseWebSocket
from nonebot.typing import Optional, Callable, overrides


def get_auth_bearer(access_token: Optional[str] = Header(
    None, alias="Authorization")):
    if not access_token:
        return None
    scheme, _, param = access_token.partition(" ")
    if scheme.lower() not in ["bearer", "token"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    return param


class Driver(BaseDriver):
    """FastAPI 驱动框架"""

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)

        self._server_app = FastAPI(
            debug=config.debug,
            openapi_url=None,
            docs_url=None,
            redoc_url=None,
        )

        self._server_app.post("/{adapter}/")(self._handle_http)
        self._server_app.post("/{adapter}/http")(self._handle_http)
        self._server_app.websocket("/{adapter}/ws")(self._handle_ws_reverse)
        self._server_app.websocket("/{adapter}/ws/")(self._handle_ws_reverse)

    @property
    @overrides(BaseDriver)
    def type(self) -> str:
        """驱动名称: ``fastapi``"""
        return "fastapi"

    @property
    @overrides(BaseDriver)
    def server_app(self) -> FastAPI:
        """``FastAPI APP`` 对象"""
        return self._server_app

    @property
    @overrides(BaseDriver)
    def asgi(self):
        """``FastAPI APP`` 对象"""
        return self._server_app

    @property
    @overrides(BaseDriver)
    def logger(self) -> logging.Logger:
        """fastapi 使用的 logger"""
        return logging.getLogger("fastapi")

    @overrides(BaseDriver)
    def on_startup(self, func: Callable) -> Callable:
        """参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#startup-event>`_"""
        return self.server_app.on_event("startup")(func)

    @overrides(BaseDriver)
    def on_shutdown(self, func: Callable) -> Callable:
        """参考文档: `Events <https://fastapi.tiangolo.com/advanced/events/#startup-event>`_"""
        return self.server_app.on_event("shutdown")(func)

    @overrides(BaseDriver)
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            *,
            app: Optional[str] = None,
            **kwargs):
        """使用 ``uvicorn`` 启动 FastAPI"""
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
        uvicorn.run(app or self.server_app,
                    host=host or str(self.config.host),
                    port=port or self.config.port,
                    reload=bool(app) and self.config.debug,
                    debug=self.config.debug,
                    log_config=LOGGING_CONFIG,
                    **kwargs)

    @overrides(BaseDriver)
    async def _handle_http(self,
                           adapter: str,
                           request: Request,
                           data: dict = Body(...)):
        if not isinstance(data, dict):
            logger.warning("Data received is invalid")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if adapter not in self._adapters:
            logger.warning("Unknown adapter")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="adapter not found")

        # 创建 Bot 对象
        BotClass = self._adapters[adapter]
        headers = dict(request.headers)
        try:
            x_self_id = await BotClass.check_permission(self, "http", headers,
                                                        data)
        except RequestDenied as e:
            raise HTTPException(status_code=e.status_code,
                                detail=e.reason) from None

        if x_self_id in self._clients:
            logger.warning("There's already a reverse websocket connection,"
                           "so the event may be handled twice.")

        bot = BotClass(self, "http", self.config, x_self_id)

        asyncio.create_task(bot.handle_message(data))
        return Response("", 204)

    @overrides(BaseDriver)
    async def _handle_ws_reverse(self, adapter: str,
                                 websocket: FastAPIWebSocket):
        ws = WebSocket(websocket)

        if adapter not in self._adapters:
            logger.warning("Unknown adapter")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Create Bot Object
        BotClass = self._adapters[adapter]
        headers = dict(websocket.headers)
        try:
            x_self_id = await BotClass.check_permission(self, "websocket",
                                                        headers, None)
        except RequestDenied:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if x_self_id in self._clients:
            logger.warning("There's already a reverse websocket connection, "
                           f"<y>{adapter.upper()} Bot {x_self_id}</y> ignored.")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)

        bot = BotClass(self, "websocket", self.config, x_self_id, websocket=ws)

        await ws.accept()
        self._clients[x_self_id] = bot
        logger.opt(colors=True).info(
            f"WebSocket Connection from <y>{adapter.upper()} "
            f"Bot {x_self_id}</y> Accepted!")

        try:
            while not ws.closed:
                data = await ws.receive()

                if not data:
                    continue

                asyncio.create_task(bot.handle_message(data))
        finally:
            del self._clients[x_self_id]


class WebSocket(BaseWebSocket):

    def __init__(self, websocket: FastAPIWebSocket):
        super().__init__(websocket)
        self._closed = None

    @property
    @overrides(BaseWebSocket)
    def closed(self):
        return self._closed

    @overrides(BaseWebSocket)
    async def accept(self):
        await self.websocket.accept()
        self._closed = False

    @overrides(BaseWebSocket)
    async def close(self, code: int = status.WS_1000_NORMAL_CLOSURE):
        await self.websocket.close(code=code)
        self._closed = True

    @overrides(BaseWebSocket)
    async def receive(self) -> Optional[dict]:
        data = None
        try:
            data = await self.websocket.receive_json()
            if not isinstance(data, dict):
                data = None
                raise ValueError
        except ValueError:
            logger.warning("Received an invalid json message.")
        except WebSocketDisconnect:
            self._closed = True
            logger.error("WebSocket disconnected by peer.")

        return data

    @overrides(BaseWebSocket)
    async def send(self, data: dict) -> None:
        text = json.dumps(data, cls=DataclassEncoder)
        await self.websocket.send({"type": "websocket.send", "text": text})
