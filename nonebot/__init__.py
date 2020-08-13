#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
from ipaddress import IPv4Address

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.drivers import BaseDriver
from nonebot.adapters.cqhttp import Bot as CQBot
from nonebot.typing import Union, Optional, NoReturn

_driver: Optional[BaseDriver] = None


def get_driver() -> Union[NoReturn, BaseDriver]:
    if _driver is None:
        raise ValueError("NoneBot has not been initialized.")
    return _driver


def get_app():
    driver = get_driver()
    return driver.server_app


def get_asgi():
    driver = get_driver()
    return driver.asgi


def init(*, _env_file: Optional[str] = None, **kwargs):
    global _driver
    env = Env()
    config = Config(**kwargs, _env_file=_env_file or f".env.{env.environment}")

    logger.setLevel(logging.DEBUG if config.debug else logging.INFO)
    logger.debug(f"Loaded config: {config.dict()}")

    Driver = getattr(importlib.import_module(config.driver), "Driver")
    _driver = Driver(env, config)

    _driver.register_adapter("cqhttp", CQBot)


def run(host: Optional[IPv4Address] = None,
        port: Optional[int] = None,
        *args,
        **kwargs):
    get_driver().run(host, port, *args, **kwargs)


from nonebot.plugin import load_plugins, get_loaded_plugins
