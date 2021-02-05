"""
后端驱动适配基类
=================

各驱动请继承以下基类
"""

import abc
import asyncio
from typing import Set, Dict, Type, Optional, Callable, TYPE_CHECKING

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.typing import T_WebSocketConnectionHook, T_WebSocketDisconnectionHook

if TYPE_CHECKING:
    from nonebot.adapters import Bot


class Driver(abc.ABC):
    """
    Driver 基类。将后端框架封装，以满足适配器使用。
    """

    _adapters: Dict[str, Type["Bot"]] = {}
    """
    :类型: ``Dict[str, Type[Bot]]``
    :说明: 已注册的适配器列表
    """
    _ws_connection_hook: Set[T_WebSocketConnectionHook] = set()
    """
    :类型: ``Set[T_WebSocketConnectionHook]``
    :说明: WebSocket 连接建立时执行的函数
    """
    _ws_disconnection_hook: Set[T_WebSocketDisconnectionHook] = set()
    """
    :类型: ``Set[T_WebSocketDisconnectionHook]``
    :说明: WebSocket 连接断开时执行的函数
    """

    @abc.abstractmethod
    def __init__(self, env: Env, config: Config):
        """
        :参数:

          * ``env: Env``: 包含环境信息的 Env 对象
          * ``config: Config``: 包含配置信息的 Config 对象
        """
        self.env = env.environment
        """
        :类型: ``str``
        :说明: 环境名称
        """
        self.config = config
        """
        :类型: ``Config``
        :说明: 配置对象
        """
        self._clients: Dict[str, "Bot"] = {}
        """
        :类型: ``Dict[str, Bot]``
        :说明: 已连接的 Bot
        """

    def register_adapter(self, name: str, adapter: Type["Bot"], **kwargs):
        """
        :说明:

          注册一个协议适配器

        :参数:

          * ``name: str``: 适配器名称，用于在连接时进行识别
          * ``adapter: Type[Bot]``: 适配器 Class
        """
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
    def server_app(self):
        """驱动 APP 对象"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def asgi(self):
        """驱动 ASGI 对象"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def logger(self):
        """驱动专属 logger 日志记录器"""
        raise NotImplementedError

    @property
    def bots(self) -> Dict[str, "Bot"]:
        """
        :类型:

          ``Dict[str, Bot]``
        :说明:

          获取当前所有已连接的 Bot
        """
        return self._clients

    @abc.abstractmethod
    def on_startup(self, func: Callable) -> Callable:
        """注册一个在驱动启动时运行的函数"""
        raise NotImplementedError

    @abc.abstractmethod
    def on_shutdown(self, func: Callable) -> Callable:
        """注册一个在驱动停止时运行的函数"""
        raise NotImplementedError

    def on_bot_connect(
            self, func: T_WebSocketConnectionHook) -> T_WebSocketConnectionHook:
        """
        :说明:

          装饰一个函数使他在 bot 通过 WebSocket 连接成功时执行。

        :函数参数:

          * ``bot: Bot``: 当前连接上的 Bot 对象
        """
        self._ws_connection_hook.add(func)
        return func

    def on_bot_disconnect(
            self,
            func: T_WebSocketDisconnectionHook) -> T_WebSocketDisconnectionHook:
        """
        :说明:

          装饰一个函数使他在 bot 通过 WebSocket 连接断开时执行。

        :函数参数:

          * ``bot: Bot``: 当前连接上的 Bot 对象
        """
        self._ws_disconnection_hook.add(func)
        return func

    def _bot_connect(self, bot: "Bot") -> None:
        """在 WebSocket 连接成功后，调用该函数来注册 bot 对象"""
        self._clients[bot.self_id] = bot

        async def _run_hook(bot: "Bot") -> None:
            coros = list(map(lambda x: x(bot), self._ws_connection_hook))
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
            coros = list(map(lambda x: x(bot), self._ws_disconnection_hook))
            if coros:
                try:
                    await asyncio.gather(*coros)
                except Exception as e:
                    logger.opt(colors=True, exception=e).error(
                        "<r><bg #f8bbd0>Error when running WebSocketDisConnection hook. "
                        "Running cancelled!</bg #f8bbd0></r>")

        asyncio.create_task(_run_hook(bot))

    @abc.abstractmethod
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            *args,
            **kwargs):
        """
        :说明:

          启动驱动框架

        :参数:

          * ``host: Optional[str]``: 驱动绑定 IP
          * ``post: Optional[int]``: 驱动绑定端口
          * ``*args``
          * ``**kwargs``
        """
        logger.opt(colors=True).debug(
            f"<g>Loaded adapters: {', '.join(self._adapters)}</g>")

    @abc.abstractmethod
    async def _handle_http(self):
        """用于处理 HTTP 类型请求的函数"""
        raise NotImplementedError

    @abc.abstractmethod
    async def _handle_ws_reverse(self):
        """用于处理 WebSocket 类型请求的函数"""
        raise NotImplementedError


class WebSocket(object):
    """WebSocket 连接封装，统一接口方便外部调用。"""

    @abc.abstractmethod
    def __init__(self, websocket):
        """
        :参数:

          * ``websocket: Any``: WebSocket 连接对象
        """
        self._websocket = websocket

    @property
    def websocket(self):
        """WebSocket 连接对象"""
        return self._websocket

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
    async def receive(self) -> dict:
        """接收一条 WebSocket 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, data: dict):
        """发送一条 WebSocket 信息"""
        raise NotImplementedError
