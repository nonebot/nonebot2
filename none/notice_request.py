from typing import Dict, Any, Optional, Callable, Union

from aiocqhttp import CQHttp
from aiocqhttp.bus import EventBus

from .session import BaseSession
from .log import logger

_bus = EventBus()


def _make_event_deco(post_type: str) -> Callable:
    def deco_deco(arg: Optional[Union[str, Callable]] = None,
                  *events: str) -> Callable:
        def deco(func: Callable) -> Callable:
            if isinstance(arg, str):
                for e in [arg] + list(events):
                    _bus.subscribe(f'{post_type}.{e}', func)
            else:
                _bus.subscribe(post_type, func)
            return func

        if isinstance(arg, Callable):
            return deco(arg)
        return deco

    return deco_deco


on_notice = _make_event_deco('notice')
on_request = _make_event_deco('request')


class NoticeSession(BaseSession):
    __slots__ = ()

    def __init__(self, bot: CQHttp, ctx: Dict[str, Any]):
        super().__init__(bot, ctx)


class RequestSession(BaseSession):
    __slots__ = ()

    def __init__(self, bot: CQHttp, ctx: Dict[str, Any]):
        super().__init__(bot, ctx)

    # TODO: 添加 approve、deny 等方法


async def handle_notice_or_request(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    post_type = ctx['post_type']  # "notice" or "request"
    detail_type = ctx[f'{post_type}_type']
    event = f'{post_type}.{detail_type}'
    if ctx.get('sub_type'):
        event += f'.{ctx["sub_type"]}'

    if post_type == 'notice':
        session = NoticeSession(bot, ctx)
    else:
        session = RequestSession(bot, ctx)

    logger.debug(f'Emitting event: {event}')
    await _bus.emit(event, session)
