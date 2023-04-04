"""本模块定义了协议适配基类，各协议请继承以下基类。

使用 {ref}`nonebot.drivers.Driver.register_adapter` 注册适配器。

FrontMatter:
    sidebar_position: 0
    description: nonebot.adapters 模块
"""

from nonebot.internal.adapter import Bot as Bot
from nonebot.internal.adapter import Event as Event
from nonebot.internal.adapter import Adapter as Adapter
from nonebot.internal.adapter import Message as Message
from nonebot.internal.adapter import MessageSegment as MessageSegment
from nonebot.internal.adapter import MessageTemplate as MessageTemplate

__autodoc__ = {
    "Bot": True,
    "Event": True,
    "Adapter": True,
    "Message": True,
    "Message.__getitem__": True,
    "Message.__contains__": True,
    "Message._construct": True,
    "MessageSegment": True,
    "MessageSegment.__str__": True,
    "MessageSegment.__add__": True,
    "MessageTemplate": True,
}
