"""
后端驱动适配基类
=================

各驱动请继承以下基类
"""

import abc
import asyncio
from dataclasses import dataclass, field
from typing import Any, Set, Dict, Type, Union, Optional, Callable, Awaitable, TYPE_CHECKING

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.typing import T_BotConnectionHook, T_BotDisconnectionHook

if TYPE_CHECKING:
    from nonebot.adapters import Bot


class Driver(abc.ABC):
    """
    Driver 基类。
    """

    _adapters: Dict[str, Type["Bot"]] = {}
    """
    :类型: ``Dict[str, Type[Bot]]``
    :说明: 已注册的适配器列表
    """
    _bot_connection_hook: Set[T_BotConnectionHook] = set()
    """
    :类型: ``Set[T_BotConnectionHook]``
    :说明: Bot 连接建立时执行的函数
    """
    _bot_disconnection_hook: Set[T_BotDisconnectionHook] = set()
    """
    :类型: ``Set[T_BotDisconnectionHook]``
    :说明: Bot 连接断开时执行的函数
    """

    def __init__(self, env: Env, config: Config):
        """
        :参数:

          * ``env: Env``: 包含环境信息的 Env 对象
          * ``config: Config``: 包含配置信息的 Config 对象
        """
        self.env: str = env.environment
        """
        :类型: ``str``
        :说明: 环境名称
        """
        self.config: Config = config
        """
        :类型: ``Config``
        :说明: 配置对象
        """
        self._clients: Dict[str, "Bot"] = {}
        """
        :类型: ``Dict[str, Bot]``
        :说明: 已连接的 Bot
        """

    @property
    def bots(self) -> Dict[str, "Bot"]:
        """
        :类型:

          ``Dict[str, Bot]``
        :说明:

          获取当前所有已连接的 Bot
        """
        return self._clients

    def register_adapter(self, name: str, adapter: Type["Bot"], **kwargs):
        """
        :说明:

          注册一个协议适配器

        :参数:

          * ``name: str``: 适配器名称，用于在连接时进行识别
          * ``adapter: Type[Bot]``: 适配器 Class
          * ``**kwargs``: 其他传递给适配器的参数
        """
        if name in self._adapters:
            logger.opt(
                colors=True).debug(f'Adapter "<y>{name}</y>" already exists')
            return
        self._adapters[name] = adapter
        adapter.register(self, self.config, **kwargs)
        logger.opt(
            colors=True).debug(f'Succeeded to load adapter "<y>{name}</y>"')

    @property
    @abc.abstractmethod
    def type(self):
        """驱动类型名称"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def logger(self):
        """驱动专属 logger 日志记录器"""
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """
        :说明:

          启动驱动框架

        :参数:
          * ``*args``
          * ``**kwargs``
        """
        logger.opt(colors=True).debug(
            f"<g>Loaded adapters: {', '.join(self._adapters)}</g>")

    @abc.abstractmethod
    def on_startup(self, func: Callable) -> Callable:
        """注册一个在驱动启动时运行的函数"""
        raise NotImplementedError

    @abc.abstractmethod
    def on_shutdown(self, func: Callable) -> Callable:
        """注册一个在驱动停止时运行的函数"""
        raise NotImplementedError

    def on_bot_connect(self, func: T_BotConnectionHook) -> T_BotConnectionHook:
        """
        :说明:

          装饰一个函数使他在 bot 通过 WebSocket 连接成功时执行。

        :函数参数:

          * ``bot: Bot``: 当前连接上的 Bot 对象
        """
        self._bot_connection_hook.add(func)
        return func

    def on_bot_disconnect(
            self, func: T_BotDisconnectionHook) -> T_BotDisconnectionHook:
        """
        :说明:

          装饰一个函数使他在 bot 通过 WebSocket 连接断开时执行。

        :函数参数:

          * ``bot: Bot``: 当前连接上的 Bot 对象
        """
        self._bot_disconnection_hook.add(func)
        return func

    def _bot_connect(self, bot: "Bot") -> None:
        """在 WebSocket 连接成功后，调用该函数来注册 bot 对象"""
        self._clients[bot.self_id] = bot

        async def _run_hook(bot: "Bot") -> None:
            coros = list(map(lambda x: x(bot), self._bot_connection_hook))
            if coros:
                try:
                    await asyncio.gather(*coros)
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        "<r><bg #f8bbd0>Error when running WebSocketConnection hook. "
                        "Running cancelled!</bg #f8bbd0></r>")

        asyncio.create_task(_run_hook(bot))

    def _bot_disconnect(self, bot: "Bot") -> None:
        """在 WebSocket 连接断开后，调用该函数来注销 bot 对象"""
        if bot.self_id in self._clients:
            del self._clients[bot.self_id]

        async def _run_hook(bot: "Bot") -> None:
            coros = list(map(lambda x: x(bot), self._bot_disconnection_hook))
            if coros:
                try:
                    await asyncio.gather(*coros)
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        "<r><bg #f8bbd0>Error when running WebSocketDisConnection hook. "
                        "Running cancelled!</bg #f8bbd0></r>")

        asyncio.create_task(_run_hook(bot))


class ForwardDriver(Driver):
    """
    Forward Driver 基类。将客户端框架封装，以满足适配器使用。
    """

    @abc.abstractmethod
    def setup_http_polling(
        self, setup: Union["HTTPPollingSetup",
                           Callable[[], Awaitable["HTTPPollingSetup"]]]
    ) -> None:
        """
        :说明:

          注册一个 HTTP 轮询连接，如果传入一个函数，则该函数会在每次连接时被调用

        :参数:

          * ``setup: Union[HTTPPollingSetup, Callable[[], Awaitable[HTTPPollingSetup]]]``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def setup_websocket(
        self, setup: Union["WebSocketSetup",
                           Callable[[], Awaitable["WebSocketSetup"]]]
    ) -> None:
        """
        :说明:

          注册一个 WebSocket 连接，如果传入一个函数，则该函数会在每次重连时被调用

        :参数:

          * ``setup: Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]``
        """
        raise NotImplementedError


