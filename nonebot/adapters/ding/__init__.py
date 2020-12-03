"""
钉钉群机器人 协议适配
============================

协议详情请看: `钉钉文档`_

.. _钉钉文档:
    https://ding-doc.dingtalk.com/doc#/serverapi2/krgddi

"""

from .utils import log
from .bot import Bot
from .event import Event
from .message import Message, MessageSegment
from .exception import (DingAdapterException, ApiNotAvailable, NetworkError,
                        ActionFailed, SessionExpired)
