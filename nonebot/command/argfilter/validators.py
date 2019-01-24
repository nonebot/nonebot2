import re
from typing import Callable, Any

from nonebot.command.argfilter import ValidateError


class BaseValidator:
    def __init__(self, message=None):
        self.message = message

    def raise_failure(self):
        raise ValidateError(self.message)


class not_empty(BaseValidator):
    """
    Validate any object to ensure it's not empty (is None or has no elements).
    """

    def __call__(self, value):
        if value is None:
            self.raise_failure()
        if hasattr(value, '__len__') and value.__len__() == 0:
            self.raise_failure()
        return value


class fit_size(BaseValidator):
    """
    Validate any sized object to ensure the size/length
    is in a given range [min_length, max_length].
    """

    def __init__(self, min_length: int = 0, max_length: int = None,
                 message=None):
        super().__init__(message)
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value):
        length = len(value) if value is not None else 0
        if length < self.min_length or \
                (self.max_length is not None and length > self.max_length):
            self.raise_failure()
        return value


class match_regex(BaseValidator):
    """
    Validate any string object to ensure it matches a given pattern.
    """

    def __init__(self, pattern: str, message=None, *, flags=0,
                 fullmatch: bool = False):
        super().__init__(message)
        self.pattern = re.compile(pattern, flags)
        self.fullmatch = fullmatch

    def __call__(self, value):
        if self.fullmatch:
            if not re.fullmatch(self.pattern, value):
                self.raise_failure()
        else:
            if not re.match(self.pattern, value):
                self.raise_failure()
        return value


class ensure_true(BaseValidator):
    """
    Validate any object to ensure the result of applying
    a boolean function to it is True.
    """

    def __init__(self, bool_func: Callable[[Any], bool], message=None):
        super().__init__(message)
        self.bool_func = bool_func

    def __call__(self, value):
        if self.bool_func(value) is not True:
            self.raise_failure()
        return value


class between_inclusive(BaseValidator):
    """
    Validate any comparable object to ensure it's between
    `start` and `end` inclusively.
    """

    def __init__(self, start=None, end=None, message=None):
        super().__init__(message)
        self.start = start
        self.end = end

    def __call__(self, value):
        if self.start is not None and value < self.start:
            self.raise_failure()
        if self.end is not None and self.end < value:
            self.raise_failure()
        return value
