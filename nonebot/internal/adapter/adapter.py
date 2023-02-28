import abc
from contextlib import asynccontextmanager
from typing import Any, Dict, AsyncGenerator

from nonebot.config import Config
from nonebot.internal.driver import (
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)

from .bot import Bot


class Adapter(abc.ABC):
    """协议适配器基类。

    通常，在 Adapter 中编写协议通信相关代码，如: 建立通信连接、处理接收与发送 data 等。

    参数:
        driver: {ref}`nonebot.drivers.Driver` 实例
        kwargs: 其他由 {ref}`nonebot.drivers.Driver.register_adapter` 传入的额外参数
    """

    def __init__(self, driver: Driver, **kwargs: Any):
        self.driver: Driver = driver
        """{ref}`nonebot.drivers.Driver` 实例"""
        self.bots: Dict[str, Bot] = {}
        """本协议适配器已建立连接的 {ref}`nonebot.adapters.Bot` 实例"""

    def __repr__(self) -> str:
        return f"Adapter(name={self.get_name()!r})"

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """当前协议适配器的名称"""
        raise NotImplementedError

    @property
    def config(self) -> Config:
        """全局 NoneBot 配置"""
        return self.driver.config

    def bot_connect(self, bot: Bot) -> None:
        """告知 NoneBot 建立了一个新的 {ref}`nonebot.adapters.Bot` 连接。

        当有新的 {ref}`nonebot.adapters.Bot` 实例连接建立成功时调用。

        参数:
            bot: {ref}`nonebot.adapters.Bot` 实例
        """
        self.driver._bot_connect(bot)
        self.bots[bot.self_id] = bot

    def bot_disconnect(self, bot: Bot) -> None:
        """告知 NoneBot {ref}`nonebot.adapters.Bot` 连接已断开。

        当有 {ref}`nonebot.adapters.Bot` 实例连接断开时调用。

        参数:
            bot: {ref}`nonebot.adapters.Bot` 实例
        """
        if self.bots.pop(bot.self_id, None) is None:
            raise RuntimeError(f"{bot} not found in adapter {self.get_name()}")
        self.driver._bot_disconnect(bot)

    def setup_http_server(self, setup: HTTPServerSetup):
        """设置一个 HTTP 服务器路由配置"""
        if not isinstance(self.driver, ReverseDriver):
            raise TypeError("Current driver does not support http server")
        self.driver.setup_http_server(setup)

    def setup_websocket_server(self, setup: WebSocketServerSetup):
        """设置一个 WebSocket 服务器路由配置"""
        if not isinstance(self.driver, ReverseDriver):
            raise TypeError("Current driver does not support websocket server")
        self.driver.setup_websocket_server(setup)

    async def request(self, setup: Request) -> Response:
        """进行一个 HTTP 客户端请求"""
        if not isinstance(self.driver, ForwardDriver):
            raise TypeError("Current driver does not support http client")
        return await self.driver.request(setup)

    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        """建立一个 WebSocket 客户端连接请求"""
        if not isinstance(self.driver, ForwardDriver):
            raise TypeError("Current driver does not support websocket client")
        async with self.driver.websocket(setup) as ws:
            yield ws

    @abc.abstractmethod
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        """`Adapter` 实际调用 api 的逻辑实现函数，实现该方法以调用 api。

        参数:
            api: API 名称
            data: API 数据
        """
        raise NotImplementedError


__autodoc__ = {"Adapter._call_api": True}
