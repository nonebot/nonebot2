from datetime import datetime, timedelta
from functools import wraps
from io import BytesIO
from ipaddress import IPv4Address
from typing import (Any, Dict, List, NoReturn, Optional, Tuple, Union)

import httpx

from nonebot.adapters import Bot as BaseBot
from nonebot.config import Config
from nonebot.drivers import Driver, WebSocket
from nonebot.exception import ApiNotAvailable, RequestDenied
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from .config import Config as MiraiConfig
from .event import Event, FriendMessage, GroupMessage, TempMessage
from .message import MessageChain, MessageSegment
from .utils import catch_network_error, argument_validation, check_tome, Log


class SessionManager:
    """Bot会话管理器, 提供API主动调用接口"""
    sessions: Dict[int, Tuple[str, datetime, httpx.AsyncClient]] = {}
    session_expiry: timedelta = timedelta(minutes=15)

    def __init__(self, session_key: str, client: httpx.AsyncClient):
        self.session_key, self.client = session_key, client

    @catch_network_error
    async def post(self,
                   path: str,
                   *,
                   params: Optional[Dict[str, Any]] = None) -> Any:
        """
        :说明:

          以POST方式主动提交API请求

        :参数:

          * ``path: str``: 对应API路径
          * ``params: Optional[Dict[str, Any]]``: 请求参数 (无需sessionKey)

        :返回:

          - ``Dict[str, Any]``: API 返回值
        """
        response = await self.client.post(
            path,
            json={
                **(params or {}),
                'sessionKey': self.session_key,
            },
            timeout=3,
        )
        response.raise_for_status()
        return response.json()

    @catch_network_error
    async def request(self,
                      path: str,
                      *,
                      params: Optional[Dict[str, Any]] = None) -> Any:
        """
        :说明:

          以GET方式主动提交API请求

        :参数:

          * ``path: str``: 对应API路径
          * ``params: Optional[Dict[str, Any]]``: 请求参数 (无需sessionKey)
        """
        response = await self.client.get(
            path,
            params={
                **(params or {}),
                'sessionKey': self.session_key,
            },
            timeout=3,
        )
        response.raise_for_status()
        return response.json()

    @catch_network_error
    async def upload(self, path: str, *, params: Dict[str, Any]) -> Any:
        """
        :说明:

            以表单(``multipart/form-data``)形式主动提交API请求

        :参数:

            * ``path: str``: 对应API路径
            * ``params: Dict[str, Any]``: 请求参数 (无需sessionKey)
        """
        files = {k: v for k, v in params.items() if isinstance(v, BytesIO)}
        form = {k: v for k, v in params.items() if k not in files}
        response = await self.client.post(
            path,
            data=form,
            files=files,
            timeout=6,
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    async def new(cls, self_id: int, *, host: IPv4Address, port: int,
                  auth_key: str) -> "SessionManager":
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
    def get(cls,
            self_id: int,
            check_expire: bool = True) -> Optional["SessionManager"]:
        if self_id not in cls.sessions:
            return None
        key, time, client = cls.sessions[self_id]
        if check_expire and (datetime.now() - time > cls.session_expiry):
            return None
        return cls(key, client)


class Bot(BaseBot):
    """
    mirai-api-http 协议 Bot 适配。

    \:\:\: warning
    API中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

    部分字段可能与文档在符号上不一致
    \:\:\:

    """

    @overrides(BaseBot)
    def __init__(self,
                 connection_type: str,
                 self_id: str,
                 *,
                 websocket: Optional[WebSocket] = None):
        super().__init__(connection_type, self_id, websocket=websocket)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        return "mirai"

    @property
    def alive(self) -> bool:
        return not self.websocket.closed

    @property
    def api(self) -> SessionManager:
        """返回该Bot对象的会话管理实例以提供API主动调用"""
        api = SessionManager.get(self_id=int(self.self_id))
        assert api is not None, 'SessionManager has not been initialized'
        return api

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
        if (cls.mirai_config.auth_key and cls.mirai_config.host and
                cls.mirai_config.port) is None:
            raise ApiNotAvailable('mirai')
        super().register(driver, config)

    @overrides(BaseBot)
    async def handle_message(self, message: dict):
        Log.debug(f'received message {message}')
        try:
            await handle_event(
                bot=self,
                event=await check_tome(
                    bot=self,
                    event=Event.new({
                        **message,
                        'self_id': self.self_id,
                    }),
                ),
            )
        except Exception as e:
            logger.opt(colors=True, exception=e).exception(
                'Failed to handle message '
                f'<r>{escape_tag(str(message))}</r>: ')

    @overrides(BaseBot)
    async def call_api(self, api: str, **data) -> NoReturn:
        """
        \:\:\: danger
        由于Mirai的HTTP API特殊性, 该API暂时无法实现
        \:\:\:
        
        \:\:\: tip
        你可以使用 ``MiraiBot.api`` 中提供的调用方法来代替
        \:\:\:
        """
        raise NotImplementedError

    @overrides(BaseBot)
    def __getattr__(self, key: str) -> NoReturn:
        """由于Mirai的HTTP API特殊性, 该API暂时无法实现"""
        raise NotImplementedError

    @overrides(BaseBot)
    @argument_validation
    async def send(self,
                   event: Event,
                   message: Union[MessageChain, MessageSegment, str],
                   at_sender: bool = False):
        """
        :说明:

          根据 ``event`` 向触发事件的主体发送信息

        :参数:

          * ``event: Event``: Event对象
          * ``message: Union[MessageChain, MessageSegment, str]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体
        """
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

    @argument_validation
    async def send_friend_message(self, target: int,
                                  message_chain: MessageChain):
        """
        :说明:

          使用此方法向指定好友发送消息

        :参数:

          * ``target: int``: 发送消息目标好友的 QQ 号
          * ``message_chain: MessageChain``: 消息链，是一个消息对象构成的数组
        """
        return await self.api.post('sendFriendMessage',
                                   params={
                                       'target': target,
                                       'messageChain': message_chain.export()
                                   })

    @argument_validation
    async def send_temp_message(self, qq: int, group: int,
                                message_chain: MessageChain):
        """
        :说明:

          使用此方法向临时会话对象发送消息

        :参数:

          * ``qq: int``: 临时会话对象 QQ 号
          * ``group: int``: 临时会话群号
          * ``message_chain: MessageChain``: 消息链，是一个消息对象构成的数组
        """
        return await self.api.post('sendTempMessage',
                                   params={
                                       'qq': qq,
                                       'group': group,
                                       'messageChain': message_chain.export()
                                   })

    @argument_validation
    async def send_group_message(self,
                                 group: int,
                                 message_chain: MessageChain,
                                 quote: Optional[int] = None):
        """
        :说明:

          使用此方法向指定群发送消息

        :参数:

          * ``group: int``: 发送消息目标群的群号
          * ``message_chain: MessageChain``: 消息链，是一个消息对象构成的数组
          * ``quote: Optional[int]``: 引用一条消息的 message_id 进行回复
        """
        return await self.api.post('sendGroupMessage',
                                   params={
                                       'group': group,
                                       'messageChain': message_chain.export(),
                                       'quote': quote
                                   })

    @argument_validation
    async def recall(self, target: int):
        """
        :说明:

          使用此方法撤回指定消息。对于bot发送的消息，有2分钟时间限制。对于撤回群聊中群员的消息，需要有相应权限

        :参数:

          * ``target: int``: 需要撤回的消息的message_id
        """
        return await self.api.post('recall', params={'target': target})

    @argument_validation
    async def send_image_message(self, target: int, qq: int, group: int,
                                 urls: List[str]) -> List[str]:
        """
        :说明:

          使用此方法向指定对象（群或好友）发送图片消息
          除非需要通过此手段获取image_id，否则不推荐使用该接口

          > 当qq和group同时存在时，表示发送临时会话图片，qq为临时会话对象QQ号，group为临时会话发起的群号

        :参数:

          * ``target: int``: 发送对象的QQ号或群号，可能存在歧义
          * ``qq: int``: 发送对象的QQ号
          * ``group: int``: 发送对象的群号
          * ``urls: List[str]``: 是一个url字符串构成的数组

        :返回:

          - ``List[str]``: 一个包含图片imageId的数组
        """
        return await self.api.post('sendImageMessage',
                                   params={
                                       'target': target,
                                       'qq': qq,
                                       'group': group,
                                       'urls': urls
                                   })

    @argument_validation
    async def upload_image(self, type: str, img: BytesIO):
        """
        :说明:

           使用此方法上传图片文件至服务器并返回Image_id

        :参数:

          * ``type: str``: "friend" 或 "group" 或 "temp"
          * ``img: BytesIO``: 图片的BytesIO对象
        """
        return await self.api.upload('uploadImage',
                                     params={
                                         'type': type,
                                         'img': img
                                     })

    @argument_validation
    async def upload_voice(self, type: str, voice: BytesIO):
        """
        :说明:

          使用此方法上传语音文件至服务器并返回voice_id

        :参数:

          * ``type: str``: 当前仅支持 "group"
          * ``voice: BytesIO``: 语音的BytesIO对象
        """
        return await self.api.upload('uploadVoice',
                                     params={
                                         'type': type,
                                         'voice': voice
                                     })

    @argument_validation
    async def fetch_message(self, count: int = 10):
        """
        :说明:

          使用此方法获取bot接收到的最老消息和最老各类事件
          (会从MiraiApiHttp消息记录中删除)

        :参数:

          * ``count: int``: 获取消息和事件的数量
        """
        return await self.api.request('fetchMessage', params={'count': count})

    @argument_validation
    async def fetch_latest_message(self, count: int = 10):
        """
        :说明:

          使用此方法获取bot接收到的最新消息和最新各类事件
          (会从MiraiApiHttp消息记录中删除)

        :参数:

          * ``count: int``: 获取消息和事件的数量
        """
        return await self.api.request('fetchLatestMessage',
                                      params={'count': count})

    @argument_validation
    async def peek_message(self, count: int = 10):
        """
        :说明:

          使用此方法获取bot接收到的最老消息和最老各类事件
          (不会从MiraiApiHttp消息记录中删除) 

        :参数:

          * ``count: int``: 获取消息和事件的数量
        """
        return await self.api.request('peekMessage', params={'count': count})

    @argument_validation
    async def peek_latest_message(self, count: int = 10):
        """
        :说明:

          使用此方法获取bot接收到的最新消息和最新各类事件
          (不会从MiraiApiHttp消息记录中删除)
        
        :参数:

          * ``count: int``: 获取消息和事件的数量
        """
        return await self.api.request('peekLatestMessage',
                                      params={'count': count})

    @argument_validation
    async def messsage_from_id(self, id: int):
        """
        :说明:

          通过messageId获取一条被缓存的消息
          使用此方法获取bot接收到的消息和各类事件

        :参数:

          * ``id: int``: 获取消息的message_id
        """
        return await self.api.request('messageFromId', params={'id': id})

    @argument_validation
    async def count_message(self):
        """
        :说明:

          使用此方法获取bot接收并缓存的消息总数，注意不包含被删除的
        """
        return await self.api.request('countMessage')

    @argument_validation
    async def friend_list(self) -> List[Dict[str, Any]]:
        """
        :说明:

          使用此方法获取bot的好友列表

        :返回:

          - ``List[Dict[str, Any]]``: 返回的好友列表数据
        """
        return await self.api.request('friendList')

    @argument_validation
    async def group_list(self) -> List[Dict[str, Any]]:
        """
        :说明:

          使用此方法获取bot的群列表

        :返回:

          - ``List[Dict[str, Any]]``: 返回的群列表数据
        """
        return await self.api.request('groupList')

    @argument_validation
    async def member_list(self, target: int) -> List[Dict[str, Any]]:
        """
        :说明:

          使用此方法获取bot指定群种的成员列表

        :参数:

          * ``target: int``: 指定群的群号

        :返回:

          - ``List[Dict[str, Any]]``: 返回的群成员列表数据
        """
        return await self.api.request('memberList', params={'target': target})

    @argument_validation
    async def mute(self, target: int, member_id: int, time: int):
        """
        :说明:

          使用此方法指定群禁言指定群员（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
          * ``member_id: int``: 指定群员QQ号
          * ``time: int``: 禁言时长，单位为秒，最多30天
        """
        return await self.api.post('mute',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'time': time
                                   })

    @argument_validation
    async def unmute(self, target: int, member_id: int):
        """
        :说明:

          使用此方法指定群解除群成员禁言（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
          * ``member_id: int``: 指定群员QQ号
        """
        return await self.api.post('unmute',
                                   params={
                                       'target': target,
                                       'memberId': member_id
                                   })

    @argument_validation
    async def kick(self, target: int, member_id: int, msg: str):
        """
        :说明:

          使用此方法移除指定群成员（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
          * ``member_id: int``: 指定群员QQ号
          * ``msg: str``: 信息
        """
        return await self.api.post('kick',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'msg': msg
                                   })

    @argument_validation
    async def quit(self, target: int):
        """
        :说明:

          使用此方法使Bot退出群聊 

        :参数:

          * ``target: int``: 退出的群号
        """
        return await self.api.post('quit', params={'target': target})

    @argument_validation
    async def mute_all(self, target: int):
        """
        :说明:

          使用此方法令指定群进行全体禁言（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
        """
        return await self.api.post('muteAll', params={'target': target})

    @argument_validation
    async def unmute_all(self, target: int):
        """
        :说明:

          使用此方法令指定群解除全体禁言（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
        """
        return await self.api.post('unmuteAll', params={'target': target})

    @argument_validation
    async def group_config(self, target: int):
        """
        :说明:

          使用此方法获取群设置

        :参数:

          * ``target: int``: 指定群的群号

        :返回:

        .. code-block:: json

            {
                "name": "群名称",
                "announcement": "群公告",
                "confessTalk": true,
                "allowMemberInvite": true,
                "autoApprove": true,
                "anonymousChat": true
            }
        """
        return await self.api.request('groupConfig', params={'target': target})

    @argument_validation
    async def modify_group_config(self, target: int, config: Dict[str, Any]):
        """
        :说明:

          使用此方法修改群设置（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
          * ``config: Dict[str, Any]``: 群设置, 格式见 ``group_config`` 的返回值
        """
        return await self.api.post('groupConfig',
                                   params={
                                       'target': target,
                                       'config': config
                                   })

    @argument_validation
    async def member_info(self, target: int, member_id: int):
        """
        :说明:

          使用此方法获取群员资料

        :参数:

          * ``target: int``: 指定群的群号
          * ``member_id: int``: 群员QQ号

        :返回:

        .. code-block:: json

            {
                "name": "群名片",
                "specialTitle": "群头衔"
            }
        """
        return await self.api.request('memberInfo',
                                      params={
                                          'target': target,
                                          'memberId': member_id
                                      })

    @argument_validation
    async def modify_member_info(self, target: int, member_id: int,
                                 info: Dict[str, Any]):
        """
        :说明:

          使用此方法修改群员资料（需要有相关权限）

        :参数:

          * ``target: int``: 指定群的群号
          * ``member_id: int``: 群员QQ号
          * ``info: Dict[str, Any]``: 群员资料, 格式见 ``member_info`` 的返回值
        """
        return await self.api.post('memberInfo',
                                   params={
                                       'target': target,
                                       'memberId': member_id,
                                       'info': info
                                   })
