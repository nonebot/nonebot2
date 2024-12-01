from contextlib import AsyncExitStack
from typing import ClassVar, NoReturn, Optional, Union
from typing_extensions import Self

import anyio

from nonebot.dependencies import Dependent
from nonebot.exception import SkippedException
from nonebot.typing import T_DependencyCache, T_PermissionChecker
from nonebot.utils import run_coro_with_catch

from .adapter import Bot, Event
from .params import BotParam, DefaultParam, DependParam, EventParam, Param


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

    HANDLER_PARAM_TYPES: ClassVar[list[type[Param]]] = [
        DependParam,
        BotParam,
        EventParam,
        DefaultParam,
    ]

    def __init__(self, *checkers: Union[T_PermissionChecker, Dependent[bool]]) -> None:
        self.checkers: set[Dependent[bool]] = {
            (
                checker
                if isinstance(checker, Dependent)
                else Dependent[bool].parse(
                    call=checker, allow_types=self.HANDLER_PARAM_TYPES
                )
            )
            for checker in checkers
        }
        """存储 `PermissionChecker`"""

    def __repr__(self) -> str:
        return f"Permission({', '.join(repr(checker) for checker in self.checkers)})"

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """检查是否满足某个权限。

        参数:
            bot: Bot 对象
            event: Event 对象
            stack: 异步上下文栈
            dependency_cache: 依赖缓存
        """
        if not self.checkers:
            return True

        result = False

        async def _run_checker(checker: Dependent[bool]) -> None:
            nonlocal result
            # calculate the result first to avoid data racing
            is_passed = await run_coro_with_catch(
                checker(
                    bot=bot, event=event, stack=stack, dependency_cache=dependency_cache
                ),
                (SkippedException,),
                False,
            )
            result |= is_passed

        async with anyio.create_task_group() as tg:
            for checker in self.checkers:
                tg.start_soon(_run_checker, checker)

        return result

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
    """检查当前事件是否属于指定会话。

    参数:
        users: 会话 ID 元组
        perm: 需同时满足的权限
    """

    __slots__ = ("perm", "users")

    def __init__(
        self, users: tuple[str, ...], perm: Optional[Permission] = None
    ) -> None:
        self.users = users
        self.perm = perm

    def __repr__(self) -> str:
        return (
            f"User(users={self.users}"
            + (f", permission={self.perm})" if self.perm else "")
            + ")"
        )

    async def __call__(self, bot: Bot, event: Event) -> bool:
        try:
            session = event.get_session_id()
        except Exception:
            return False
        return bool(
            session in self.users and (self.perm is None or await self.perm(bot, event))
        )

    @classmethod
    def _clean_permission(cls, perm: Permission) -> Optional[Permission]:
        if len(perm.checkers) == 1 and isinstance(
            user_perm := next(iter(perm.checkers)).call, cls
        ):
            return user_perm.perm
        return perm

    @classmethod
    def from_event(cls, event: Event, perm: Optional[Permission] = None) -> Self:
        """从事件中获取会话 ID。

        如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有的会话 ID 限制。

        参数:
            event: Event 对象
            perm: 需同时满足的权限
        """
        return cls((event.get_session_id(),), perm=perm and cls._clean_permission(perm))

    @classmethod
    def from_permission(cls, *users: str, perm: Optional[Permission] = None) -> Self:
        """指定会话与权限。

        如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有的会话 ID 限制。

        参数:
            users: 会话白名单
            perm: 需同时满足的权限
        """
        return cls(users, perm=perm and cls._clean_permission(perm))


def USER(*users: str, perm: Optional[Permission] = None):
    """匹配当前事件属于指定会话。

    如果 `perm` 中仅有 `User` 类型的权限检查函数，则会去除原有检查函数的会话 ID 限制。

    参数:
        user: 会话白名单
        perm: 需要同时满足的权限
    """

    return Permission(User.from_permission(*users, perm=perm))
