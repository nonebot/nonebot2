import asyncio
import json
from ipaddress import IPv4Address
from typing import (Any, Callable, Coroutine, Dict, NoReturn, Optional, Set,
                    TypeVar)

import httpx
import websockets

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event as BaseEvent
from nonebot.drivers import Driver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides

from .config import Config
from .event import Event

WebsocketHandlerFunction = Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]
WebsocketHandler_T = TypeVar('WebsocketHandler_T',
                             bound=WebsocketHandlerFunction)


class WebSocket(BaseWebSocket):

    @classmethod
    async def new(cls, *, host: IPv4Address, port: int,
                  session_key: str) -> "WebSocket":
        listen_address = httpx.URL(f'ws://{host}:{port}/all',
                                   params={'sessionKey': session_key})
        websocket = await websockets.connect(uri=str(listen_address))
        return cls(websocket)

    @overrides(BaseWebSocket)
    def __init__(self, websocket: websockets.WebSocketClientProtocol):
        self.event_handlers: Set[WebsocketHandlerFunction] = set()
        super().__init__(websocket)

    @property
    @overrides(BaseWebSocket)
    def websocket(self) -> websockets.WebSocketClientProtocol:
        return self._websocket

    @overrides(BaseWebSocket)
    async def send(self, data: Dict[str, Any]):
        return await self.websocket.send(json.dumps(data))

    @overrides(BaseWebSocket)
    async def receive(self) -> Dict[str, Any]:
        received = await self.websocket.recv()
        return json.loads(received)

    async def _dispatcher(self):
        while not self.websocket.closed:
            try:
                data = await self.receive()
            except websockets.ConnectionClosedOK:
                break
            except Exception as e:
                logger.exception(f'Websocket client listened {self.websocket} '
                                 f'failed to receive data: {e}')
                continue
            asyncio.ensure_future(
                asyncio.gather(*map(lambda f: f(data), self.event_handlers),
                               return_exceptions=True))

    @overrides(BaseWebSocket)
    async def accept(self):
        asyncio.ensure_future(self._dispatcher())

    @overrides(BaseWebSocket)
    async def close(self):
        await self.websocket.close()

    def handle(self, callable: WebsocketHandler_T) -> WebsocketHandler_T:
        self.event_handlers.add(callable)
        return callable


class MiraiBot(BaseBot):

    def __init__(self, connection_type: str, self_id: str, *,
                 websocket: WebSocket):
        super().__init__(connection_type, self_id, websocket=websocket)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        return "mirai"

    @classmethod
    @overrides(BaseBot)
    async def check_permission(cls, driver: "Driver", connection_type: str,
                               headers: dict, body: Optional[dict]) -> NoReturn:
        raise RequestDenied(
            status_code=501,
            reason=f'Connection {connection_type} not implented')

    @classmethod
    @overrides(BaseBot)
    def register(cls, driver: "Driver", config: "Config", qq: int):
        config = Config.parse_obj(config.dict())
        assert config.auth_key and config.host and config.port, f'Current config {config!r} is invalid'

        super().register(driver, config)  # type: ignore

        @driver.on_startup
        async def _startup():
            async with httpx.AsyncClient(
                    base_url=f'http://{config.host}:{config.port}') as client:
                response = await client.get('/about')
                info = response.json()
                logger.debug(f'Mirai API returned info: {info}')
                response = await client.post('/auth',
                                             json={'authKey': config.auth_key})
                status = response.json()
                assert status['code'] == 0
                session_key = status['session']
                response = await client.post('/verify',
                                             json={
                                                 'sessionKey': session_key,
                                                 'qq': qq
                                             })
                assert response.json()['code'] == 0

            websocket = await WebSocket.new(
                host=config.host,  # type: ignore
                port=config.port,  # type: ignore
                session_key=session_key)
            bot = cls(connection_type='forward_ws',
                      self_id=str(qq),
                      websocket=websocket)
            websocket.handle(bot.handle_message)
            driver._clients[str(qq)] = bot
            await websocket.accept()

        @driver.on_shutdown
        async def _shutdown():
            bot = driver._clients.pop(str(qq), None)
            if bot is None:
                return
            await bot.websocket.close()  #type:ignore

    @overrides(BaseBot)
    async def handle_message(self, message: dict):
        event = Event.new(message)
        await handle_event(self, event)

    @overrides(BaseBot)
    async def call_api(self, api: str, **data):
        return super().call_api(api, **data)

    @overrides(BaseBot)
    async def send(self, event: "BaseEvent", message: str, **kwargs):
        return super().send(event, message, **kwargs)
