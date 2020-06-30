#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import nonebot
from nonebot.matcher import matchers

if __name__ == "__main__":
    nonebot.load_plugins(os.path.join(os.path.dirname(__file__),
                                      "test_plugins"))
    print(nonebot.get_loaded_plugins())
    print(matchers)
    print(matchers[1][0].handlers)
