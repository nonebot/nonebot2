from typing import Any, Dict, Optional, Tuple
from datetime import datetime, timedelta
from ipaddress import IPv4Address

import httpx

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event as BaseEvent
from nonebot.config import Config
from nonebot.drivers import Driver, WebSocket
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides

from .config import Config as MiraiConfig
from .event import Event, FriendMessage, TempMessage, GroupMessage


class SessionManager:
    sessions: Dict[int, Tuple[str, datetime, httpx.AsyncClient]] = {}
    session_expiry: timedelta = timedelta(minutes=15)

    def __init__(self, session_key: str, client: httpx.AsyncClient):
        self.session_key, self.client = session_key, client

    async def post(self, path: str, *, params: Optional[Dict[str, Any]] = None):
        params = {**(params or {}), 'sessionKey': self.session_key}
        response = await self.client.post(path, json=params)
        response.raise_for_status()
        return response.json()

    @classmethod
    async def new(cls, self_id: int, *, host: IPv4Address, port: int,
                  auth_key: str):
        if self_id in cls.sessions:
            manager = cls.get(self_id)
            if manager is not None:
                return manager
        client = httpx.AsyncClient(base_url=f'http://{host}:{port}')
        response = await client.post('/auth', json={'authKey': auth_key})
        response.raise_for_status()
        auth = response.json()
        assert auth['code'] == 0
        session_key = auth['session']
        response = await client.post('/verify',
                                     json={
                                         'sessionKey': session_key,
                                         'qq': self_id
                                     })
        assert response.json()['code'] == 0
        cls.sessions[self_id] = session_key, datetime.now(), client
        return cls(session_key, client)

    @classmethod
    def get(cls, self_id: int):
        key, time, client = cls.sessions[self_id]
        if datetime.now() - time > cls.session_expiry:
            return None
        return cls(key, client)


class MiraiBot(BaseBot):

    def __init__(self,
                 connection_type: str,
                 self_id: str,
                 *,
                 websocket: Optional[WebSocket] = None):
        super().__init__(connection_type, self_id, websocket=websocket)
        self.api = SessionManager.get(int(self_id))

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
                               headers: dict, body: Optional[dict]) -> str:
        if connection_type == 'ws':
            raise RequestDenied(
                status_code=501,
                reason='Websocket connection is not implemented')
        self_id: Optional[str] = headers.get('bot')
        if self_id is None:
            raise RequestDenied(status_code=400,
                                reason='Header `Bot` is required.')
        self_id = str(self_id).strip()
        await SessionManager.new(
            int(self_id),
            host=cls.mirai_config.host,  # type: ignore
            port=cls.mirai_config.port,  #type: ignore
            auth_key=cls.mirai_config.auth_key)  # type: ignore
        return self_id

    @classmethod
    @overrides(BaseBot)
    def register(cls, driver: "Driver", config: "Config"):
        cls.mirai_config = MiraiConfig(**config.dict())
        assert cls.mirai_config.auth_key is not None
        assert cls.mirai_config.host is not None
        assert cls.mirai_config.port is not None
        super().register(driver, config)

    @overrides(BaseBot)
    async def handle_message(self, message: dict):
        await handle_event(bot=self,
                           event=Event.new({
                               **message,
                               'self_id': self.self_id,
                           }))

    @overrides(BaseBot)
    async def call_api(self, api: str, **data):
        return await self.api.post('/' + api, params=data)

    @overrides(BaseBot)
    async def send(self, event: "BaseEvent", message: str, **kwargs):
        pass
