#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from types import ModuleType
from typing import NoReturn, TYPE_CHECKING
from typing import Any, Set, List, Dict, Type, Tuple, Mapping
from typing import Union, TypeVar, Optional, Iterable, Callable, Awaitable

# import some modules needed when checking types
if TYPE_CHECKING:
    from nonebot.matcher import Matcher as MatcherClass
    from nonebot.drivers import BaseDriver, BaseWebSocket
    from nonebot.adapters import BaseBot, BaseEvent, BaseMessage, BaseMessageSegment


def overrides(InterfaceClass: object):

    def overrider(func: Callable) -> Callable:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


Driver = TypeVar("Driver", bound="BaseDriver")
WebSocket = TypeVar("WebSocket", bound="BaseWebSocket")

Bot = TypeVar("Bot", bound="BaseBot")
Event = TypeVar("Event", bound="BaseEvent")
Message = TypeVar("Message", bound="BaseMessage")
MessageSegment = TypeVar("MessageSegment", bound="BaseMessageSegment")

PreProcessor = Callable[[Bot, Event], Union[Awaitable[None],
                                            Awaitable[NoReturn]]]

Matcher = TypeVar("Matcher", bound="MatcherClass")
Handler = Callable[[Bot, Event, Dict[Any, Any]], Union[Awaitable[None],
                                                       Awaitable[NoReturn]]]
