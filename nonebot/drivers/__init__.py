"""本模块定义了驱动适配器基类。

各驱动请继承以下基类。

FrontMatter:
    sidebar_position: 0
    description: nonebot.drivers 模块
"""

from nonebot.internal.driver import URL as URL
from nonebot.internal.driver import Driver as Driver
from nonebot.internal.driver import Cookies as Cookies
from nonebot.internal.driver import Request as Request
from nonebot.internal.driver import Response as Response
from nonebot.internal.driver import WebSocket as WebSocket
from nonebot.internal.driver import HTTPVersion as HTTPVersion
from nonebot.internal.driver import ForwardMixin as ForwardMixin
from nonebot.internal.driver import ForwardDriver as ForwardDriver
from nonebot.internal.driver import ReverseDriver as ReverseDriver
from nonebot.internal.driver import combine_driver as combine_driver
from nonebot.internal.driver import HTTPServerSetup as HTTPServerSetup
from nonebot.internal.driver import WebSocketServerSetup as WebSocketServerSetup

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
