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

from typing import Any, Dict, Union, Optional, Callable, NoReturn, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event
    from nonebot.matcher import Matcher


def overrides(InterfaceClass: object):

    def overrider(func: Callable) -> Callable:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


State = Dict[Any, Any]
"""
:类型: ``Dict[Any, Any]``

:说明:

  事件处理状态 State 类型
"""
EventPreProcessor = Callable[["Bot", "Event", State], Awaitable[None]]
"""
:类型: ``Callable[[Bot, Event, State], Awaitable[None]]``

:说明:

  事件预处理函数 EventPreProcessor 类型
"""
EventPostProcessor = Callable[["Bot", "Event", State], Awaitable[None]]
"""
:类型: ``Callable[[Bot, Event, State], Awaitable[None]]``

:说明:

  事件预处理函数 EventPostProcessor 类型
"""
RunPreProcessor = Callable[["Matcher", "Bot", "Event", State], Awaitable[None]]
"""
:类型: ``Callable[[Matcher, Bot, Event, State], Awaitable[None]]``

:说明:

  事件响应器运行前预处理函数 RunPreProcessor 类型
"""
RunPostProcessor = Callable[
    ["Matcher", Optional[Exception], "Bot", "Event", State], Awaitable[None]]
"""
:类型: ``Callable[[Matcher, Optional[Exception], Bot, Event, State], Awaitable[None]]``

:说明:

  事件响应器运行前预处理函数 RunPostProcessor 类型，第二个参数为运行时产生的错误（如果存在）
"""

RuleChecker = Callable[["Bot", "Event", State], Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event, State], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应事件的处理函数。
"""
PermissionChecker = Callable[["Bot", "Event"], Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应消息的处理函数。
"""
Handler = Callable[["Bot", "Event", State], Union[Awaitable[None],
                                                  Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, State], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  Handler 即事件的处理函数。
"""
ArgsParser = Callable[["Bot", "Event", State], Union[Awaitable[None],
                                                     Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, State], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  ArgsParser 即消息参数解析函数，在 Matcher.got 获取参数时被运行。
"""
