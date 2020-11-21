#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-11-22 00:56:31
@LastEditors    : yanyongyu
@LastEditTime   : 2020-11-22 01:03:05
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from pathlib import Path

from nonebot.drivers.fastapi import Driver
from fastapi.staticfiles import StaticFiles


def register_route(driver: Driver, socketio):
    app = driver.server_app

    static_path = str((Path(__file__).parent / ".." / "dist").resolve())

    app.mount("/docs",
              StaticFiles(directory=static_path, html=True),
              name="docs")
