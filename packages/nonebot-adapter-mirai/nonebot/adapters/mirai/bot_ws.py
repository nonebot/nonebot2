import asyncio
import json
from ipaddress import IPv4Address
from typing import (Any, Callable, Coroutine, Dict, NoReturn, Optional, Set,
                    TypeVar)

import httpx
import websockets

from nonebot.config import Config
from nonebot.drivers import Driver
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.typing import overrides

from .bot import SessionManager, Bot

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
        await (await websocket.ping())
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
            asyncio.gather(
                *map(lambda f: f(data), self.event_handlers),  #type: ignore
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


class WebsocketBot(Bot):
    """
    mirai-api-http 正向 Websocket 协议 Bot 适配。
    """

    @overrides(Bot)
    def __init__(self, connection_type: str, self_id: str, *,
                 websocket: WebSocket):
        super().__init__(connection_type, self_id, websocket=websocket)

    @property
    @overrides(Bot)
    def type(self) -> str:
        return "mirai-ws"

    @property
    def alive(self) -> bool:
        return not self.websocket.closed

    @property
    def api(self) -> SessionManager:
        api = SessionManager.get(self_id=int(self.self_id), check_expire=False)
        assert api is not None, 'SessionManager has not been initialized'
        return api

    @classmethod
    @overrides(Bot)
    async def check_permission(cls, driver: "Driver", connection_type: str,
                               headers: dict, body: Optional[dict]) -> NoReturn:
        raise RequestDenied(
            status_code=501,
            reason=f'Connection {connection_type} not implented')

    @classmethod
    @overrides(Bot)
    def register(cls, driver: "Driver", config: "Config", qq: int):
        """
        :说明:

          注册该Adapter 

        :参数:

          * ``driver: Driver``: 程序所使用的``Driver``
          * ``config: Config``: 程序配置对象
          * ``qq: int``: 要使用的Bot的QQ号 **注意: 在使用正向Websocket时必须指定该值!**
        """
        super().register(driver, config)
        cls.active = True

        async def _bot_connection():
            session: SessionManager = await SessionManager.new(
                qq,
                host=cls.mirai_config.host,  # type: ignore
                port=cls.mirai_config.port,  # type: ignore
                auth_key=cls.mirai_config.auth_key  # type: ignore
            )
            websocket = await WebSocket.new(
                host=cls.mirai_config.host,  # type: ignore
                port=cls.mirai_config.port,  # type: ignore
                session_key=session.session_key)
            bot = cls(connection_type='forward_ws',
                      self_id=str(qq),
                      websocket=websocket)
            websocket.handle(bot.handle_message)
            await websocket.accept()
            return bot

        async def _connection_ensure():
            self_id = str(qq)
            if self_id not in driver._clients:
                bot = await _bot_connection()
                driver._bot_connect(bot)
            else:
                bot = driver._clients[self_id]
            if not bot.alive:
                driver._bot_disconnect(bot)
            return

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
