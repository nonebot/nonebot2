from typing import Callable, Any, Awaitable, Union

ArgFilter_T = Callable[[Any], Union[Any, Awaitable[Any]]]


class ValidateError(ValueError):
    def __init__(self, message=None):
        self.message = message
