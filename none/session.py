from typing import Union, Callable, Dict, Any, List, Sequence

from aiocqhttp import CQHttp

from .helpers import send, send_expr


class BaseSession:
    __slots__ = ('bot', 'ctx')

    def __init__(self, bot: CQHttp, ctx: Dict[str, Any]):
        self.bot = bot
        self.ctx = ctx

    async def send(self,
                   message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
                   *, ignore_failure: bool = True) -> None:
        return await send(self.bot, self.ctx, message,
                          ignore_failure=ignore_failure)

    async def send_expr(self,
                        expr: Union[str, Sequence[str], Callable],
                        **kwargs):
        return await send_expr(self.bot, self.ctx, expr, **kwargs)
