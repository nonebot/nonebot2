import asyncio
from contextlib import AsyncExitStack
from typing import Any, Set, Tuple, Union, NoReturn, Optional, Coroutine

from nonebot.dependencies import Dependent
from nonebot.utils import run_coro_with_catch
from nonebot.exception import SkippedException
from nonebot.typing import T_DependencyCache, T_PermissionChecker

from .adapter import Bot, Event
from .params import BotParam, EventParam, DependParam, DefaultParam


class Permission:
    """{ref}`nonebot.matcher.Matcher` 权限类。

    当事件传递时，在 {ref}`nonebot.matcher.Matcher` 运行前进行检查。

    参数:
        checkers: PermissionChecker

    用法:
        ```python
        Permission(async_function) | sync_function
        # 等价于
        Permission(async_function, sync_function)
        ```
    """

    __slots__ = ("checkers",)

    HANDLER_PARAM_TYPES = [
        DependParam,
        BotParam,
        EventParam,
        DefaultParam,
    ]

    def __init__(self, *checkers: Union[T_PermissionChecker, Dependent[bool]]) -> None:
        self.checkers: Set[Dependent[bool]] = set(
            checker
            if isinstance(checker, Dependent)
            else Dependent[bool].parse(
                call=checker, allow_types=self.HANDLER_PARAM_TYPES
            )
            for checker in checkers
        )
        """存储 `PermissionChecker`"""

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """检查是否满足某个权限

        参数:
            bot: Bot 对象
            event: Event 对象
            stack: 异步上下文栈
            dependency_cache: 依赖缓存
        """
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *(
                run_coro_with_catch(
                    checker(
                        bot=bot,
                        event=event,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    ),
                    (SkippedException,),
                    False,
                )
                for checker in self.checkers
            ),
        )
        return any(results)

    def __and__(self, other: object) -> NoReturn:
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

    def __ror__(
        self, other: Optional[Union["Permission", T_PermissionChecker]]
    ) -> "Permission":
        if other is None:
            return self
        elif isinstance(other, Permission):
            return Permission(*other.checkers, *self.checkers)
        else:
            return Permission(other, *self.checkers)


class User:
    """检查当前事件是否属于指定会话

    参数:
        users: 会话 ID 元组
        perm: 需同时满足的权限
    """

    __slots__ = ("users", "perm")

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
    """匹配当前事件属于指定会话

    参数:
        user: 会话白名单
        perm: 需要同时满足的权限
    """

    return Permission(User(users, perm))
