"""
Provide logger object.

Any other modules in "nonebot" should use "logger" from this module
to log messages.
"""

import logging
import sys

logger = logging.getLogger('nonebot')
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s %(name)s] %(levelname)s: %(message)s'
))
logger.addHandler(default_handler)
