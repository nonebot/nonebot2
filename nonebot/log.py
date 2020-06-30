#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

logger = logging.getLogger("nonebot")
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
logger.addHandler(default_handler)
