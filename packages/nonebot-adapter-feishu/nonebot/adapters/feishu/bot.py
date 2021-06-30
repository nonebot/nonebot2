from typing import Any, Union, Optional, TYPE_CHECKING

from nonebot.log import logger
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import RequestDenied

from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from nonebot.drivers import Driver


class Bot(BaseBot):
    """
    飞书 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    @property
    def type(self) -> str:
        return "feishu"

    @classmethod
    async def check_permission(cls, driver: "Driver", connection_type: str,
                               headers: dict, body: Optional[dict]) -> str:
        # raise RequestDenied(401, "reason")
        return "bot id"

    async def handle_message(self, message: dict):
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
