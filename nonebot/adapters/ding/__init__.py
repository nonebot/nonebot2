"""
钉钉群机器人 协议适配
============================

协议详情请看: `钉钉文档`_

.. _钉钉文档:
    https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p
"""

from .utils import log
from .bot import Bot
from .message import Message, MessageSegment
from .event import Event, MessageEvent, PrivateMessageEvent, GroupMessageEvent
from .exception import (DingAdapterException, ApiNotAvailable, NetworkError,
                        ActionFailed, SessionExpired)
