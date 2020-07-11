#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import nonebot
from nonebot.matcher import matchers

nonebot.init()
app = nonebot.get_asgi()

nonebot.load_plugins("test_plugins")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
