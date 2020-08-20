#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志
====

NoneBot 使用标准库 `logging`_ 来记录日志信息。

自定义 logger 请参考 `logging`_ 文档。

.. _logging:
    https://docs.python.org/3/library/logging.html
"""

import sys
import logging

logger = logging.getLogger("nonebot")
"""
:说明:

  NoneBot 日志记录器对象。

:默认信息:

  * 格式: ``[%(asctime)s %(name)s] %(levelname)s: %(message)s``
  * 等级: ``DEBUG`` / ``INFO`` ，根据 config 配置改变
  * 输出: 输出至 stdout

:用法:

.. code-block:: python

    from nonebot.log import logger

    # 也可以这样
    import logging
    logger = logging.getLogger("nonebot")
"""

default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
logger.addHandler(default_handler)
