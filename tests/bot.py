#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import nonebot
from nonebot.log import logger, default_format

# test custom log
logger.add("error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

nonebot.init(custom_config2="config on init")
app = nonebot.get_asgi()

# load builtin plugin
nonebot.load_builtin_plugins()

# load local plugins
nonebot.load_plugins("test_plugins")

# modify some config / config depends on loaded configs
config = nonebot.get_driver().config
config.custom_config3 = config.custom_config1

if __name__ == "__main__":
    nonebot.run(app="bot:app")
