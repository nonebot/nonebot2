"""
Quart 驱动适配
================

后端使用方法请参考: `Quart 文档`_

.. _Quart 文档:
    https://pgjones.gitlab.io/quart/index.html
"""

import asyncio
from dataclasses import dataclass
from typing import List, TypeVar, Callable, Optional, Coroutine

import uvicorn
from pydantic import BaseSettings

from nonebot.config import Env
from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.config import Config as NoneBotConfig
from nonebot.drivers import HTTPRequest, ReverseDriver
from nonebot.drivers import WebSocket as BaseWebSocket

try:
    from quart import request as _request
    import werkzeug.exceptions as exceptions
    from quart import websocket as _websocket
    from quart import Quart, Request, Response
    from quart import Websocket as QuartWebSocket
except ImportError:
    raise ValueError(
        'Please install Quart by using `pip install nonebot2[quart]`')

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])


class Config(BaseSettings):
    """
    Quart 驱动框架设置
    """
    quart_reload: Optional[bool] = None
    """
    :类型:

      ``Optional[bool]``

    :说明:

      开启/关闭冷重载，默认会在配置了 app 的 debug 模式启用
    """
    quart_reload_dirs: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      重载监控文件夹列表，默认为 uvicorn 默认值
    """
    quart_reload_delay: Optional[float] = None
    """
    :类型:

      ``Optional[float]``

    :说明:

      重载延迟，默认为 uvicorn 默认值
    """
    quart_reload_includes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """
    quart_reload_excludes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """

    class Config:
        extra = "ignore"


class Driver(ReverseDriver):
    """
    Quart 驱动框架

    :上报地址:

      * ``/{adapter name}/http``: HTTP POST 上报
      * ``/{adapter name}/ws``: WebSocket 上报
    """

    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self.quart_config = Config(**config.dict())

        self._server_app = Quart(self.__class__.__qualname__)
        self._server_app.add_url_rule("/<adapter>/http",
                                      methods=["POST"],
                                      view_func=self._handle_http)
        self._server_app.add_websocket("/<adapter>/ws",
                                       view_func=self._handle_ws_reverse)

    @property
    @overrides(ReverseDriver)
    def type(self) -> str:
        """驱动名称: ``quart``"""
        return "quart"

    @property
    @overrides(ReverseDriver)
    def server_app(self) -> Quart:
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def asgi(self):
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def logger(self):
        """Quart 使用的 logger"""
        return self._server_app.logger

    @overrides(ReverseDriver)
    def on_startup(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown`_

        .. _Startup and Shutdown:
            https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html
        """
        return self.server_app.before_serving(func)  # type: ignore

    @overrides(ReverseDriver)
    def on_shutdown(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown`_"""
        return self.server_app.after_serving(func)  # type: ignore

    @overrides(ReverseDriver)
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            *,
            app: Optional[str] = None,
            **kwargs):
        """使用 ``uvicorn`` 启动 Quart"""
        super().run(host, port, app, **kwargs)
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "nonebot.log.LoguruHandler",
                },
            },
            "loggers": {
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": "INFO"
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                },
            },
        }
        uvicorn.run(
            app or self.server_app,  # type: ignore
            host=host or str(self.config.host),
            port=port or self.config.port,
            reload=self.quart_config.quart_reload
            if self.quart_config.quart_reload is not None else
            (bool(app) and self.config.debug),
            reload_dirs=self.quart_config.quart_reload_dirs,
            reload_delay=self.quart_config.quart_reload_delay,
            reload_includes=self.quart_config.quart_reload_includes,
            reload_excludes=self.quart_config.quart_reload_excludes,
            debug=self.config.debug,
            log_config=LOGGING_CONFIG,
            **kwargs)

    async def _handle_http(self, adapter: str):
        request: Request = _request
        data: bytes = await request.get_data()  # type: ignore

        if adapter not in self._adapters:
            logger.warning(f'Unknown adapter {adapter}. '
                           'Please register the adapter before use.')
            raise exceptions.NotFound()

        BotClass = self._adapters[adapter]
        http_request = HTTPRequest(request.http_version, request.scheme,
                                   request.path, request.query_string,
                                   dict(request.headers), request.method, data)

        self_id, response = await BotClass.check_permission(self, http_request)

        if not self_id:
            raise exceptions.Unauthorized(
                description=(response and response.body or b"").decode())
        if self_id in self._clients:
            logger.warning("There's already a reverse websocket connection,"
                           "so the event may be handled twice.")
        bot = BotClass(self_id, http_request)
        asyncio.create_task(bot.handle_message(data))
        return Response(response and response.body or "",
                        response and response.status or 200)

    async def _handle_ws_reverse(self, adapter: str):
        websocket: QuartWebSocket = _websocket
        ws = WebSocket(websocket.http_version, websocket.scheme,
                       websocket.path, websocket.query_string,
                       dict(websocket.headers), websocket)

        if adapter not in self._adapters:
            logger.warning(
                f'Unknown adapter {adapter}. Please register the adapter before use.'
            )
            raise exceptions.NotFound()

        BotClass = self._adapters[adapter]
        self_id, response = await BotClass.check_permission(self, ws)

        if not self_id:
            raise exceptions.Unauthorized(
                description=(response and response.body or b"").decode())

        if self_id in self._clients:
            logger.opt(colors=True).warning(
                "There's already a websocket connection, "
                f"<y>{escape_tag(adapter.upper())} Bot {escape_tag(self_id)}</y> ignored."
            )
            raise exceptions.Forbidden(description='Client already exists.')

        bot = BotClass(self_id, ws)
        await ws.accept()
        logger.opt(colors=True).info(
            f"WebSocket Connection from <y>{escape_tag(adapter.upper())} "
            f"Bot {escape_tag(self_id)}</y> Accepted!")
        self._bot_connect(bot)

        try:
            while not ws.closed:
                try:
                    data = await ws.receive()
                except asyncio.CancelledError:
                    logger.warning("WebSocket disconnected by peer.")
                    break
                except Exception as e:
                    logger.opt(exception=e).error(
                        "Error when receiving data from websocket.")
                    break

                asyncio.create_task(bot.handle_message(data.encode()))
        finally:
            self._bot_disconnect(bot)


@dataclass
class WebSocket(BaseWebSocket):
    websocket: QuartWebSocket = None  # type: ignore

    @property
    @overrides(BaseWebSocket)
    def closed(self):
        # FIXME
        return False

    @overrides(BaseWebSocket)
    async def accept(self):
        await self.websocket.accept()

    @overrides(BaseWebSocket)
    async def close(self):
        # FIXME
        pass

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        return await self.websocket.receive()  # type: ignore

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive()  # type: ignore

    @overrides(BaseWebSocket)
    async def send(self, data: str):
        await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes):
        await self.websocket.send(data)
