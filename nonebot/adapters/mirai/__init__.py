"""
Mirai-API-HTTP 协议适配
============================

协议详情请看: `mirai-api-http 文档`_ 

.. mirai-api-http 文档:
    https://github.com/project-mirai/mirai-api-http/tree/master/docs
"""

from .bot import MiraiBot
from .bot_ws import MiraiWebsocketBot
from .event import *
from .message import MessageChain, MessageSegment
