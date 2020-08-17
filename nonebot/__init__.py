#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
from ipaddress import IPv4Address
from nonebot.typing import Type, Union, Driver, Optional, NoReturn

_driver: Optional[Driver] = None


def get_driver() -> Union[NoReturn, Driver]:
    if _driver is None:
        raise ValueError("NoneBot has not been initialized.")
    return _driver


def get_app():
    driver = get_driver()
    return driver.server_app


def get_asgi():
    driver = get_driver()
    return driver.asgi


def get_bots():
    driver = get_driver()
    return driver.bots


from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.adapters.cqhttp import Bot as CQBot

try:
    import nonebot_test
except ImportError:
    nonebot_test = None


def init(*, _env_file: Optional[str] = None, **kwargs):
    global _driver
    env = Env()
    config = Config(**kwargs, _env_file=_env_file or f".env.{env.environment}")

    logger.setLevel(logging.DEBUG if config.debug else logging.INFO)
    logger.debug(f"Loaded config: {config.dict()}")

    DriverClass: Type[Driver] = getattr(importlib.import_module(config.driver),
                                        "Driver")
    _driver = DriverClass(env, config)

    # register build-in adapters
    _driver.register_adapter("cqhttp", CQBot)

    # load nonebot test frontend if debug
    if config.debug and nonebot_test:
        logger.debug("Loading nonebot test frontend...")
        nonebot_test.init()


def run(host: Optional[IPv4Address] = None,
        port: Optional[int] = None,
        *args,
        **kwargs):
    get_driver().run(host, port, *args, **kwargs)


from nonebot.plugin import load_plugins, get_loaded_plugins
