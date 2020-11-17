"""
后端驱动适配基类
=================

各驱动请继承以下基类
"""

import abc

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.typing import Bot, Dict, Type, Union, Optional, Callable


class BaseDriver(abc.ABC):
    """
    Driver 基类。将后端框架封装，以满足适配器使用。
    """

    _adapters: Dict[str, Type[Bot]] = {}
    """
    :类型: ``Dict[str, Type[Bot]]``
    :说明: 已注册的适配器列表
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
        self._clients: Dict[str, Bot] = {}
        """
        :类型: ``Dict[str, Bot]``
        :说明: 已连接的 Bot
        """

    @classmethod
    def register_adapter(cls, name: str, adapter: Type[Bot]):
        """
        :说明:
          注册一个协议适配器
        :参数:
          * ``name: str``: 适配器名称，用于在连接时进行识别
          * ``adapter: Type[Bot]``: 适配器 Class
        """
        cls._adapters[name] = adapter
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
    def bots(self) -> Dict[str, Bot]:
        """
        :类型: ``Dict[str, Bot]``
        :说明: 获取当前所有已连接的 Bot
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
        raise NotImplementedError

    @abc.abstractmethod
    async def _handle_http(self):
        """用于处理 HTTP 类型请求的函数"""
        raise NotImplementedError

    @abc.abstractmethod
    async def _handle_ws_reverse(self):
        """用于处理 WebSocket 类型请求的函数"""
        raise NotImplementedError


class BaseWebSocket(object):
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
