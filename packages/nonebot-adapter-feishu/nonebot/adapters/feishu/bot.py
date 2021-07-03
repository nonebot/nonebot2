import json

from typing import Any, Tuple, Union, Optional, TYPE_CHECKING

from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Driver, HTTPRequest, HTTPResponse

from .config import Config as FeishuConfig
from .event import Event
from .message import Message, MessageSegment
from .utils import log, AESCipher

if TYPE_CHECKING:
    from nonebot.config import Config


class Bot(BaseBot):
    """
    飞书 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    @property
    def type(self) -> str:
        return "feishu"

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
            return None, HTTPResponse(
                200,
                json.dumps({
                    "challenge": challenge
                }).encode())

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
        try:
            event = Event.parse_obj(message)
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    async def _call_api(self, api: str, **data) -> Any:
        raise NotImplementedError

    async def send(self, event: Event, message: Union[str, Message,
                                                      MessageSegment],
                   **kwargs) -> Any:
        raise NotImplementedError
