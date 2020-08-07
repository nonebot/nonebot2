#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from types import ModuleType
from typing import TYPE_CHECKING
from typing import Any, Set, List, Dict, Type, Tuple, Mapping
from typing import Union, Optional, Iterable, Callable, Awaitable

if TYPE_CHECKING:
    from nonebot.adapters import BaseBot as Bot
    from nonebot.event import Event

Handler = Callable[["Bot", "Event", dict], Awaitable[None]]
