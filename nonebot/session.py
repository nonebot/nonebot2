from aiocqhttp import Event as CQEvent

from . import NoneBot
from .helpers import send
from .typing import Message_T


class BaseSession:
    __slots__ = ('bot', 'event')

    def __init__(self, bot: NoneBot, event: CQEvent):
        self.bot = bot
        self.event = event

    @property
    def ctx(self) -> CQEvent:
        return self.event

    @ctx.setter
    def ctx(self, val: CQEvent) -> None:
        self.event = val

    @property
    def self_id(self) -> int:
        return self.event.self_id

    async def send(self,
                   message: Message_T,
                   *,
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
        return await send(self.bot,
                          self.event,
                          message,
                          at_sender=at_sender,
                          ensure_private=ensure_private,
                          ignore_failure=ignore_failure,
                          **kwargs)
