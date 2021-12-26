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
from typing import Any, Set, Tuple, Union, NoReturn, Optional, Coroutine

from nonebot.adapters import Bot, Event
from nonebot.dependencies import Dependent
from nonebot.exception import SkippedException
from nonebot.typing import T_Handler, T_DependencyCache, T_PermissionChecker
from nonebot.params import (
    BotParam,
    EventType,
    EventParam,
    DependParam,
    DefaultParam,
)


async def _run_coro_with_catch(coro: Coroutine[Any, Any, Any]):
    try:
        return await coro
    except SkippedException:
        return False


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

    HANDLER_PARAM_TYPES = [
        DependParam,
        BotParam,
        EventParam,
        DefaultParam,
    ]

    def __init__(self, *checkers: Union[T_PermissionChecker, Dependent[bool]]) -> None:
        """
        :参数:

          * ``*checkers: Union[T_PermissionChecker, Dependent[bool]``: PermissionChecker
        """

        self.checkers: Set[Dependent[bool]] = set(
            checker
            if isinstance(checker, Dependent)
            else Dependent[bool].parse(
                call=checker, allow_types=self.HANDLER_PARAM_TYPES
            )
            for checker in checkers
        )
        """
        :说明:

          存储 ``PermissionChecker``

        :类型:

          * ``Set[Dependent[bool]]``
        """

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """
        :说明:

          检查是否满足某个权限

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``stack: Optional[AsyncExitStack]``: 异步上下文栈
          * ``dependency_cache: Optional[CacheDict[T_Handler, Any]]``: 依赖缓存

        :返回:

          - ``bool``
        """
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *(
                _run_coro_with_catch(
                    checker(
                        bot=bot,
                        event=event,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    )
                )
                for checker in self.checkers
            ),
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


class Message:
    async def __call__(self, type: str = EventType()) -> bool:
        return type == "message"


class Notice:
    async def __call__(self, type: str = EventType()) -> bool:
        return type == "notice"


class Request:
    async def __call__(self, type: str = EventType()) -> bool:
        return type == "request"


class MetaEvent:
    async def __call__(self, type: str = EventType()) -> bool:
        return type == "meta_event"


MESSAGE = Permission(Message())
"""
- **说明**: 匹配任意 ``message`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 message type 的 Matcher。
"""
NOTICE = Permission(Notice())
"""
- **说明**: 匹配任意 ``notice`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 notice type 的 Matcher。
"""
REQUEST = Permission(Request())
"""
- **说明**: 匹配任意 ``request`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 request type 的 Matcher。
"""
METAEVENT = Permission(MetaEvent())
"""
- **说明**: 匹配任意 ``meta_event`` 类型事件，仅在需要同时捕获不同类型事件时使用。优先使用 meta_event type 的 Matcher。
"""


class User:
    def __init__(
        self, users: Tuple[str, ...], perm: Optional[Permission] = None
    ) -> None:
        self.users = users
        self.perm = perm

    async def __call__(self, bot: Bot, event: Event) -> bool:
        return bool(
            event.get_session_id() in self.users
            and (self.perm is None or await self.perm(bot, event))
        )


def USER(*users: str, perm: Optional[Permission] = None):
    """
    :说明:

      ``event`` 的 ``session_id`` 在白名单内且满足 perm

    :参数:

      * ``*user: str``: 白名单
      * ``perm: Optional[Permission]``: 需要同时满足的权限
    """

    return Permission(User(users, perm))


class SuperUser:
    async def __call__(self, bot: Bot, event: Event) -> bool:
        return event.get_type() == "message" and (
            f"{bot.adapter.get_name().split(maxsplit=1)[0].lower()}:{event.get_user_id()}"
            in bot.config.superusers
            or event.get_user_id() in bot.config.superusers  # 兼容旧配置
        )


SUPERUSER = Permission(SuperUser())
"""
- **说明**: 匹配任意超级用户消息类型事件
"""
