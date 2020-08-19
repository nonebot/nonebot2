#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
类型
====

下面的文档中，「类型」部分使用 Python 的 Type Hint 语法，见 `PEP 484`_、`PEP 526`_ 和 `typing`_。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

以下类型均可从 nonebot.typing 模块导入。

.. _PEP 484:
    https://www.python.org/dev/peps/pep-0484/

.. _PEP 526:
    https://www.python.org/dev/peps/pep-0526/

.. _typing:
    https://docs.python.org/3/library/typing.html
"""

from types import ModuleType
from typing import NoReturn, TYPE_CHECKING
from typing import Any, Set, List, Dict, Type, Tuple, Mapping
from typing import Union, TypeVar, Optional, Iterable, Callable, Awaitable

# import some modules needed when checking types
if TYPE_CHECKING:
    from nonebot.rule import Rule as RuleClass
    from nonebot.matcher import Matcher as MatcherClass
    from nonebot.drivers import BaseDriver, BaseWebSocket
    from nonebot.permission import Permission as PermissionClass
    from nonebot.adapters import BaseBot, BaseEvent, BaseMessage, BaseMessageSegment


def overrides(InterfaceClass: object):

    def overrider(func: Callable) -> Callable:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


Driver = TypeVar("Driver", bound="BaseDriver")
"""
:类型: `BaseDriver`

:说明:

  所有 Driver 的基类。
"""
WebSocket = TypeVar("WebSocket", bound="BaseWebSocket")
"""
:类型: `BaseWebSocket`

:说明:

  所有 WebSocket 的基类。
"""

Bot = TypeVar("Bot", bound="BaseBot")
"""
:类型: `BaseBot`

:说明:

  所有 Bot 的基类。
"""
Event = TypeVar("Event", bound="BaseEvent")
"""
:类型: `BaseEvent`

:说明:

  所有 Event 的基类。
"""
Message = TypeVar("Message", bound="BaseMessage")
"""
:类型: `BaseMessage`

:说明:

  所有 Message 的基类。
"""
MessageSegment = TypeVar("MessageSegment", bound="BaseMessageSegment")
"""
:类型: `BaseMessageSegment`

:说明:

  所有 MessageSegment 的基类。
"""

PreProcessor = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                                  Awaitable[NoReturn]]]
"""
:类型: `Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]`

:说明:

  消息预处理函数 PreProcessor 类型
"""

Matcher = TypeVar("Matcher", bound="MatcherClass")
Handler = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                             Awaitable[NoReturn]]]
Rule = TypeVar("Rule", bound="RuleClass")
RuleChecker = Callable[[Bot, Event, dict], Awaitable[bool]]
Permission = TypeVar("Permission", bound="PermissionClass")
PermissionChecker = Callable[[Bot, Event], Awaitable[bool]]
ArgsParser = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                                Awaitable[NoReturn]]]
