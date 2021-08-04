import json
import re
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union

import httpx
from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer

from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Driver, HTTPRequest, HTTPResponse
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides

from .config import Config as FeishuConfig
from .event import (Event, GroupMessageEvent, MessageEvent,
                    PrivateMessageEvent, get_event_model)
from .exception import ActionFailed, ApiNotAvailable, NetworkError
from .message import Message, MessageSegment, MessageSerializer
from .utils import AESCipher, log

if TYPE_CHECKING:
    from nonebot.config import Config


def _check_at_me(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头或结尾是否存在 @机器人，去除并赋值 ``event.reply``, ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if not isinstance(event, MessageEvent):
        return

    message = event.get_message()
    # ensure message not empty
    if not message:
        message.append(MessageSegment.text(""))

    if event.event.message.chat_type == "p2p":
        event.to_me = True

        for index, segment in enumerate(message):
            if segment.type == "at" and segment.data.get(
                    "user_name") in bot.config.nickname:
                event.to_me = True
                del event.event.message.content[index]
                return
            elif segment.type == "text" and segment.data.get("mentions"):
                for mention in segment.data["mentions"].values():
                    if mention["name"] in bot.config.nickname:
                        event.to_me = True
                        segment.data["text"] = segment.data["text"].replace(
                            f"@{mention['name']}", "")
                        segment.data["text"] = segment.data["text"].lstrip()
                        break
                else:
                    continue
                break

        if not message:
            message.append(MessageSegment.text(""))


def _check_nickname(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头是否存在昵称，去除并赋值 ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if not isinstance(event, MessageEvent):
        return

    first_msg_seg = event.get_message()[0]
    if first_msg_seg.type != "text":
        return

    first_text = first_msg_seg.data["text"]

    nicknames = set(filter(lambda n: n, bot.config.nickname))
    if nicknames:
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        m = re.search(rf"^({nickname_regex})([\s,，]*|$)", first_text,
                      re.IGNORECASE)
        if m:
            nickname = m.group(1)
            log("DEBUG", f"User is calling me {nickname}")
            event.to_me = True
            first_msg_seg.data["text"] = first_text[m.end():]


def _handle_api_result(result: Optional[Dict[str, Any]]) -> Any:
    """
    :说明:

      处理 API 请求返回值。

    :参数:

      * ``result: Optional[Dict[str, Any]]``: API 返回数据

    :返回:

        - ``Any``: API 调用返回数据

    :异常:

        - ``ActionFailed``: API 调用失败
    """
    if isinstance(result, dict):
        if result.get("code") != 0:
            raise ActionFailed(**result)
        return result.get("data")


class Bot(BaseBot):
    """
    飞书 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    @property
    def type(self) -> str:
        return "feishu"

    @property
    def api_root(self) -> str:
        return "https://open.feishu.cn/open-apis/"

    @classmethod
    def register(cls, driver: Driver, config: "Config"):
        super().register(driver, config)
        cls.feishu_config = FeishuConfig(**config.dict())

    @classmethod
    @overrides(BaseBot)
    async def check_permission(
            cls, driver: Driver, request: HTTPRequest
    ) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        if not isinstance(request, HTTPRequest):
            log("WARNING",
                "Unsupported connection type, available type: `http`")
            return None, HTTPResponse(
                405, b"Unsupported connection type, available type: `http`")

        encrypt_key = cls.feishu_config.encrypt_key
        if encrypt_key:
            encrypted = json.loads(request.body)["encrypt"]
            decrypted = AESCipher(encrypt_key).decrypt_string(encrypted)
            data = json.loads(decrypted)
        else:
            data = json.loads(request.body)

        challenge = data.get("challenge")
        if challenge:
            return data.get("token"), HTTPResponse(
                200,
                json.dumps({
                    "challenge": challenge
                }).encode())

        schema = data.get("schema")
        if not schema:
            return None, HTTPResponse(
                400,
                b"Missing `schema` in POST body, only accept event of version 2.0"
            )

        headers = data.get("header")
        if headers:
            token = headers.get("token")
            app_id = headers.get("app_id")
        else:
            log("WARNING", "Missing `header` in POST body")
            return None, HTTPResponse(400, b"Missing `header` in POST body")

        if not token:
            log("WARNING", "Missing `verification token` in POST body")
            return None, HTTPResponse(
                400, b"Missing `verification token` in POST body")
        else:
            if token != cls.feishu_config.verification_token:
                log("WARNING", "Verification token check failed")
                return None, HTTPResponse(403,
                                          b"Verification token check failed")

        return app_id, HTTPResponse(200, b'')

    async def handle_message(self, message: bytes):
        """
        :说明:

          处理事件并转换为 `Event <#class-event>`_
        """
        data = json.loads(message)
        if data.get("type") == "url_verification":
            return

        try:
            header = data["header"]
            event_type = header["event_type"]
            if data.get("event"):
                if data["event"].get("message"):
                    event_type += f".{data['event']['message']['chat_type']}"

            models = get_event_model(event_type)
            for model in models:
                try:
                    event = model.parse_obj(data)
                    break
                except Exception as e:
                    log("DEBUG", "Event Parser Error", e)
            else:
                event = Event.parse_obj(data)

            _check_at_me(self, event)
            _check_nickname(self, event)

            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    def _construct_url(self, path: str) -> str:
        return self.api_root + path

    @cached(ttl=60 * 60,
            cache=Cache.MEMORY,
            key="_feishu_tenant_access_token",
            serializer=PickleSerializer())
    async def _fetch_tenant_access_token(self) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._construct_url(
                        "auth/v3/tenant_access_token/internal/"),
                    json={
                        "app_id": self.feishu_config.app_id,
                        "app_secret": self.feishu_config.app_secret
                    },
                    timeout=self.config.api_timeout)

            if 200 <= response.status_code < 300:
                result = response.json()
                return result["tenant_access_token"]
            else:
                raise NetworkError(f"HTTP request received unexpected "
                                   f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    @overrides(BaseBot)
    async def _call_api(self, api: str, **data) -> Any:
        log("DEBUG", f"Calling API <y>{api}</y>")
        if isinstance(self.request, HTTPRequest):
            if not self.api_root:
                raise ApiNotAvailable

            headers = {}
            self.feishu_config.tenant_access_token = await self._fetch_tenant_access_token(
            )
            headers[
                "Authorization"] = "Bearer " + self.feishu_config.tenant_access_token

            try:
                async with httpx.AsyncClient(
                        timeout=self.config.api_timeout) as client:
                    response = await client.send(
                        httpx.Request(data["method"],
                                      self.api_root + api,
                                      json=data.get("body", {}),
                                      params=data.get("query", {}),
                                      headers=headers))
                if 200 <= response.status_code < 300:
                    result = response.json()
                    return _handle_api_result(result)
                raise NetworkError(f"HTTP request received unexpected "
                                   f"status code: {response.status_code} "
                                   f"response body: {response.text}")
            except httpx.InvalidURL:
                raise NetworkError("API root url invalid")
            except httpx.HTTPError:
                raise NetworkError("HTTP request failed")

    @overrides(BaseBot)
    async def call_api(self, api: str, **data) -> Any:
        """
        :说明:

          调用 飞书 协议 API

        :参数:

          * ``api: str``: API 名称
          * ``**data: Any``: API 参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        return await super().call_api(api, **data)

    @overrides(BaseBot)
    async def send(self,
                   event: Event,
                   message: Union[str, Message, MessageSegment],
                   at_sender: bool = False,
                   **kwargs) -> Any:
        msg = message if isinstance(message, Message) else Message(message)

        if isinstance(event, GroupMessageEvent):
            receive_id, receive_id_type = event.event.message.chat_id, 'chat_id'
        elif isinstance(event, PrivateMessageEvent):
            receive_id, receive_id_type = event.get_user_id(), 'union_id'
        else:
            raise ValueError(
                "Cannot guess `receive_id` and `receive_id_type` to reply!")

        at_sender = at_sender and bool(event.get_user_id())

        if at_sender and receive_id_type != "union_id":
            msg = MessageSegment.at(event.get_user_id()) + " " + msg

        msg_type, content = MessageSerializer(msg).serialize()

        params = {
            "method": "POST",
            "query": {
                "receive_id_type": receive_id_type
            },
            "body": {
                "receive_id": receive_id,
                "content": content,
                "msg_type": msg_type
            }
        }

        return await self.call_api(f"im/v1/messages", **params)
