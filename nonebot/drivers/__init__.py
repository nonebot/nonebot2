"""
后端驱动适配基类
=================

各驱动请继承以下基类
"""

import abc
import asyncio
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Set,
    Dict,
    Type,
    Callable,
    Awaitable,
    AsyncGenerator,
)

from ._model import URL as URL
from nonebot.log import logger
from nonebot.utils import escape_tag
from ._model import Request as Request
from nonebot.config import Env, Config
from ._model import Response as Response
from ._model import WebSocket as WebSocket
from ._model import HTTPVersion as HTTPVersion
from nonebot.typing import T_BotConnectionHook, T_BotDisconnectionHook

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Adapter


class Driver(abc.ABC):
    """
    Driver 基类。
    """

    _adapters: Dict[str, "Adapter"] = {}
    """
    :类型: ``Dict[str, Adapter]``
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

    def register_adapter(self, adapter: Type["Adapter"], **kwargs) -> None:
        """
        :说明:

          注册一个协议适配器

        :参数:

          * ``name: str``: 适配器名称，用于在连接时进行识别
          * ``adapter: Type[Bot]``: 适配器 Class
          * ``**kwargs``: 其他传递给适配器的参数
        """
        name = adapter.get_name()
        if name in self._adapters:
            logger.opt(colors=True).debug(
                f'Adapter "<y>{escape_tag(name)}</y>" already exists'
            )
            return
        self._adapters[name] = adapter(self, **kwargs)
        logger.opt(colors=True).debug(
            f'Succeeded to load adapter "<y>{escape_tag(name)}</y>"'
        )

    @property
    @abc.abstractmethod
    def type(self) -> str:
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
            f"<g>Loaded adapters: {escape_tag(', '.join(self._adapters))}</g>"
        )

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

    def on_bot_disconnect(self, func: T_BotDisconnectionHook) -> T_BotDisconnectionHook:
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
        if bot.self_id in self._clients:
            raise RuntimeError(f"Duplicate bot connection with id {bot.self_id}")
        self._clients[bot.self_id] = bot

        async def _run_hook(bot: "Bot") -> None:
            coros = list(map(lambda x: x(bot), self._bot_connection_hook))
            if coros:
                try:
                    await asyncio.gather(*coros)
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        "<r><bg #f8bbd0>Error when running WebSocketConnection hook. "
                        "Running cancelled!</bg #f8bbd0></r>"
                    )

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
                        "Running cancelled!</bg #f8bbd0></r>"
                    )

        asyncio.create_task(_run_hook(bot))


class ForwardMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def request(self, setup: Request) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        raise NotImplementedError
        yield  # used for static type checking's generator detection


class ForwardDriver(Driver, ForwardMixin):
    """
    Forward Driver 基类。将客户端框架封装，以满足适配器使用。
    """


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

    @abc.abstractmethod
    def setup_http_server(self, setup: "HTTPServerSetup") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def setup_websocket_server(self, setup: "WebSocketServerSetup") -> None:
        raise NotImplementedError


def combine_driver(driver: Type[Driver], *mixins: Type[ForwardMixin]) -> Type[Driver]:
    # check first
    assert issubclass(driver, Driver), "`driver` must be subclass of Driver"
    assert all(
        map(lambda m: issubclass(m, ForwardMixin), mixins)
    ), "`mixins` must be subclass of ForwardMixin"

    class CombinedDriver(*mixins, driver, ForwardDriver):  # type: ignore
        @property
        def type(self) -> str:
            return (
                driver.type.__get__(self)
                + "+"
                + "+".join(map(lambda x: x.type.__get__(self), mixins))
            )

    return CombinedDriver


@dataclass
class HTTPServerSetup:
    path: URL  # path should not be absolute, check it by URL.is_absolute() == False
    method: str
    name: str
    handle_func: Callable[[Request], Awaitable[Response]]


@dataclass
class WebSocketServerSetup:
    path: URL  # path should not be absolute, check it by URL.is_absolute() == False
    name: str
    handle_func: Callable[[WebSocket], Awaitable[Any]]
