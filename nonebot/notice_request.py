from typing import Optional, Callable, Union

from aiocqhttp.bus import EventBus

from . import NoneBot
from .exceptions import CQHttpError
from .log import logger
from .session import BaseSession
from .typing import Context_T

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

    def __init__(self, bot: NoneBot, ctx: Context_T):
        super().__init__(bot, ctx)


class RequestSession(BaseSession):
    __slots__ = ()

    def __init__(self, bot: NoneBot, ctx: Context_T):
        super().__init__(bot, ctx)

    async def approve(self, remark: str = '') -> None:
        """
        Approve the request.

        :param remark: remark of friend (only works in friend request)
        """
        try:
            await self.bot.call_action(
                action='.handle_quick_operation_async',
                self_id=self.ctx.get('self_id'),
                context=self.ctx,
                operation={'approve': True, 'remark': remark}
            )
        except CQHttpError:
            pass

    async def reject(self, reason: str = '') -> None:
        """
        Reject the request.

        :param reason: reason to reject (only works in group request)
        """
        try:
            await self.bot.call_action(
                action='.handle_quick_operation_async',
                self_id=self.ctx.get('self_id'),
                context=self.ctx,
                operation={'approve': False, 'reason': reason}
            )
        except CQHttpError:
            pass


async def handle_notice_or_request(bot: NoneBot, ctx: Context_T) -> None:
    post_type = ctx['post_type']  # "notice" or "request"
    detail_type = ctx[f'{post_type}_type']
    event = f'{post_type}.{detail_type}'
    if ctx.get('sub_type'):
        event += f'.{ctx["sub_type"]}'

    if post_type == 'notice':
        _log_notice(ctx)
        session = NoticeSession(bot, ctx)
    else:  # must be 'request'
        _log_request(ctx)
        session = RequestSession(bot, ctx)

    logger.debug(f'Emitting event: {event}')
    try:
        await _bus.emit(event, session)
    except Exception as e:
        logger.error(f'An exception occurred while handling event {event}:')
        logger.exception(e)


def _log_notice(ctx: Context_T) -> None:
    logger.info(f'Notice: {ctx}')


def _log_request(ctx: Context_T) -> None:
    logger.info(f'Request: {ctx}')
