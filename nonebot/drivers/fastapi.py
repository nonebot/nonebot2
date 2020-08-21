#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging

import uvicorn
from fastapi import Body, status, Header, FastAPI, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect, WebSocket as FastAPIWebSocket

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.utils import DataclassEncoder
from nonebot.adapters.cqhttp import Bot as CQBot
from nonebot.drivers import BaseDriver, BaseWebSocket
from nonebot.typing import Union, Optional, Callable, overrides


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
            "formatters": {
                "default": {
                    "()": "logging.Formatter",
                    "fmt": "[%(asctime)s %(name)s] %(levelname)s: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
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
                    host=str(host) or str(self.config.host),
                    port=port or self.config.port,
                    reload=app and self.config.debug,
                    debug=self.config.debug,
                    log_config=LOGGING_CONFIG,
                    **kwargs)

    @overrides(BaseDriver)
    async def _handle_http(
        self,
        adapter: str,
        data: dict = Body(...),
        x_self_id: str = Header(None),
        access_token: Optional[str] = Depends(get_auth_bearer)):
        secret = self.config.secret
        if secret is not None and secret != access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authenticated",
                                headers={"WWW-Authenticate": "Bearer"})

        # Create Bot Object
        if adapter in self._adapters:
            BotClass = self._adapters[adapter]
            bot = BotClass(self, "http", self.config, x_self_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="adapter not found")

        await bot.handle_message(data)
        return {"status": 200, "message": "success"}

    @overrides(BaseDriver)
    async def _handle_ws_reverse(
        self,
        adapter: str,
        websocket: FastAPIWebSocket,
        x_self_id: str = Header(None),
        access_token: Optional[str] = Depends(get_auth_bearer)):
        secret = self.config.secret
        if secret is not None and secret != access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authenticated",
                                headers={"WWW-Authenticate": "Bearer"})

        websocket = WebSocket(websocket)

        if not x_self_id:
            logger.error(f"Error Connection Unkown: self_id {x_self_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        if x_self_id in self._clients:
            logger.error(f"Error Connection Conflict: self_id {x_self_id}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        # Create Bot Object
        if adapter in self._adapters:
            BotClass = self._adapters[adapter]
            bot = BotClass(self,
                           "websocket",
                           self.config,
                           x_self_id,
                           websocket=websocket)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="adapter not found")

        await websocket.accept()
        self._clients[x_self_id] = bot

        try:
            while not websocket.closed:
                data = await websocket.receive()

                if not data:
                    continue

                await bot.handle_message(data)
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
        except ValueError:
            logger.debug("Received an invalid json message.")
        except WebSocketDisconnect:
            self._closed = True
            logger.error("WebSocket disconnected by peer.")

        return data

    @overrides(BaseWebSocket)
    async def send(self, data: dict) -> None:
        text = json.dumps(data, cls=DataclassEncoder)
        await self.websocket.send({"type": "websocket.send", "text": text})
