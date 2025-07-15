"""本模块定义了驱动适配器基类。

各驱动请继承以下基类。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 0
    description: nonebot.drivers 模块
"""

from nonebot.internal.driver import URL as URL
from nonebot.internal.driver import ASGIMixin as ASGIMixin
from nonebot.internal.driver import Cookies as Cookies
from nonebot.internal.driver import Driver as Driver
from nonebot.internal.driver import ForwardDriver as ForwardDriver
from nonebot.internal.driver import ForwardMixin as ForwardMixin
from nonebot.internal.driver import HTTPClientMixin as HTTPClientMixin
from nonebot.internal.driver import HTTPClientSession as HTTPClientSession
from nonebot.internal.driver import HTTPServerSetup as HTTPServerSetup
from nonebot.internal.driver import HTTPVersion as HTTPVersion
from nonebot.internal.driver import Mixin as Mixin
from nonebot.internal.driver import Request as Request
from nonebot.internal.driver import Response as Response
from nonebot.internal.driver import ReverseDriver as ReverseDriver
from nonebot.internal.driver import ReverseMixin as ReverseMixin
from nonebot.internal.driver import Timeout as Timeout
from nonebot.internal.driver import WebSocket as WebSocket
from nonebot.internal.driver import WebSocketClientMixin as WebSocketClientMixin
from nonebot.internal.driver import WebSocketServerSetup as WebSocketServerSetup
from nonebot.internal.driver import combine_driver as combine_driver

__autodoc__ = {
    "URL": True,
    "Cookies": True,
    "Request": True,
    "Response": True,
    "Timeout": True,
    "WebSocket": True,
    "HTTPVersion": True,
    "Driver": True,
    "Mixin": True,
    "ForwardMixin": True,
    "ForwardDriver": True,
    "HTTPClientMixin": True,
    "WebSocketClientMixin": True,
    "ReverseMixin": True,
    "ReverseDriver": True,
    "ASGIMixin": True,
    "combine_driver": True,
    "HTTPServerSetup": True,
    "WebSocketServerSetup": True,
}
