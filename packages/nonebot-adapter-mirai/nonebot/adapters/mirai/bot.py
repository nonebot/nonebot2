import asyncio
import json
import sys
from typing import Any, Dict, Optional, Tuple, Union, cast

import httpx
from loguru import logger

from nonebot.adapters import Bot as BaseBot
from nonebot.config import Config
from nonebot.drivers import (Driver, ForwardDriver, HTTPConnection,
                             HTTPResponse, ReverseDriver, WebSocket,
                             WebSocketSetup)
from nonebot.exception import ApiNotAvailable
from nonebot.typing import overrides

from .config import Config as MiraiConfig
from .event import Event, FriendMessage, GroupMessage, TempMessage
from .exception import ActionFailed
from .message import MessageChain, MessageSegment
from .utils import Log, process_event, MiraiDataclassEncoder


class SyncIDStore:
    _sync_id = 0
    _futures: Dict[str, asyncio.Future] = {}

    @classmethod
    def get_id(cls) -> str:
        sync_id = cls._sync_id
        cls._sync_id = (cls._sync_id + 1) % sys.maxsize
        return str(sync_id)

    @classmethod
    def add_response(cls, response: Dict[str, Any]):
        if not isinstance(response.get('syncId'), str):
            return
        sync_id: str = response['syncId']
        if sync_id in cls._futures:
            cls._futures[sync_id].set_result(response)
        return sync_id

    @classmethod
    async def fetch_response(cls, sync_id: str,
                             timeout: Optional[float]) -> Dict[str, Any]:
        future = asyncio.get_running_loop().create_future()
        cls._futures[sync_id] = future
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise ApiNotAvailable('timeout') from None
        finally:
            del cls._futures[sync_id]


class Bot(BaseBot):
    r"""
    mirai-api-http 协议 Bot 适配。

    \:\:\: warning
    API中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

    部分字段可能与文档在符号上不一致
    \:\:\:

    """

    _type = 'mirai'

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        return self._type

    @classmethod
    @overrides(BaseBot)
    async def check_permission(
            cls, driver: Driver,
            request: HTTPConnection) -> Tuple[Optional[str], HTTPResponse]:
        if isinstance(request, WebSocket):
            return None, HTTPResponse(
                501, b'Websocket connection is not implemented')
        self_id: Optional[str] = request.headers.get('bot')
        if self_id is None:
            return None, HTTPResponse(400, b'Header `Bot` is required.')
        self_id = str(self_id).strip()

        return self_id, HTTPResponse(204, b'')

    @classmethod
    @overrides(BaseBot)
    def register(cls, driver: Driver, config: "Config"):
        cls.mirai_config = MiraiConfig(**config.dict())
        super().register(driver, config)

        if not isinstance(driver, ForwardDriver) and cls.mirai_config.ws_urls:
            logger.warning(
                f"Current driver {cls.config.driver} don't support forward connections"
            )
        elif isinstance(driver, ForwardDriver) and cls.mirai_config.ws_urls:
            for url, user_id in cls.mirai_config.ws_urls.items():
                user_id = [user_id] if isinstance(user_id, int) else user_id
                for self_id in user_id:
                    connect_url = httpx.URL(
                        url,
                        params={
                            'verifyKey': cls.mirai_config.verify_key,
                            'qq': self_id
                        },
                        path='/all')
                    setup = WebSocketSetup(
                        adapter='mirai',
                        self_id=str(self_id),
                        url=str(connect_url),
                    )
                    driver.setup_websocket(setup)

        elif isinstance(driver, ReverseDriver):
            logger.debug(
                'Param "qq" does not set for mirai adapter, use http post instead'
            )

    @overrides(BaseBot)
    async def handle_message(self, message: bytes):
        try:
            data: Dict[str, Any] = json.loads(message)

            if int(data.get('syncId') or '0') >= 0:
                SyncIDStore.add_response(data)
                return

            await process_event(
                bot=self,
                event=Event.new({
                    **data['data'],
                    'self_id': self.self_id,
                }),
            )
        except Exception as e:
            Log.error(f'Failed to handle message: {message}', e)

    @overrides(BaseBot)
    async def _call_api(self, api: str, **data) -> Any:

        def snake_to_camel(name: str):
            first, *rest = name.split('_')
            return ''.join([first.lower(), *(r.title() for r in rest)])

        sync_id = SyncIDStore.get_id()
        api = snake_to_camel(api)
        data = {snake_to_camel(k): v for k, v in data.items()}
        body = {
            'syncId': sync_id,
            'command': api,
            'subcommand': None,
            'content': {
                **data,
            },
        }
        await cast(WebSocket, self.request).send(
            json.dumps(
                body,
                cls=MiraiDataclassEncoder,
            ))
        result: Dict[str, Any] = await SyncIDStore.fetch_response(
            sync_id, timeout=self.config.api_timeout)

        if ('data' not in result) or (result['data'].get('code') != 0):
            raise ActionFailed(**(result.get('data') or result))

        return result['data']

    @overrides(BaseBot)
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
        if not isinstance(message, MessageChain):
            message = MessageChain(message)
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
