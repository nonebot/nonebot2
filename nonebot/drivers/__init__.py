"""本模块定义了驱动适配器基类。

各驱动请继承以下基类。

FrontMatter:
    sidebar_position: 0
    description: nonebot.drivers 模块
"""

from nonebot.internal.model import URL as URL
from nonebot.internal.driver import Driver as Driver
from nonebot.internal.model import Cookies as Cookies
from nonebot.internal.model import Request as Request
from nonebot.internal.model import Response as Response
from nonebot.internal.model import WebSocket as WebSocket
from nonebot.internal.model import HTTPVersion as HTTPVersion
from nonebot.internal.driver import ForwardMixin as ForwardMixin
from nonebot.internal.driver import ForwardDriver as ForwardDriver
from nonebot.internal.driver import ReverseDriver as ReverseDriver
from nonebot.internal.driver import combine_driver as combine_driver
from nonebot.internal.model import HTTPServerSetup as HTTPServerSetup
from nonebot.internal.model import WebSocketServerSetup as WebSocketServerSetup

__autodoc__ = {
    "URL": True,
    "Driver": True,
    "Cookies": True,
    "Request": True,
    "Response": True,
    "WebSocket": True,
    "HTTPVersion": True,
    "ForwardMixin": True,
    "ForwardDriver": True,
    "ReverseDriver": True,
    "combine_driver": True,
    "HTTPServerSetup": True,
    "WebSocketServerSetup": True,
}
