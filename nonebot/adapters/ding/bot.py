import hmac
import base64
from datetime import datetime

import httpx
from nonebot.log import logger
from nonebot.config import Config
from nonebot.adapters import BaseBot
from nonebot.message import handle_event
from nonebot.exception import RequestDenied
from nonebot.typing import Any, Union, Driver, Optional, NoReturn

from .utils import log
from .event import Event
from .model import MessageModel
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed, SessionExpired


class Bot(BaseBot):
    """
    钉钉 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    def __init__(self, driver: Driver, connection_type: str, config: Config,
                 self_id: str, **kwargs):

        super().__init__(driver, connection_type, config, self_id, **kwargs)

    @property
    def type(self) -> str:
        """
        - 返回: ``"ding"``
        """
        return "ding"

    @classmethod
    async def check_permission(cls, driver: Driver, connection_type: str,
                               headers: dict, body: Optional[dict]) -> str:
        """
        :说明:

          钉钉协议鉴权。参考 `鉴权 <https://ding-doc.dingtalk.com/doc#/serverapi2/elzz1p>`_
        """
        timestamp = headers.get("timestamp")
        sign = headers.get("sign")

        # 检查连接方式
        if connection_type not in ["http"]:
            raise RequestDenied(405, "Unsupported connection type")

        # 检查 timestamp
        if not timestamp:
            raise RequestDenied(400, "Missing `timestamp` Header")

        # 检查 sign
        secret = driver.config.secret
        if secret:
            if not sign:
                log("WARNING", "Missing Signature Header")
                raise RequestDenied(400, "Missing `sign` Header")
            string_to_sign = f"{timestamp}\n{secret}"
            sig = hmac.new(secret.encode("utf-8"),
                           string_to_sign.encode("utf-8"), "sha256").digest()
            if sign != base64.b64encode(sig).decode("utf-8"):
                log("WARNING", "Signature Header is invalid")
                raise RequestDenied(403, "Signature is invalid")
        else:
            log("WARNING", "Ding signature check ignored!")
        return body["chatbotUserId"]

    async def handle_message(self, body: dict):
        message = MessageModel.parse_obj(body)
        if not message:
            return

        try:
            event = Event(message)
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )
        return

    async def call_api(self,
                       api: str,
                       event: Optional[Event] = None,
                       **data) -> Union[Any, NoReturn]:
        """
        :说明:

          调用 钉钉 协议 API

        :参数:

          * ``api: str``: API 名称
          * ``**data: Any``: API 参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        if self.connection_type != "http":
            log("ERROR", "Only support http connection.")
            return
        if "self_id" in data:
            self_id = data.pop("self_id")
            if self_id:
                bot = self.driver.bots[str(self_id)]
                return await bot.call_api(api, **data)

        log("DEBUG", f"Calling API <y>{api}</y>")

        if api == "send_message":
            if event:
                # 确保 sessionWebhook 没有过期
                if int(datetime.now().timestamp()) > int(
                        event.raw_event.sessionWebhookExpiredTime / 1000):
                    raise SessionExpired

                target = event.raw_event.sessionWebhook
            else:
                target = None

            if not target:
                raise ApiNotAvailable

            headers = {}
            segment: MessageSegment = data["message"][0]
            try:
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.post(
                        target,
                        params={"access_token": self.config.access_token},
                        json=segment.data,
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

    async def send(self,
                   event: Event,
                   message: Union[str, "Message", "MessageSegment"],
                   at_sender: bool = False,
                   **kwargs) -> Union[Any, NoReturn]:
        """
        :说明:

          根据 ``event``  向触发事件的主体发送消息。

        :参数:

          * ``event: Event``: Event 对象
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体
          * ``**kwargs``: 覆盖默认参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``ValueError``: 缺少 ``user_id``, ``group_id``
          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        msg = message if isinstance(message, Message) else Message(message)

        at_sender = at_sender and bool(event.user_id)
        params = {}
        params["event"] = event
        params.update(kwargs)

        if at_sender and event.detail_type != "private":
            params["message"] = f"@{event.user_id} " + msg
        else:
            params["message"] = msg

        return await self.call_api("send_message", **params)
