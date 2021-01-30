import asyncio
import json
from ipaddress import IPv4Address
from typing import (Any, Callable, Coroutine, Dict, NoReturn, Optional, Set,
                    TypeVar)

import httpx
import websockets

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event as BaseEvent
from nonebot.config import Config
from nonebot.drivers import Driver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides

from .config import Config as MiraiConfig
from .event import Event

WebsocketHandlerFunction = Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]
WebsocketHandler_T = TypeVar('WebsocketHandler_T',
                             bound=WebsocketHandlerFunction)


async def _ws_authorization(client: httpx.AsyncClient, *, auth_key: str,
                            qq: int) -> str:

    async def request(method: str, *, path: str, **kwargs) -> Dict[str, Any]:
        response = await client.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()

    about = await request('GET', path='/about')
    logger.opt(colors=True).debug('Mirai API HTTP backend version: '
                                  f'<g><b>{about["data"]["version"]}</b></g>')

    status = await request('POST', path='/auth', json={'authKey': auth_key})
    assert status['code'] == 0
    session_key = status['session']

    verify = await request('POST',
                           path='/verify',
                           json={
                               'sessionKey': session_key,
                               'qq': qq
                           })
    assert verify['code'] == 0, verify['msg']
    return session_key


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

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def send(self, data: Dict[str, Any]):
        return await self.websocket.send(json.dumps(data))

    @overrides(BaseWebSocket)
    async def receive(self) -> Dict[str, Any]:
        received = await self.websocket.recv()
        return json.loads(received)

    async def _dispatcher(self):
        while not self.closed:
            try:
                data = await self.receive()
            except websockets.ConnectionClosedOK:
                logger.debug(f'Websocket connection {self.websocket} closed')
                break
            except websockets.ConnectionClosedError:
                logger.exception(f'Websocket connection {self.websocket} '
                                 'connection closed abnormally:')
                break
            except json.JSONDecodeError as e:
                logger.exception(f'Websocket client listened {self.websocket} '
                                 f'failed to decode data: {e}')
                continue
            asyncio.gather(*map(lambda f: f(data), self.event_handlers),
                           return_exceptions=True)

    @overrides(BaseWebSocket)
    async def accept(self):
        asyncio.create_task(self._dispatcher())

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

    @property
    def alive(self) -> bool:
        return not self.websocket.closed

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
        cls.mirai_config = MiraiConfig(**config.dict())
        cls.active = True
        assert cls.mirai_config.auth_key is not None
        assert cls.mirai_config.host is not None
        assert cls.mirai_config.port is not None
        super().register(driver, config)

        async def _bot_connection():
            async with httpx.AsyncClient(
                    base_url=
                    f'http://{cls.mirai_config.host}:{cls.mirai_config.port}'
            ) as client:
                session_key = await _ws_authorization(
                    client,
                    auth_key=cls.mirai_config.auth_key,  # type: ignore
                    qq=qq)  # type: ignore

            websocket = await WebSocket.new(
                host=cls.mirai_config.host,  # type: ignore
                port=cls.mirai_config.port,  # type: ignore
                session_key=session_key)
            bot = cls(connection_type='forward_ws',
                      self_id=str(qq),
                      websocket=websocket)
            websocket.handle(bot.handle_message)
            driver._clients[str(qq)] = bot
            await websocket.accept()

        async def _connection_ensure():
            if str(qq) not in driver._clients:
                await _bot_connection()
            elif not driver._clients[str(qq)].alive:
                driver._clients.pop(str(qq), None)
                await _bot_connection()

        @driver.on_startup
        async def _startup():

            async def _checker():
                while cls.active:
                    try:
                        await _connection_ensure()
                    except Exception as e:
                        logger.opt(colors=True).warning(
                            'Failed to create mirai connection to '
                            f'<y>{qq}</y>, reason: <r>{e}</r>. '
                            'Will retry after 3 seconds')
                    await asyncio.sleep(3)

            asyncio.create_task(_checker())

        @driver.on_shutdown
        async def _shutdown():
            cls.active = False
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
