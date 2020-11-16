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
    from nonebot.drivers import BaseDriver, BaseWebSocket
    from nonebot.permission import Permission as PermissionClass
    from nonebot.adapters import BaseBot, BaseEvent, BaseMessage, BaseMessageSegment
    from nonebot.matcher import Matcher as MatcherClass, MatcherGroup as MatcherGroupClass


def overrides(InterfaceClass: object):

    def overrider(func: Callable) -> Callable:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


Driver = TypeVar("Driver", bound="BaseDriver")
"""
:类型: ``BaseDriver``

:说明:

  所有 Driver 的基类。
"""
WebSocket = TypeVar("WebSocket", bound="BaseWebSocket")
"""
:类型: ``BaseWebSocket``

:说明:

  所有 WebSocket 的基类。
"""

Bot = TypeVar("Bot", bound="BaseBot")
"""
:类型: ``BaseBot``

:说明:

  所有 Bot 的基类。
"""
Event = TypeVar("Event", bound="BaseEvent")
"""
:类型: ``BaseEvent``

:说明:

  所有 Event 的基类。
"""
Message = TypeVar("Message", bound="BaseMessage")
"""
:类型: ``BaseMessage``

:说明:

  所有 Message 的基类。
"""
MessageSegment = TypeVar("MessageSegment", bound="BaseMessageSegment")
"""
:类型: ``BaseMessageSegment``

:说明:

  所有 MessageSegment 的基类。
"""

EventPreProcessor = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                                       Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  事件预处理函数 EventPreProcessor 类型
"""
EventPostProcessor = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                                        Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  事件预处理函数 EventPostProcessor 类型
"""
RunPreProcessor = Callable[["Matcher", Bot, Event, dict],
                           Union[Awaitable[None], Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Matcher, Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  事件响应器运行前预处理函数 RunPreProcessor 类型
"""
RunPostProcessor = Callable[["Matcher", Optional[Exception], Bot, Event, dict],
                            Union[Awaitable[None], Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Matcher, Optional[Exception], Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  事件响应器运行前预处理函数 RunPostProcessor 类型，第二个参数为运行时产生的错误（如果存在）
"""

Matcher = TypeVar("Matcher", bound="MatcherClass")
"""
:类型: ``Matcher``

:说明:

  Matcher 即响应事件的处理类。通过 Rule 判断是否响应事件，运行 Handler。
"""
MatcherGroup = TypeVar("MatcherGroup", bound="MatcherGroupClass")
"""
:类型: ``MatcherGroup``

:说明:

  MatcherGroup 为 Matcher 的集合。可以共享 Handler。
"""
Rule = TypeVar("Rule", bound="RuleClass")
"""
:类型: ``Rule``

:说明:

  Rule 即判断是否响应事件的处理类。内部存储 RuleChecker ，返回全为 True 则响应事件。
"""
RuleChecker = Callable[[Bot, Event, dict], Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event, dict], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应事件的处理函数。
"""
Permission = TypeVar("Permission", bound="PermissionClass")
"""
:类型: ``Permission``

:说明:

  Permission 即判断是否响应消息的处理类。内部存储 PermissionChecker ，返回只要有一个 True 则响应消息。
"""
PermissionChecker = Callable[[Bot, Event], Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应消息的处理函数。
"""
Handler = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                             Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  Handler 即事件的处理函数。
"""
ArgsParser = Callable[[Bot, Event, dict], Union[Awaitable[None],
                                                Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  ArgsParser 即消息参数解析函数，在 Matcher.got 获取参数时被运行。
"""