class ReverseDriver(Driver):
    """
    Reverse Driver 基类。将后端框架封装，以满足适配器使用。
    """

    @property
    @abc.abstractmethod
    def server_app(self) -> Any:
        """驱动 APP 对象"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def asgi(self) -> Any:
        """驱动 ASGI 对象"""
        raise NotImplementedError


@dataclass
class HTTPConnection(abc.ABC):
    http_version: str
    """One of ``"1.0"``, ``"1.1"`` or ``"2"``."""
    scheme: str
    """URL scheme portion (likely ``"http"`` or ``"https"``)."""
    path: str
    """
    HTTP request target excluding any query string,
    with percent-encoded sequences and UTF-8 byte sequences
    decoded into characters.
    """
    query_string: bytes = b""
    """ URL portion after the ``?``, percent-encoded."""
    headers: Dict[str, str] = field(default_factory=dict)
    """A dict of name-value pairs,
    where name is the header name, and value is the header value.

    Order of header values must be preserved from the original HTTP request;
    order of header names is not important.

    Header names must be lowercased.
    """

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """Connection type."""
        raise NotImplementedError


@dataclass
class HTTPRequest(HTTPConnection):
    """HTTP 请求封装。参考 `asgi http scope`_。

    .. _asgi http scope:
        https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope
    """
    method: str = "GET"
    """The HTTP method name, uppercased."""
    body: bytes = b""
    """Body of the request.

    Optional; if missing defaults to ``b""``.
    """

    @property
    def type(self) -> str:
        """Always ``http``"""
        return "http"


@dataclass
class HTTPResponse:
    """HTTP 响应封装。参考 `asgi http scope`_。

    .. _asgi http scope:
        https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope
    """
    status: int
    """HTTP status code."""
    body: Optional[bytes] = None
    """HTTP body content.

    Optional; if missing defaults to ``None``.
    """
    headers: Dict[str, str] = field(default_factory=dict)
    """A dict of name-value pairs,
    where name is the header name, and value is the header value.

    Order must be preserved in the HTTP response.

    Header names must be lowercased.

    Optional; if missing defaults to an empty dict.
    """

    @property
    def type(self) -> str:
        """Always ``http``"""
        return "http"


@dataclass
class WebSocket(HTTPConnection, abc.ABC):
    """WebSocket 连接封装。参考 `asgi websocket scope`_。

    .. _asgi websocket scope:
        https://asgi.readthedocs.io/en/latest/specs/www.html#websocket-connection-scope
    """

    @property
    def type(self) -> str:
        """Always ``websocket``"""
        return "websocket"

    @property
    @abc.abstractmethod
    def closed(self):
        """
        :类型: ``bool``
        :说明: 连接是否已经关闭
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def accept(self):
        """接受 WebSocket 连接请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self, code: int):
        """关闭 WebSocket 连接请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def receive(self) -> str:
        """接收一条 WebSocket text 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def receive_bytes(self) -> bytes:
        """接收一条 WebSocket binary 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, data: str):
        """发送一条 WebSocket text 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def send_bytes(self, data: bytes):
        """发送一条 WebSocket binary 信息"""
        raise NotImplementedError


@dataclass
class HTTPPollingSetup:
    adapter: str
    """协议适配器名称"""
    self_id: str
    """机器人 ID"""
    url: str
    """URL"""
    method: str
    """HTTP method"""
    body: bytes
    """HTTP body"""
    headers: Dict[str, str]
    """HTTP headers"""
    http_version: str
    """HTTP version"""
    poll_interval: float
    """HTTP 轮询间隔"""


@dataclass
class WebSocketSetup:
    adapter: str
    """协议适配器名称"""
    self_id: str
    """机器人 ID"""
    url: str
    """URL"""
    headers: Dict[str, str] = field(default_factory=dict)
    """HTTP headers"""
    reconnect_interval: float = 3.
    """WebSocket 重连间隔"""
