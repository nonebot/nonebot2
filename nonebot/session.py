from . import NoneBot
from .helpers import send
from .typing import Context_T, Message_T


class BaseSession:
    __slots__ = ('bot', 'ctx')

    def __init__(self, bot: NoneBot, ctx: Context_T):
        self.bot = bot
        self.ctx = ctx

    @property
    def self_id(self) -> int:
        return self.ctx['self_id']

    async def send(self, message: Message_T, *,
                   at_sender: bool = False,
                   ensure_private: bool = False,
                   ignore_failure: bool = True,
                   **kwargs) -> None:
        """
        Send a message ignoring failure by default.

        :param message: message to send
        :param at_sender: @ the sender if in group or discuss chat
        :param ensure_private: ensure the message is sent to private chat
        :param ignore_failure: if any CQHttpError raised, ignore it
        :return: the result returned by CQHTTP
        """
        return await send(self.bot, self.ctx, message,
                          at_sender=at_sender,
                          ensure_private=ensure_private,
                          ignore_failure=ignore_failure, **kwargs)
