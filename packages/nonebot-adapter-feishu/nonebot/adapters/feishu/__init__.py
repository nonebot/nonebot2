import logging

from nonebot.log import LoguruHandler, logger

aiocache_logger = logging.getLogger("aiocache.serializers.serializers")
aiocache_logger.setLevel(logging.DEBUG)
aiocache_logger.handlers.clear()
aiocache_logger.addHandler(LoguruHandler())

from .bot import Bot
from .event import *
from .event import Event
from .message import Message, MessageSegment
