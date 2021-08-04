r"""
Mirai-API-HTTP 协议适配
============================

协议详情请看: `mirai-api-http 文档`_

\:\:\: tip
该Adapter目前仍然处在早期实验性阶段, 并未经过充分测试

如果你在使用过程中遇到了任何问题, 请前往 `Issue页面`_ 为我们提供反馈
\:\:\:

\:\:\: danger
Mirai-API-HTTP 的适配器以 `AGPLv3许可`_ 单独开源

这意味着在使用该适配器时需要 **以该许可开源您的完整程序代码**
\:\:\:

.. _mirai-api-http 文档:
    https://github.com/project-mirai/mirai-api-http/tree/master/docs

.. _Issue页面:
    https://github.com/nonebot/nonebot2/issues

.. _AGPLv3许可:
    https://opensource.org/licenses/AGPL-3.0

"""

from .bot import Bot
from .event import *
from .message import MessageChain, MessageSegment

WebsocketBot = Bot
"""
``WebsocketBot``现在已经和``Bot``合并, 并已经被弃用, 请直接使用``Bot``
"""
