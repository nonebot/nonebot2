"""本模块定义了 NoneBot 模块中共享的一些类型。

使用 Python 的 Type Hint 语法，
参考 [`PEP 484`](https://www.python.org/dev/peps/pep-0484/),
[`PEP 526`](https://www.python.org/dev/peps/pep-0526/) 和
[`typing`](https://docs.python.org/3/library/typing.html)。

FrontMatter:
    sidebar_position: 11
    description: nonebot.typing 模块
"""

import warnings
from typing_extensions import ParamSpec, TypeAlias, override
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

    from nonebot.adapters import Bot
    from nonebot.permission import Permission

T = TypeVar("T")
P = ParamSpec("P")

T_Wrapped: TypeAlias = Callable[P, T]


def overrides(InterfaceClass: object):
    """标记一个方法为父类 interface 的 implement"""

    warnings.warn(
        "overrides is deprecated and will be removed in a future version, "
        "use @typing_extensions.override instead. "
        "See [PEP 698](https://peps.python.org/pep-0698/) for more details.",
        DeprecationWarning,
    )
    return override


# state
T_State: TypeAlias = Dict[Any, Any]
"""事件处理状态 State 类型"""

_DependentCallable: TypeAlias = Union[Callable[..., T], Callable[..., Awaitable[T]]]

# driver hooks
T_BotConnectionHook: TypeAlias = _DependentCallable[Any]
"""Bot 连接建立时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""
T_BotDisconnectionHook: TypeAlias = _DependentCallable[Any]
"""Bot 连接断开时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""

# api hooks
T_CallingAPIHook: TypeAlias = Callable[["Bot", str, Dict[str, Any]], Awaitable[Any]]
"""`bot.call_api` 钩子函数"""
T_CalledAPIHook: TypeAlias = Callable[
    ["Bot", Optional[Exception], str, Dict[str, Any], Any], Awaitable[Any]
]
"""`bot.call_api` 后执行的函数，参数分别为 bot, exception, api, data, result"""

# event hooks
T_EventPreProcessor: TypeAlias = _DependentCallable[Any]
"""事件预处理函数 EventPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_EventPostProcessor: TypeAlias = _DependentCallable[Any]
"""事件预处理函数 EventPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""

# matcher run hooks
T_RunPreProcessor: TypeAlias = _DependentCallable[Any]
"""事件响应器运行前预处理函数 RunPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_RunPostProcessor: TypeAlias = _DependentCallable[Any]
"""事件响应器运行后后处理函数 RunPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- ExceptionParam: 异常对象（可能为 None）
- DefaultParam: 带有默认值的参数
"""

# rule, permission
T_RuleChecker: TypeAlias = _DependentCallable[bool]
"""RuleChecker 即判断是否响应事件的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_PermissionChecker: TypeAlias = _DependentCallable[bool]
"""PermissionChecker 即判断事件是否满足权限的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- DefaultParam: 带有默认值的参数
"""

T_Handler: TypeAlias = _DependentCallable[Any]
"""Handler 处理函数。"""
T_TypeUpdater: TypeAlias = _DependentCallable[str]
"""TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。
默认会更新为 `message`。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_PermissionUpdater: TypeAlias = _DependentCallable["Permission"]
"""PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。
默认会更新为当前事件的触发对象。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_DependencyCache: TypeAlias = Dict[_DependentCallable[Any], "Task[Any]"]
"""依赖缓存, 用于存储依赖函数的返回值"""
