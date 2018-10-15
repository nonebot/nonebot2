from . import NoneBot
from .helpers import send, send_expr
from .typing import Context_T, Message_T, Expression_T


class BaseSession:
    __slots__ = ('bot', 'ctx')

    def __init__(self, bot: NoneBot, ctx: Context_T):
        self.bot = bot
        self.ctx = ctx

    async def send(self, message: Message_T, *,
                   ignore_failure: bool = True) -> None:
        """Send a message ignoring failure by default."""
        return await send(self.bot, self.ctx, message,
                          ignore_failure=ignore_failure)

    async def send_expr(self, expr: Expression_T, **kwargs):
        """Sending a expression message ignoring failure by default."""
        return await send_expr(self.bot, self.ctx, expr, **kwargs)
