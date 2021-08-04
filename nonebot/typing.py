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
from collections.abc import Callable as BaseCallable
from typing import Any, Dict, Union, TypeVar, Optional, Callable, NoReturn, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from nonebot.matcher import Matcher
    from nonebot.adapters import Bot, Event
    from nonebot.permission import Permission

T_Wrapped = TypeVar("T_Wrapped", bound=BaseCallable)


def overrides(InterfaceClass: object):

    def overrider(func: T_Wrapped) -> T_Wrapped:
        assert func.__name__ in dir(
            InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


T_State = Dict[Any, Any]
"""
:类型: ``Dict[Any, Any]``

:说明:

  事件处理状态 State 类型
"""
T_StateFactory = Callable[["Bot", "Event"], Awaitable[T_State]]
"""
:类型: ``Callable[[Bot, Event], Awaitable[T_State]]``

:说明:

  事件处理状态 State 类工厂函数
"""

T_BotConnectionHook = Callable[["Bot"], Awaitable[None]]
"""
:类型: ``Callable[[Bot], Awaitable[None]]``

:说明:

  Bot 连接建立时执行的函数
"""
T_BotDisconnectionHook = Callable[["Bot"], Awaitable[None]]
"""
:类型: ``Callable[[Bot], Awaitable[None]]``

:说明:

  Bot 连接断开时执行的函数
"""
T_CallingAPIHook = Callable[["Bot", str, Dict[str, Any]], Awaitable[None]]
"""
:类型: ``Callable[[Bot, str, Dict[str, Any]], Awaitable[None]]``

:说明:

  ``bot.call_api`` 时执行的函数
"""
T_CalledAPIHook = Callable[
    ["Bot", Optional[Exception], str, Dict[str, Any], Any], Awaitable[None]]
"""
:类型: ``Callable[[Bot, Optional[Exception], str, Dict[str, Any], Any], Awaitable[None]]``

:说明:

  ``bot.call_api`` 后执行的函数，参数分别为 bot, exception, api, data, result
"""

T_EventPreProcessor = Callable[["Bot", "Event", T_State], Awaitable[None]]
"""
:类型: ``Callable[[Bot, Event, T_State], Awaitable[None]]``

:说明:

  事件预处理函数 EventPreProcessor 类型
"""
T_EventPostProcessor = Callable[["Bot", "Event", T_State], Awaitable[None]]
"""
:类型: ``Callable[[Bot, Event, T_State], Awaitable[None]]``

:说明:

  事件预处理函数 EventPostProcessor 类型
"""
T_RunPreProcessor = Callable[["Matcher", "Bot", "Event", T_State],
                             Awaitable[None]]
"""
:类型: ``Callable[[Matcher, Bot, Event, T_State], Awaitable[None]]``

:说明:

  事件响应器运行前预处理函数 RunPreProcessor 类型
"""
T_RunPostProcessor = Callable[
    ["Matcher", Optional[Exception], "Bot", "Event", T_State], Awaitable[None]]
"""
:类型: ``Callable[[Matcher, Optional[Exception], Bot, Event, T_State], Awaitable[None]]``

:说明:

  事件响应器运行前预处理函数 RunPostProcessor 类型，第二个参数为运行时产生的错误（如果存在）
"""

T_RuleChecker = Callable[["Bot", "Event", T_State], Union[bool,
                                                          Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event, T_State], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应事件的处理函数。
"""
T_PermissionChecker = Callable[["Bot", "Event"], Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[[Bot, Event], Union[bool, Awaitable[bool]]]``

:说明:

  RuleChecker 即判断是否响应消息的处理函数。
"""

T_Handler = Union[Callable[[Any, Any, Any, Any], Union[Awaitable[None],
                                                       Awaitable[NoReturn]]],
                  Callable[[Any, Any, Any], Union[Awaitable[None],
                                                  Awaitable[NoReturn]]],
                  Callable[[Any, Any], Union[Awaitable[None],
                                             Awaitable[NoReturn]]],
                  Callable[[Any], Union[Awaitable[None], Awaitable[NoReturn]]]]
"""
:类型:

  * ``Callable[[Bot, Event, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]``
  * ``Callable[[Bot, Event], Union[Awaitable[None], Awaitable[NoReturn]]]``
  * ``Callable[[Bot, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]``
  * ``Callable[[Bot], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  Handler 即事件的处理函数。
"""
T_ArgsParser = Callable[["Bot", "Event", T_State], Union[Awaitable[None],
                                                         Awaitable[NoReturn]]]
"""
:类型: ``Callable[[Bot, Event, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]``

:说明:

  ArgsParser 即消息参数解析函数，在 Matcher.got 获取参数时被运行。
"""
T_TypeUpdater = Callable[["Bot", "Event", T_State, str], Awaitable[str]]
"""
:类型: ``Callable[[Bot, Event, T_State, str], Awaitable[str]]``

:说明:

  TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。默认会更新为 ``message``。
"""
T_PermissionUpdater = Callable[["Bot", "Event", T_State, "Permission"],
                               Awaitable["Permission"]]
"""
:类型: ``Callable[[Bot, Event, T_State, Permission], Awaitable[Permission]]``

:说明:

  PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。默认会更新为当前事件的触发对象。
"""
