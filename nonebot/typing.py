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
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Union,
    TypeVar,
    Callable,
    Optional,
    Awaitable,
)

if TYPE_CHECKING:
    from asyncio import Task

    from nonebot.adapters import Bot, Event
    from nonebot.permission import Permission

T_Wrapped = TypeVar("T_Wrapped", bound=Callable)


def overrides(InterfaceClass: object):
    def overrider(func: T_Wrapped) -> T_Wrapped:
        assert func.__name__ in dir(InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


T_State = Dict[Any, Any]
"""
:类型: ``Dict[Any, Any]``

:说明:

  事件处理状态 State 类型
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
    ["Bot", Optional[Exception], str, Dict[str, Any], Any], Awaitable[None]
]
"""
:类型: ``Callable[[Bot, Optional[Exception], str, Dict[str, Any], Any], Awaitable[None]]``

:说明:

  ``bot.call_api`` 后执行的函数，参数分别为 bot, exception, api, data, result
"""

T_EventPreProcessor = Callable[..., Union[None, Awaitable[None]]]
"""
:类型: ``Callable[..., Union[None, Awaitable[None]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  事件预处理函数 EventPreProcessor 类型
"""
T_EventPostProcessor = Callable[..., Union[None, Awaitable[None]]]
"""
:类型: ``Callable[..., Union[None, Awaitable[None]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  事件预处理函数 EventPostProcessor 类型
"""
T_RunPreProcessor = Callable[..., Union[None, Awaitable[None]]]
"""
:类型: ``Callable[..., Union[None, Awaitable[None]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``MatcherParam``: Matcher 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  事件响应器运行前预处理函数 RunPreProcessor 类型
"""
T_RunPostProcessor = Callable[..., Union[None, Awaitable[None]]]
"""
:类型: ``Callable[..., Union[None, Awaitable[None]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``MatcherParam``: Matcher 对象
  * ``ExceptionParam``: 异常对象（可能为 None）
  * ``DefaultParam``: 带有默认值的参数

:说明:

  事件响应器运行前预处理函数 RunPostProcessor 类型，第二个参数为运行时产生的错误（如果存在）
"""

T_RuleChecker = Callable[..., Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[..., Union[bool, Awaitable[bool]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  RuleChecker 即判断是否响应事件的处理函数。
"""
T_PermissionChecker = Callable[..., Union[bool, Awaitable[bool]]]
"""
:类型: ``Callable[..., Union[bool, Awaitable[bool]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  RuleChecker 即判断是否响应消息的处理函数。
"""

T_Handler = Callable[..., Any]
"""
:类型: ``Callable[..., Any]``

:说明:

  Handler 处理函数。
"""
T_TypeUpdater = Callable[..., Union[str, Awaitable[str]]]
"""
:类型: ``Callable[..., Union[None, Awaitable[None]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``MatcherParam``: Matcher 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。默认会更新为 ``message``。
"""
T_PermissionUpdater = Callable[..., Union["Permission", Awaitable["Permission"]]]
"""
:类型: ``Callable[..., Union[Permission, Awaitable[Permission]]]``

:依赖参数:

  * ``DependParam``: 子依赖参数
  * ``BotParam``: Bot 对象
  * ``EventParam``: Event 对象
  * ``StateParam``: State 对象
  * ``MatcherParam``: Matcher 对象
  * ``DefaultParam``: 带有默认值的参数

:说明:

  PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。默认会更新为当前事件的触发对象。
"""
T_DependencyCache = Dict[Callable[..., Any], "Task[Any]"]
"""
:类型: ``Dict[Callable[..., Any], Task[Any]]``
:说明:
  依赖缓存, 用于存储依赖函数的返回值
"""
