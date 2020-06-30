#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .log import logger

logger.setLevel(level=logging.DEBUG)

from .plugin import load_plugins, get_loaded_plugins
