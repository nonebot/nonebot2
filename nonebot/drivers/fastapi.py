#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hmac
import json
import asyncio
import logging

import uvicorn
from fastapi.responses import Response
from fastapi import Body, status, Header, FastAPI, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect, WebSocket as FastAPIWebSocket

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.utils import DataclassEncoder
from nonebot.drivers import BaseDriver, BaseWebSocket
from nonebot.typing import Optional, Callable, overrides


def get_auth_bearer(access_token: Optional[str] = Header(
    None, alias="Authorization")):
    if not access_token:
        return None
    scheme, _, param = access_token.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    return param


class Driver(BaseDriver):

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
        return "fastapi"

    @property
    @overrides(BaseDriver)
    def server_app(self) -> FastAPI:
        return self._server_app

    @property
    @overrides(BaseDriver)
    def asgi(self):
        return self._server_app

    @property
    @overrides(BaseDriver)
    def logger(self) -> logging.Logger:
        return logging.getLogger("fastapi")

    @overrides(BaseDriver)
    def on_startup(self, func: Callable) -> Callable:
        return self.server_app.on_event("startup")(func)

    @overrides(BaseDriver)
    def on_shutdown(self, func: Callable) -> Callable:
        return self.server_app.on_event("shutdown")(func)

    @overrides(BaseDriver)
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            *,
            app: Optional[str] = None,
            **kwargs):
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
                           data: dict = Body(...),
                           x_self_id: Optional[str] = Header(None),
                           x_signature: Optional[str] = Header(None),
                           auth: Optional[str] = Depends(get_auth_bearer)):
        # 检查self_id
        if not x_self_id:
            logger.warning("Missing X-Self-ID Header")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Missing X-Self-ID Header")

        # 检查签名
        secret = self.config.secret
        if secret:
            if not x_signature:
                logger.warning("Missing Signature Header")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Missing Signature")
            sig = hmac.new(secret.encode("utf-8"),
                           json.dumps(data).encode(), "sha1").hexdigest()
            if x_signature != "sha1=" + sig:
                logger.warning("Signature Header is invalid")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Signature is invalid")

        access_token = self.config.access_token
        if access_token and access_token != auth:
            logger.warning("Authorization Header is invalid"
                           if auth else "Missing Authorization Header")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Authorization Header is invalid"
                                if auth else "Missing Authorization Header")

        if not isinstance(data, dict):
            logger.warning("Data received is invalid")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if x_self_id in self._clients:
            logger.warning("There's already a reverse websocket api connection,"
                           "so the event may be handled twice.")

        # 创建 Bot 对象
        if adapter in self._adapters:
            BotClass = self._adapters[adapter]
            bot = BotClass(self, "http", self.config, x_self_id)
        else:
            logger.warning("Unknown adapter")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="adapter not found")

        asyncio.create_task(bot.handle_message(data))
        return Response("", 204)

    @overrides(BaseDriver)
    async def _handle_ws_reverse(
        self,
        adapter: str,
        websocket: FastAPIWebSocket,
        x_self_id: str = Header(None),
        auth: Optional[str] = Depends(get_auth_bearer)):
        ws = WebSocket(websocket)

        access_token = self.config.access_token
        if access_token and access_token != auth:
            logger.warning("Authorization Header is invalid"
                           if auth else "Missing Authorization Header")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if not x_self_id:
            logger.warning(f"Missing X-Self-ID Header")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if x_self_id in self._clients:
            logger.warning(f"Connection Conflict: self_id {x_self_id}")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Create Bot Object
        if adapter in self._adapters:
            BotClass = self._adapters[adapter]
            bot = BotClass(self,
                           "websocket",
                           self.config,
                           x_self_id,
                           websocket=ws)
        else:
            logger.warning("Unknown adapter")
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

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
