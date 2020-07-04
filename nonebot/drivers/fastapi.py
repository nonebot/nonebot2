#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from typing import Optional
from ipaddress import IPv4Address

import uvicorn
from fastapi import FastAPI

from . import BaseDriver


class Driver(BaseDriver):

    def __init__(self, config):
        self._server_app = FastAPI(
            debug=config.debug,
            openapi_url=None,
            docs_url=None,
            redoc_url=None,
        )

        self.config = config

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
