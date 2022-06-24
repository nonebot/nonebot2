"""本模块定义了 NoneBot 模块中共享的一些类型。

下面的文档中，「类型」部分使用 Python 的 Type Hint 语法，
参考 [`PEP 484`](https://www.python.org/dev/peps/pep-0484/),
[`PEP 526`](https://www.python.org/dev/peps/pep-0526/) 和
[`typing`](https://docs.python.org/3/library/typing.html)。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

FrontMatter:
    sidebar_position: 11
    description: nonebot.typing 模块
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

    from nonebot.adapters import Bot
    from nonebot.permission import Permission

T_Wrapped = TypeVar("T_Wrapped", bound=Callable)


def overrides(InterfaceClass: object) -> Callable[[T_Wrapped], T_Wrapped]:
    """标记一个方法为父类 interface 的 implement"""

    def overrider(func: T_Wrapped) -> T_Wrapped:
        assert func.__name__ in dir(InterfaceClass), f"Error method: {func.__name__}"
        return func

    return overrider


T_State = Dict[Any, Any]
"""事件处理状态 State 类型"""

T_BotConnectionHook = Callable[..., Awaitable[Any]]
"""Bot 连接建立时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""
T_BotDisconnectionHook = Callable[..., Awaitable[Any]]
"""Bot 连接断开时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""
T_CallingAPIHook = Callable[["Bot", str, Dict[str, Any]], Awaitable[Any]]
"""`bot.call_api` 钩子函数"""
T_CalledAPIHook = Callable[
    ["Bot", Optional[Exception], str, Dict[str, Any], Any], Awaitable[Any]
]
"""`bot.call_api` 后执行的函数，参数分别为 bot, exception, api, data, result"""

T_EventPreProcessor = Callable[..., Union[Any, Awaitable[Any]]]
"""事件预处理函数 EventPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_EventPostProcessor = Callable[..., Union[Any, Awaitable[Any]]]
"""事件预处理函数 EventPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_RunPreProcessor = Callable[..., Union[Any, Awaitable[Any]]]
"""事件响应器运行前预处理函数 RunPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_RunPostProcessor = Callable[..., Union[Any, Awaitable[Any]]]
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

T_RuleChecker = Callable[..., Union[bool, Awaitable[bool]]]
"""RuleChecker 即判断是否响应事件的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_PermissionChecker = Callable[..., Union[bool, Awaitable[bool]]]
"""PermissionChecker 即判断事件是否满足权限的处理函数。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- DefaultParam: 带有默认值的参数
"""

T_Handler = Callable[..., Any]
"""Handler 处理函数。"""
T_TypeUpdater = Callable[..., Union[str, Awaitable[str]]]
"""TypeUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新响应的事件类型。默认会更新为 `message`。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_PermissionUpdater = Callable[..., Union["Permission", Awaitable["Permission"]]]
"""PermissionUpdater 在 Matcher.pause, Matcher.reject 时被运行，用于更新会话对象权限。默认会更新为当前事件的触发对象。

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_DependencyCache = Dict[Callable[..., Any], "Task[Any]"]
"""依赖缓存, 用于存储依赖函数的返回值"""
