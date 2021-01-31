from datetime import datetime, timedelta
from io import BytesIO
from ipaddress import IPv4Address
from typing import Any, Dict, List, NoReturn, Optional, Tuple, Union

import httpx

from nonebot.adapters import Bot as BaseBot
from nonebot.config import Config
from nonebot.drivers import Driver, WebSocket
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import RequestDenied
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from .config import Config as MiraiConfig
from .event import Event, FriendMessage, GroupMessage, TempMessage
from .message import MessageChain, MessageSegment


class ActionFailed(BaseActionFailed):

    def __init__(self, code: int, message: str = ''):
        super().__init__('mirai')
        self.code = code
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}(code={self.code}, message={self.message!r})"


class SessionManager:
    sessions: Dict[int, Tuple[str, datetime, httpx.AsyncClient]] = {}
    session_expiry: timedelta = timedelta(minutes=15)

    def __init__(self, session_key: str, client: httpx.AsyncClient):
        self.session_key, self.client = session_key, client

    @staticmethod
    def _raise_code(data: Dict[str, Any]) -> Dict[str, Any]:
        code = data.get('code', 0)
        logger.opt(colors=True).debug('Mirai API returned data: '
                                      f'<y>{escape_tag(str(data))}</y>')
        if code != 0:
            raise ActionFailed(code, message=data['msg'])
        return data

    async def post(self,
                   path: str,
                   *,
                   params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = {**(params or {}), 'sessionKey': self.session_key}
        response = await self.client.post(path, json=params, timeout=3)
        response.raise_for_status()
        return self._raise_code(response.json())

    async def request(self,
                      path: str,
                      *,
                      params: Optional[Dict[str,
                                            Any]] = None) -> Dict[str, Any]:
        response = await self.client.get(path,
                                         params={
                                             **(params or {}), 'sessionKey':
                                                 self.session_key
                                         },
                                         timeout=3)
        response.raise_for_status()
        return self._raise_code(response.json())

    async def upload(self, path: str, *, type: str,
                     file: Tuple[str, BytesIO]) -> Dict[str, Any]:
        file_type, file_io = file
        response = await self.client.post(path,
                                          data={
                                              'sessionKey': self.session_key,
                                              'type': type
                                          },
                                          files={file_type: file_io},
                                          timeout=6)
        response.raise_for_status()
        return self._raise_code(response.json())

    @classmethod
    async def new(cls, self_id: int, *, host: IPv4Address, port: int,
                  auth_key: str):
        session = cls.get(self_id)
        if session is not None:
            return session

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
        if self_id not in cls.sessions:
            return None
        key, time, client = cls.sessions[self_id]
        if datetime.now() - time > cls.session_expiry:
            return None
        return cls(key, client)


class MiraiBot(BaseBot):

    @overrides(BaseBot)
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
    async def call_api(self, api: str, **data) -> NoReturn:
        raise NotImplementedError

    @overrides(BaseBot)
    def __getattr__(self, key: str) -> NoReturn:
        raise NotImplementedError

    @overrides(BaseBot)
    async def send(self,
                   event: Event,
                   message: Union[MessageChain, MessageSegment, str],
                   at_sender: bool = False):
        if isinstance(message, MessageSegment):
            message = MessageChain(message)
        elif isinstance(message, str):
            message = MessageChain(MessageSegment.plain(message))
        if isinstance(event, FriendMessage):
            return await self.send_friend_message(target=event.sender.id,
                                                  message_chain=message)
        elif isinstance(event, GroupMessage):
            if at_sender:
                message = MessageSegment.at(event.sender.id) + message
            return await self.send_group_message(group=event.sender.group.id,
                                                 message_chain=message)
        elif isinstance(event, TempMessage):
            return await self.send_temp_message(qq=event.sender.id,
                                                group=event.sender.group.id,
                                                message_chain=message)
        else:
            raise ValueError(f'Unsupported event type {event!r}.')

    async def send_friend_message(self, target: int,
                                  message_chain: MessageChain):
        return await self.api.post('sendFriendMessage',
                                   params={
                                       'target': target,
                                       'messageChain': message_chain.export()
                                   })

    async def send_temp_message(self, qq: int, group: int,
                                message_chain: MessageChain):
        return await self.api.post('sendTempMessage',
                                   params={
                                       'qq': qq,
                                       'group': group,
                                       'messageChain': message_chain.export()
                                   })

    async def send_group_message(self,
                                 group: int,
                                 message_chain: MessageChain,
                                 quote: Optional[int] = None):
        return await self.api.post('sendGroupMessage',
                                   params={
                                       'group': group,
                                       'messageChain': message_chain.export(),
                                       'quote': quote
                                   })

    async def recall(self, target: int):
        return await self.api.post('recall', params={'target': target})

    async def send_image_message(self, target: int, qq: int, group: int,
                                 urls: List[str]):
        return await self.api.post('sendImageMessage',
                                   params={
                                       'target': target,
                                       'qq': qq,
                                       'group': group,
                                       'urls': urls
                                   })

    async def upload_image(self, type: str, img: BytesIO):
        return await self.api.upload('uploadImage',
                                     type=type,
                                     file=('img', img))

    async def upload_voice(self, type: str, voice: BytesIO):
        return await self.api.upload('uploadVoice',
                                     type=type,
                                     file=('voice', voice))

    async def fetch_message(self):
        return await self.api.request('fetchMessage')

    async def fetch_latest_message(self):
        return await self.api.request('fetchLatestMessage')

    async def peek_message(self, count: int):
        return await self.api.request('peekMessage', params={'count': count})

    async def peek_latest_message(self, count: int):
        return await self.api.request('peekLatestMessage',
                                      params={'count': count})

    async def messsage_from_id(self, id: int):
        return await self.api.request('messageFromId', params={'id': id})

    async def count_message(self):
        return await self.api.request('countMessage')

    async def friend_list(self) -> List[Dict[str, Any]]:
        return await self.api.request('friendList')  # type: ignore

    async def group_list(self) -> List[Dict[str, Any]]:
        return await self.api.request('groupList')  # type: ignore

    async def member_list(self, target: int) -> List[Dict[str, Any]]:
        return await self.api.request('memberList',
                                      params={'target': target})  # type: ignore

    async def mute(self, target: int, member_id: int, time: int):
        return await self.api.post('mute',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'time': time
                                   })

    async def unmute(self, target: int, member_id: int):
        return await self.api.post('unmute',
                                   params={
                                       'target': target,
                                       'memberId': member_id
                                   })

    async def kick(self, target: int, member_id: int, msg: str):
        return await self.api.post('kick',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'msg': msg
                                   })

    async def quit(self, target: int):
        return await self.api.post('quit', params={'target': target})

    async def mute_all(self, target: int):
        return await self.api.post('muteAll', params={'target': target})

    async def unmute_all(self, target: int):
        return await self.api.post('unmuteAll', params={'target': target})

    async def group_config(self, target: int):
        return await self.api.request('groupConfig', params={'target': target})

    async def modify_group_config(self, target: int, config: Dict[str, Any]):
        return await self.api.post('groupConfig',
                                   params={
                                       'target': target,
                                       'config': config
                                   })

    async def member_info(self, target: int, member_id: int):
        return await self.api.request('memberInfo',
                                      params={
                                          'target': target,
                                          'memberId': member_id
                                      })

    async def modify_member_info(self, target: int, member_id: int,
                                 info: Dict[str, Any]):
        return await self.api.post('memberInfo',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'info': info
                                   })
