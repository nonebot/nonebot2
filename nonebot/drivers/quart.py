"""
Quart 驱动适配
================

后端使用方法请参考: `Quart 文档`_

.. _Quart 文档:
    https://pgjones.gitlab.io/quart/index.html
"""

import asyncio
from json.decoder import JSONDecodeError
from typing import Any, Callable, Coroutine, Dict, Optional, Type, TypeVar

import uvicorn

from nonebot.config import Config as NoneBotConfig
from nonebot.config import Env
from nonebot.drivers import Driver as BaseDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.typing import overrides

try:
    from quart import Quart, Request, Response
    from quart import Websocket as QuartWebSocket
    from quart import exceptions
    from quart import request as _request
    from quart import websocket as _websocket
except ImportError:
    raise ValueError(
        'Please install Quart by using `pip install nonebot2[quart]`')

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])


class Driver(BaseDriver):
    """
    Quart 驱动框架

    :上报地址:

      * ``/{adapter name}/http``: HTTP POST 上报
      * ``/{adapter name}/ws``: WebSocket 上报
    """

    @overrides(BaseDriver)
    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self._server_app = Quart(self.__class__.__qualname__)
        self._server_app.add_url_rule('/<adapter>/http',
                                      methods=['POST'],
                                      view_func=self._handle_http)
        self._server_app.add_websocket('/<adapter>/ws',
                                       view_func=self._handle_ws_reverse)

    @property
    @overrides(BaseDriver)
    def type(self) -> str:
        """驱动名称: ``quart``"""
        return 'quart'

    @property
    @overrides(BaseDriver)
    def server_app(self) -> Quart:
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(BaseDriver)
    def asgi(self):
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(BaseDriver)
    def logger(self):
        """fastapi 使用的 logger"""
        return self._server_app.logger

    @overrides(BaseDriver)
    def on_startup(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown <https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html>`_"""
        return self.server_app.before_serving(func)  # type: ignore

    @overrides(BaseDriver)
    def on_shutdown(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown <https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html>`_"""
        return self.server_app.after_serving(func)  # type: ignore

    @overrides(BaseDriver)
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
        uvicorn.run(app or self.server_app,
                    host=host or str(self.config.host),
                    port=port or self.config.port,
                    reload=bool(app) and self.config.debug,
                    debug=self.config.debug,
                    log_config=LOGGING_CONFIG,
                    **kwargs)

    @overrides(BaseDriver)
    async def _handle_http(self, adapter: str):
        request: Request = _request

        try:
            data: Dict[str, Any] = await request.get_json()
        except Exception as e:
            raise exceptions.BadRequest()

        if adapter not in self._adapters:
            logger.warning(f'Unknown adapter {adapter}. '
                           'Please register the adapter before use.')
            raise exceptions.NotFound()

        BotClass = self._adapters[adapter]
        headers = {k: v for k, v in request.headers.items(lower=True)}

        try:
            self_id = await BotClass.check_permission(self, 'http', headers,
                                                      data)
        except RequestDenied as e:
            raise exceptions.HTTPException(status_code=e.status_code,
                                           description=e.reason,
                                           name='Request Denied')
        if self_id in self._clients:
            logger.warning("There's already a reverse websocket connection,"
                           "so the event may be handled twice.")
        bot = BotClass('http', self_id)
        asyncio.create_task(bot.handle_message(data))
        return Response('', 204)

    @overrides(BaseDriver)
    async def _handle_ws_reverse(self, adapter: str):
        websocket: QuartWebSocket = _websocket
        if adapter not in self._adapters:
            logger.warning(
                f'Unknown adapter {adapter}. Please register the adapter before use.'
            )
            raise exceptions.NotFound()

        BotClass = self._adapters[adapter]
        headers = {k: v for k, v in websocket.headers.items(lower=True)}
        try:
            self_id = await BotClass.check_permission(self, 'websocket',
                                                      headers, None)
        except RequestDenied as e:
            raise exceptions.HTTPException(status_code=e.status_code,
                                           description=e.reason,
                                           name='Request Denied')
        if self_id in self._clients:
            logger.warning("There's already a reverse websocket connection,"
                           "so the event may be handled twice.")
        ws = WebSocket(websocket)
        bot = BotClass('websocket', self_id, websocket=ws)
        await ws.accept()
        logger.opt(colors=True).info(
            f"WebSocket Connection from <y>{adapter.upper()} "
            f"Bot {self_id}</y> Accepted!")
        self._bot_connect(bot)

        try:
            while not ws.closed:
                data = await ws.receive()
                if data is None:
                    continue
                asyncio.create_task(bot.handle_message(data))
        finally:
            self._bot_disconnect(bot)


class WebSocket(BaseWebSocket):

    @overrides(BaseWebSocket)
    def __init__(self, websocket: QuartWebSocket):
        super().__init__(websocket)
        self._closed = False

    @property
    @overrides(BaseWebSocket)
    def websocket(self) -> QuartWebSocket:
        return self._websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self):
        return self._closed

    @overrides(BaseWebSocket)
    async def accept(self):
        await self.websocket.accept()
        self._closed = False

    @overrides(BaseWebSocket)
    async def close(self):
        self._closed = True

    @overrides(BaseWebSocket)
    async def receive(self) -> Optional[Dict[str, Any]]:
        data: Optional[Dict[str, Any]] = None
        try:
            data = await self.websocket.receive_json()
        except JSONDecodeError:
            logger.warning('Received an invalid json message.')
        except asyncio.CancelledError:
            self._closed = True
            logger.warning('WebSocket disconnected by peer.')
        return data

    @overrides(BaseWebSocket)
    async def send(self, data: dict):
        await self.websocket.send_json(data)
