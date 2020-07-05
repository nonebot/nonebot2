#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from typing import Optional
from ipaddress import IPv4Address

import uvicorn
from fastapi import Body, FastAPI, WebSocket

from nonebot.log import logger
from nonebot.drivers import BaseDriver


class Driver(BaseDriver):

    def __init__(self, config):
        self._server_app = FastAPI(
            debug=config.debug,
            openapi_url=None,
            docs_url=None,
            redoc_url=None,
        )

        self.config = config

        self._server_app.post("/coolq/")(self._handle_http)
        self._server_app.websocket("/coolq/ws")(self._handle_ws_reverse)

    @property
    def server_app(self):
        return self._server_app

    @property
    def asgi(self):
        return self._server_app

    @property
    def logger(self):
        return logging.getLogger("fastapi")

    def run(self,
            host: Optional[IPv4Address] = None,
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
                    host=host or str(self.config.host),
                    port=port or self.config.port,
                    reload=app and self.config.debug,
                    debug=self.config.debug,
                    log_config=LOGGING_CONFIG,
                    **kwargs)

    async def _handle_http(self, data: dict = Body(...)):
        logger.debug(f"Received message: {data}")
        return {"status": 200, "message": "success"}

    async def _handle_ws_reverse(self, websocket: WebSocket):
        await websocket.accept()
        while True:
            try:
                data = await websocket.receive_json()
            except json.decoder.JSONDecodeError as e:
                logger.exception(e)
                continue

            logger.debug(f"Received message: {data}")
