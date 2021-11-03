import json
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union

import httpx

from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import (
    Driver,
    ForwardDriver,
    HTTPConnection,
    HTTPPollingSetup,
    HTTPResponse,
)
from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.typing import overrides

from .config import Config as TelegramConfig
from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.config import Config


class Bot(BaseBot):
    """
    telegram bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    telegram_config: TelegramConfig
    username: str
    update_offset: int = 0

    def __init__(self, self_id: str, request: HTTPConnection):
        super().__init__(self_id, request)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        """
        - 返回: ``"telegram"``
        """
        return "telegram"

    @classmethod
    def register(cls, driver: "Driver", config: "Config"):
        super().register(driver, config)
        cls.telegram_config = TelegramConfig(**config.dict())

        logger.info("Delete old webhook")
        httpx.post(
            f"{cls.telegram_config.api_server}bot{cls.telegram_config.token}/deleteWebhook"
        )

        if isinstance(driver, ForwardDriver) and cls.telegram_config.url:
            logger.info("Set new webhook")
            httpx.post(
                f"{cls.telegram_config.api_server}bot{cls.telegram_config.token}/setWebhook",
                params={"url": f"{cls.telegram_config.url}/telegram/http"},
            )
        else:
            logger.info("Start poll")
            res = httpx.post(
                f"{cls.telegram_config.api_server}bot{cls.telegram_config.token}/getUpdates"
            ).json()["result"]
            if res:
                cls.update_offset = res[-1]["update_id"]
            driver.setup_http_polling(
                HTTPPollingSetup(
                    "telegram",
                    cls.telegram_config.token.split(":", maxsplit=1)[0],
                    f"{cls.telegram_config.api_server}bot{cls.telegram_config.token}/getUpdates",
                    "post",
                    b"",
                    {},
                    "1.1",
                    0.1,
                )
            )

    @classmethod
    async def check_permission(
        cls, driver: Driver, request: HTTPConnection
    ) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        """
        Telegram 的 Webhook 方式完全不带机器人本身的标识符，所以只能默认所有上报都通过
        """
        cls.username = httpx.post(
            f"{cls.telegram_config.api_server}bot{cls.telegram_config.token}/getMe"
        ).json()["result"]["username"]

        return cls.telegram_config.token.split(":", maxsplit=1)[0], HTTPResponse(200)

    async def handle_message(self, message: bytes):
        message: dict = json.loads(message)
        if "update_id" in message:
            await self._handle_message(message)
        else:
            for msg in message["result"]:
                if msg["update_id"] > self.update_offset:
                    self.update_offset = msg["update_id"]
                    await self._handle_message(msg)

    async def _handle_message(self, message: Dict[str, Any]):
        try:
            event = Event.parse_event(message)
            event.self_username = self.username
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    async def _call_api(self, api: str, **data) -> Any:
        # 将方法名称改为驼峰式
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )

        async with httpx.AsyncClient(
            proxies=self.telegram_config.proxy, timeout=10
        ) as client:
            response = await client.post(
                f"{self.telegram_config.api_server}bot{self.telegram_config.token}/{api}",
                json=data,
            )
        return response.text

    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs
    ) -> Any:
        """
        TODO

        由于 Telegram 对于不同类型的消息有不同的 API，如果需要批量发送不同类型的消息请尽量使用此方法，Nonebot 将会自动帮你转换成多条消息。
        """
        if isinstance(message, str):
            response = await self.send_message(chat_id=event.chat.id, text=message)
        elif isinstance(message, MessageSegment):
            if message.type == "text":
                response = await self.send_message(
                    chat_id=event.chat.id, text=message.data.get("text")
                )
        else:
            for seg in message:
                if seg.type == "text":
                    response = await self.send_message(
                        chat_id=event.chat.id, text=seg.data.get("text")
                    )
        return response
