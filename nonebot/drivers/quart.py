import asyncio
from json.decoder import JSONDecodeError
from logging import getLogger, warn
from typing import Any, Callable, Coroutine, Dict, Optional, TypeVar

from nonebot.config import Config as NoneBotConfig
from nonebot.config import Env
from nonebot.drivers import Driver as BaseDriver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import RequestDenied
from nonebot.log import LoguruHandler, logger
from nonebot.typing import overrides

try:
    from hypercorn.asyncio import serve
    from hypercorn.config import Config as HypercornConfig
    from quart import Quart, Request, Response
    from quart import Websocket as QuartWebSocket
    from quart import exceptions
    from quart import request as _request
    from quart import websocket as _websocket
except ImportError:
    raise ValueError('Quart not fount, please install quart first')

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])


class Driver(BaseDriver):

    @overrides(BaseDriver)
    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self._server_app = Quart(self.__class__.__qualname__)
        self._server_app.logger.handlers.clear()
        self._server_app.logger.addHandler(LoguruHandler())
        self._server_app.route('/<adapter>/http',
                               methods=['POST'])(self._handle_http)
        self._server_app.websocket('/<adapter>/ws')(self._handle_ws_reverse)

    @property
    @overrides(BaseDriver)
    def type(self) -> str:
        return 'quart'

    @property
    @overrides(BaseDriver)
    def server_app(self) -> Quart:
        return self._server_app

    @property
    @overrides(BaseDriver)
    def asgi(self):
        return self._server_app

    @property
    @overrides(BaseDriver)
    def loggers(self):
        return self._server_app.logger

    @overrides(BaseDriver)
    def on_startup(self, func: _AsyncCallable) -> _AsyncCallable:
        return self.server_app.before_serving(func)  # type: ignore

    @overrides(BaseDriver)
    def on_shutdown(self, func: _AsyncCallable) -> _AsyncCallable:
        return self.server_app.after_serving(func)  # type: ignore

    @overrides(BaseDriver)
    def run(self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            **kwargs):
        super().run(host, port, **kwargs)
        config = HypercornConfig()
        for k, v in kwargs.items():
            if not hasattr(config, k):
                warn(f'Config {k!r} is not available for quart driver.')
                continue
            setattr(config, k, v)
        config.bind.append(
            f'{host or self.config.host}:{port or self.config.port}')

        serve_task = asyncio.run_coroutine_threadsafe(
            coro=serve(self.server_app, config),
            loop=asyncio.get_running_loop(),
        )
        try:
            serve_task.result()
        finally:
            serve_task.cancel()

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
        headers = dict(request.headers)
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
        headers = dict(websocket.headers)
        try:
            self_id = await BotClass.check_permission(self, 'ws', headers, None)
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
