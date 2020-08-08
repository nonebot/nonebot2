#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from types import ModuleType
from typing import TYPE_CHECKING
from typing import Any, Set, List, Dict, Type, Tuple, Mapping
from typing import Union, Optional, Iterable, Callable, Awaitable

# import some modules needed when checking types
if TYPE_CHECKING:
    from nonebot.adapters import BaseBot as Bot
    from nonebot.event import Event


def overrides(InterfaceClass: object):

    def overrider(func: Callable) -> Callable:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


Handler = Callable[["Bot", "Event", dict], Awaitable[None]]
