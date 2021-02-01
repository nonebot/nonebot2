"""
Mirai-API-HTTP 协议适配
============================

协议详情请看: `mirai-api-http 文档`_ 

\:\:\: tip
该Adapter目前仍然处在早期实验性阶段, 并未经过充分测试

如果你在使用过程中遇到了任何问题, 请前往 `Issue页面`_ 为我们提供反馈
\:\:\:

.. _mirai-api-http 文档:
    https://github.com/project-mirai/mirai-api-http/tree/master/docs

.. _Issue页面:
    https://github.com/nonebot/nonebot2/issues

"""

from .bot import Bot
from .bot_ws import WebsocketBot
from .event import *
from .message import MessageChain, MessageSegment
