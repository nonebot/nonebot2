"""本模块定义了 NoneBot 模块中共享的一些类型。

使用 Python 的 Type Hint 语法，
参考 [`PEP 484`](https://www.python.org/dev/peps/pep-0484/),
[`PEP 526`](https://www.python.org/dev/peps/pep-0526/) 和
[`typing`](https://docs.python.org/3/library/typing.html)。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 11
    description: nonebot.typing 模块
"""

import sys
import types
import typing as t
from typing import TYPE_CHECKING, TypeVar
import typing_extensions as t_ext
from typing_extensions import ParamSpec, TypeAlias, get_args, get_origin, override
import warnings

if TYPE_CHECKING:
    from nonebot.adapters import Bot
    from nonebot.internal.params import DependencyCache
    from nonebot.permission import Permission

T = TypeVar("T")
P = ParamSpec("P")

T_Wrapped: TypeAlias = t.Callable[P, T]


def overrides(InterfaceClass: object):
    """标记一个方法为父类 interface 的 implement"""

    warnings.warn(
        "overrides is deprecated and will be removed in a future version, "
        "use @typing_extensions.override instead. "
        "See [PEP 698](https://peps.python.org/pep-0698/) for more details.",
        DeprecationWarning,
    )
    return override


if sys.version_info < (3, 10):

    def type_has_args(type_: type[t.Any]) -> bool:
        """判断类型是否有参数"""
        return isinstance(type_, (t._GenericAlias, types.GenericAlias))  # type: ignore

else:

    def type_has_args(type_: type[t.Any]) -> bool:
        return isinstance(type_, (t._GenericAlias, types.GenericAlias, types.UnionType))  # type: ignore


if sys.version_info < (3, 10):

    def origin_is_union(origin: t.Optional[type[t.Any]]) -> bool:
        """判断是否是 Union 类型"""
        return origin is t.Union

else:

    def origin_is_union(origin: t.Optional[type[t.Any]]) -> bool:
        return origin is t.Union or origin is types.UnionType


def origin_is_literal(origin: t.Optional[type[t.Any]]) -> bool:
    """判断是否是 Literal 类型"""
    return origin is t.Literal or origin is t_ext.Literal


def _literal_values(type_: type[t.Any]) -> tuple[t.Any, ...]:
    return get_args(type_)


def all_literal_values(type_: type[t.Any]) -> list[t.Any]:
    """获取 Literal 类型包含的所有值"""
    if not origin_is_literal(get_origin(type_)):
        return [type_]

    return [x for value in _literal_values(type_) for x in all_literal_values(value)]


def origin_is_annotated(origin: t.Optional[type[t.Any]]) -> bool:
    """判断是否是 Annotated 类型"""
    return origin is t_ext.Annotated


NONE_TYPES = {None, type(None), t.Literal[None], t_ext.Literal[None]}
if sys.version_info >= (3, 10):
    NONE_TYPES.add(types.NoneType)


def is_none_type(type_: type[t.Any]) -> bool:
    """判断是否是 None 类型"""
    return type_ in NONE_TYPES


if sys.version_info < (3, 12):

    def is_type_alias_type(type_: type[t.Any]) -> bool:
        """判断是否是 TypeAliasType 类型"""
        return isinstance(type_, t_ext.TypeAliasType)
else:

    def is_type_alias_type(type_: type[t.Any]) -> bool:
        return isinstance(type_, (t.TypeAliasType, t_ext.TypeAliasType))


def evaluate_forwardref(
    ref: t.ForwardRef, globalns: dict[str, t.Any], localns: dict[str, t.Any]
) -> t.Any:
    # Python 3.13/3.12.4+ made `recursive_guard` a kwarg,
    # so name it explicitly to avoid:
    # TypeError: ForwardRef._evaluate()
    # missing 1 required keyword-only argument: 'recursive_guard'
    return ref._evaluate(globalns, localns, recursive_guard=frozenset())


# state
# use annotated flag to avoid ForwardRef recreate generic type (py >= 3.11)
class StateFlag:
    def __repr__(self) -> str:
        return "StateFlag()"


_STATE_FLAG = StateFlag()

T_State: TypeAlias = t.Annotated[dict[t.Any, t.Any], _STATE_FLAG]
"""事件处理状态 State 类型"""

_DependentCallable: TypeAlias = t.Union[
    t.Callable[..., T], t.Callable[..., t.Awaitable[T]]
]

# driver hooks
T_BotConnectionHook: TypeAlias = _DependentCallable[t.Any]
"""Bot 连接建立时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""
T_BotDisconnectionHook: TypeAlias = _DependentCallable[t.Any]
"""Bot 连接断开时钩子函数

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- DefaultParam: 带有默认值的参数
"""

# api hooks
T_CallingAPIHook: TypeAlias = t.Callable[
    ["Bot", str, dict[str, t.Any]], t.Awaitable[t.Any]
]
"""`bot.call_api` 钩子函数"""
T_CalledAPIHook: TypeAlias = t.Callable[
    ["Bot", t.Optional[Exception], str, dict[str, t.Any], t.Any], t.Awaitable[t.Any]
]
"""`bot.call_api` 后执行的函数，参数分别为 bot, exception, api, data, result"""

# event hooks
T_EventPreProcessor: TypeAlias = _DependentCallable[t.Any]
"""事件预处理函数 EventPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""
T_EventPostProcessor: TypeAlias = _DependentCallable[t.Any]
"""事件后处理函数 EventPostProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- DefaultParam: 带有默认值的参数
"""

# matcher run hooks
T_RunPreProcessor: TypeAlias = _DependentCallable[t.Any]
"""事件响应器运行前预处理函数 RunPreProcessor 类型

依赖参数:

- DependParam: 子依赖参数
- BotParam: Bot 对象
- EventParam: Event 对象
- StateParam: State 对象
- MatcherParam: Matcher 对象
- DefaultParam: 带有默认值的参数
"""
T_RunPostProcessor: TypeAlias = _DependentCallable[t.Any]
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

T_Handler: TypeAlias = _DependentCallable[t.Any]
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
T_DependencyCache: TypeAlias = dict[_DependentCallable[t.Any], "DependencyCache"]
"""依赖缓存, 用于存储依赖函数的返回值"""
