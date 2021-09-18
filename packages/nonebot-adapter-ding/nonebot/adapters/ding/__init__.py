"""
钉钉群机器人 协议适配
============================

协议详情请看: `钉钉文档`_

.. _钉钉文档:
    https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p
"""

from .bot import Bot as Bot
from .utils import log as log
from .event import Event as Event
from .message import Message as Message
from .event import MessageEvent as MessageEvent
from .exception import ActionFailed as ActionFailed
from .exception import NetworkError as NetworkError
from .message import MessageSegment as MessageSegment
from .exception import SessionExpired as SessionExpired
from .event import GroupMessageEvent as GroupMessageEvent
from .exception import ApiNotAvailable as ApiNotAvailable
from .event import PrivateMessageEvent as PrivateMessageEvent
from .exception import DingAdapterException as DingAdapterException
