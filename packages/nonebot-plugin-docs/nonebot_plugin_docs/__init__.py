#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-11-22 00:56:58
@LastEditors    : yanyongyu
@LastEditTime   : 2020-11-22 01:00:29
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

import importlib

import nonebot
from nonebot.log import logger


def init():
    driver = nonebot.get_driver()
    try:
        _module = importlib.import_module(
            f"nonebot_plugin_docs.drivers.{driver.type}")
    except ImportError:
        logger.warning(f"Driver {driver.type} not supported")
        return
    register_route = getattr(_module, "register_route")
    register_route(driver)
    host = str(driver.config.host)
    port = driver.config.port
    if host in ["0.0.0.0", "127.0.0.1"]:
        host = "localhost"
    logger.opt(colors=True).info(f"Nonebot docs will be running at: "
                                 f"<b><u>http://{host}:{port}/docs/</u></b>")


init()
