import json
import urllib.parse

import time
from datetime import datetime
from typing import Any, Tuple, Union, Optional, TYPE_CHECKING

import httpx

from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Driver, HTTPConnection, HTTPRequest, HTTPResponse

from .utils import calc_hmac_base64, log
from .config import Config as DingConfig
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed, SessionExpired
from .event import MessageEvent, PrivateMessageEvent, GroupMessageEvent, ConversationType

if TYPE_CHECKING:
    from nonebot.config import Config

SEND = "send"


class Bot(BaseBot):
    """
    钉钉 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """
    ding_config: DingConfig

    @property
    def type(self) -> str:
        """
        - 返回: ``"ding"``
        """
        return "ding"

    @classmethod
    def register(cls, driver: Driver, config: "Config"):
        super().register(driver, config)
        cls.ding_config = DingConfig(**config.dict())

    @classmethod
    @overrides(BaseBot)
    async def check_permission(
            cls, driver: Driver,
            request: HTTPConnection) -> Tuple[Optional[str], HTTPResponse]:
        """
        :说明:

          钉钉协议鉴权。参考 `鉴权 <https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p>`_
        """
        timestamp = request.headers.get("timestamp")
        sign = request.headers.get("sign")

        # 检查连接方式
        if not isinstance(request, HTTPRequest):
            return None, HTTPResponse(
                405, b"Unsupported connection type, available type: `http`")

        # 检查 timestamp
        if not timestamp:
            return None, HTTPResponse(400, b"Missing `timestamp` Header")

        # 检查 sign
        secret = cls.ding_config.secret
        if secret:
            if not sign:
                log("WARNING", "Missing Signature Header")
                return None, HTTPResponse(400, b"Missing `sign` Header")
            sign_base64 = calc_hmac_base64(str(timestamp), secret)
            if sign != sign_base64.decode('utf-8'):
                log("WARNING", "Signature Header is invalid")
                return None, HTTPResponse(403, b"Signature is invalid")
        else:
            log("WARNING", "Ding signature check ignored!")
        return (json.loads(request.body.decode())["chatbotUserId"],
                HTTPResponse(204, b''))

    @overrides(BaseBot)
    async def handle_message(self, message: bytes):
        data = json.loads(message)

        if not data:
            return

        # 判断消息类型，生成不同的 Event
        try:
            conversation_type = data["conversationType"]
            if conversation_type == ConversationType.private:
                event = PrivateMessageEvent.parse_obj(data)
            elif conversation_type == ConversationType.group:
                event = GroupMessageEvent.parse_obj(data)
            else:
                raise ValueError("Unsupported conversation type")
        except Exception as e:
            log("ERROR", "Event Parser Error", e)
            return

        try:
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {data}</bg #f8bbd0></r>"
            )
        return

    @overrides(BaseBot)
    async def _call_api(self,
                        api: str,
                        event: Optional[MessageEvent] = None,
                        **data) -> Any:
        if self.connection_type != "http":
            log("ERROR", "Only support http connection.")
            return

        log("DEBUG", f"Calling API <y>{api}</y>")
        params = {}
        # 传入参数有 webhook，则使用传入的 webhook
        webhook = data.get("webhook")

        if webhook:
            secret = data.get("secret")
            if secret:
                # 有这个参数的时候再计算加签的值
                timestamp = str(round(time.time() * 1000))
                params["timestamp"] = timestamp
                hmac_code_base64 = calc_hmac_base64(timestamp, secret)
                sign = urllib.parse.quote_plus(hmac_code_base64)
                params["sign"] = sign
        else:
            # webhook 不存在则使用 event 中的 sessionWebhook
            if event:
                # 确保 sessionWebhook 没有过期
                if int(datetime.now().timestamp()) > int(
                        event.sessionWebhookExpiredTime / 1000):
                    raise SessionExpired

                webhook = event.sessionWebhook
            else:
                raise ApiNotAvailable

        headers = {}
        message: Message = data.get("message", None)
        if not message:
            raise ValueError("Message not found")
        try:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(webhook,
                                             params=params,
                                             json=message._produce(),
                                             timeout=self.config.api_timeout)

            if 200 <= response.status_code < 300:
                result = response.json()
                if isinstance(result, dict):
                    if result.get("errcode") != 0:
                        raise ActionFailed(errcode=result.get("errcode"),
                                           errmsg=result.get("errmsg"))
                    return result
            raise NetworkError(f"HTTP request received unexpected "
                               f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    @overrides(BaseBot)
    async def call_api(self,
                       api: str,
                       event: Optional[MessageEvent] = None,
                       **data) -> Any:
        """
        :说明:

          调用 钉钉 协议 API

        :参数:

          * ``api: str``: API 名称
          * ``event: Optional[MessageEvent]``: Event 对象
          * ``**data: Any``: API 参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        return await super().call_api(api, event=event, **data)

    @overrides(BaseBot)
    async def send(self,
                   event: MessageEvent,
                   message: Union[str, "Message", "MessageSegment"],
                   at_sender: bool = False,
                   webhook: Optional[str] = None,
                   secret: Optional[str] = None,
                   **kwargs) -> Any:
        """
        :说明:

          根据 ``event``  向触发事件的主体发送消息。

        :参数:

          * ``event: Event``: Event 对象
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体
          * ``webhook: Optional[str]``: 该条消息将调用的 webhook 地址。不传则将使用 sessionWebhook，若其也不存在，该条消息不发送，使用自定义 webhook 时注意你设置的安全方式，如加关键词，IP地址，加签等等。
          * ``secret: Optional[str]``: 如果你使用自定义的 webhook 地址，推荐使用加签方式对消息进行验证，将 `机器人安全设置页面，加签一栏下面显示的SEC开头的字符串` 传入这个参数即可。
          * ``**kwargs``: 覆盖默认参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``ValueError``: 缺少 ``user_id``, ``group_id``
          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        msg = message if isinstance(message, Message) else Message(message)

        at_sender = at_sender and bool(event.senderId)
        params = {}
        params["event"] = event
        if webhook:
            params["webhook"] = webhook
            params["secret"] = secret
        params.update(kwargs)

        if at_sender and event.conversationType != ConversationType.private:
            params[
                "message"] = f"@{event.senderId} " + msg + MessageSegment.atDingtalkIds(
                    event.senderId)
        else:
            params["message"] = msg

        return await self.call_api(SEND, **params)
