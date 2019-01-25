from typing import Optional

from nonebot.typing import Message_T


class ValidateError(ValueError):
    def __init__(self, message: Optional[Message_T] = None):
        self.message = message
