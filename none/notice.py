from typing import Dict, Any

from aiocqhttp import CQHttp
from aiocqhttp.bus import EventBus

from .session import BaseSession
from .helpers import make_event_deco
from .logger import logger

_bus = EventBus()
on_notice = make_event_deco('notice', _bus)


class NoticeSession(BaseSession):
    __slots__ = ()

    def __init__(self, bot: CQHttp, ctx: Dict[str, Any]):
        super().__init__(bot, ctx)


async def handle_notice(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    event = f'notice.{ctx["notice_type"]}'
    if ctx.get('sub_type'):
        event += f'.{ctx["sub_type"]}'

    session = NoticeSession(bot, ctx)
    logger.debug(f'Emitting event: {event}')
    await _bus.emit(event, session)
