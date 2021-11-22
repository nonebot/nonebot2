r"""
权限
====

每个 ``Matcher`` 拥有一个 ``Permission`` ，其中是 ``PermissionChecker`` 的集合，只要有一个 ``PermissionChecker`` 检查结果为 ``True`` 时就会继续运行。

\:\:\:tip 提示
``PermissionChecker`` 既可以是 async function 也可以是 sync function
\:\:\:
"""

import asyncio
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Type, Union, Callable, NoReturn, Optional

from nonebot import params
from nonebot.handler import Handler
from nonebot.adapters import Bot, Event
from nonebot.typing import T_PermissionChecker


class Permission:
    """
    :说明:

      ``Matcher`` 规则类，当事件传递时，在 ``Matcher`` 运行前进行检查。

    :示例:

    .. code-block:: python

        Permission(async_function) | sync_function
        # 等价于
        from nonebot.utils import run_sync
        Permission(async_function, run_sync(sync_function))
    """

    __slots__ = ("checkers",)

    HANDLER_PARAM_TYPES = [params.BotParam, params.EventParam, params.DefaultParam]

    def __init__(self, *checkers: Union[T_PermissionChecker, Handler]) -> None:
        """
        :参数:

          * ``*checkers: Union[T_PermissionChecker, Handler]``: PermissionChecker
        """

        self.checkers = set(
            checker
            if isinstance(checker, Handler)
            else Handler(checker, allow_types=self.HANDLER_PARAM_TYPES)
            for checker in checkers
        )
        """
        :说明:

          存储 ``PermissionChecker``

        :类型:

          * ``Set[Handler]``
        """

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[Dict[Callable[..., Any], Any]] = None,
    ) -> bool:
        """
        :说明:

          检查是否满足某个权限

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``stack: Optional[AsyncExitStack]``: 异步上下文栈
          * ``dependency_cache: Optional[Dict[Callable[..., Any], Any]]``: 依赖缓存

        :返回:

          - ``bool``
        """
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *(
                checker(
                    bot=bot,
                    event=event,
                    _stack=stack,
                    _dependency_cache=dependency_cache,
                )
                for checker in self.checkers
            )
        )
        return any(results)

    def __and__(self, other) -> NoReturn:
        raise RuntimeError("And operation between Permissions is not allowed.")

    def __or__(
        self, other: Optional[Union["Permission", T_PermissionChecker]]
    ) -> "Permission":
        if other is None:
            return self
        elif isinstance(other, Permission):
            return Permission(*self.checkers, *other.checkers)
        else:
            return Permission(*self.checkers, other)


async def _message(event: Event) -> bool:
    return event.get_type() == "message"


async def _notice(event: Event) -> bool:
    return event.get_type() == "notice"


async def _request(event: Event) -> bool:
    return event.get_type() == "request"


async def _metaevent(event: Event) -> bool:
    return event.get_type() == "meta_event"


MESSAGE = Permission(_message)
"""
- **说明**: 匹配任意 ``message`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 message type 的 Matcher。
"""
NOTICE = Permission(_notice)
"""
- **说明**: 匹配任意 ``notice`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 notice type 的 Matcher。
"""
REQUEST = Permission(_request)
"""
- **说明**: 匹配任意 ``request`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 request type 的 Matcher。
"""
METAEVENT = Permission(_metaevent)
"""
- **说明**: 匹配任意 ``meta_event`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 meta_event type 的 Matcher。
"""


def USER(*user: str, perm: Optional[Permission] = None):
    """
    :说明:

      ``event`` 的 ``session_id`` 在白名单内且满足 perm

    :参数:

      * ``*user: str``: 白名单
      * ``perm: Optional[Permission]``: 需要同时满足的权限
    """

    async def _user(bot: Bot, event: Event) -> bool:
        return bool(
            event.get_session_id() in user and (perm is None or await perm(bot, event))
        )

    return Permission(_user)


async def _superuser(bot: Bot, event: Event) -> bool:
    return (
        event.get_type() == "message" and event.get_user_id() in bot.config.superusers
    )


SUPERUSER = Permission(_superuser)
"""
- **说明**: 匹配任意超级用户消息类型事件
"""
