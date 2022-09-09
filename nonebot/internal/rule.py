import asyncio
from contextlib import AsyncExitStack
from typing import Set, Union, NoReturn, Optional

from nonebot.dependencies import Dependent
from nonebot.exception import SkippedException
from nonebot.typing import T_State, T_RuleChecker, T_DependencyCache

from .adapter import Bot, Event
from .params import BotParam, EventParam, StateParam, DependParam, DefaultParam


class Rule:
    """{ref}`nonebot.matcher.Matcher` 规则类。

    当事件传递时，在 {ref}`nonebot.matcher.Matcher` 运行前进行检查。

    参数:
        *checkers: RuleChecker

    用法:
        ```python
        Rule(async_function) & sync_function
        # 等价于
        Rule(async_function, sync_function)
        ```
    """

    __slots__ = ("checkers",)

    HANDLER_PARAM_TYPES = [
        DependParam,
        BotParam,
        EventParam,
        StateParam,
        DefaultParam,
    ]

    def __init__(self, *checkers: Union[T_RuleChecker, Dependent[bool]]) -> None:
        self.checkers: Set[Dependent[bool]] = {
            checker
            if isinstance(checker, Dependent)
            else Dependent[bool].parse(
                call=checker, allow_types=self.HANDLER_PARAM_TYPES
            )
            for checker in checkers
        }
        """存储 `RuleChecker`"""

    def __repr__(self) -> str:
        return f"Rule({', '.join(repr(checker) for checker in self.checkers)})"

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """检查是否符合所有规则

        参数:
            bot: Bot 对象
            event: Event 对象
            state: 当前 State
            stack: 异步上下文栈
            dependency_cache: 依赖缓存
        """
        if not self.checkers:
            return True
        try:
            results = await asyncio.gather(
                *(
                    checker(
                        bot=bot,
                        event=event,
                        state=state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    )
                    for checker in self.checkers
                )
            )
        except SkippedException:
            return False
        return all(results)

    def __and__(self, other: Optional[Union["Rule", T_RuleChecker]]) -> "Rule":
        if other is None:
            return self
        elif isinstance(other, Rule):
            return Rule(*self.checkers, *other.checkers)
        else:
            return Rule(*self.checkers, other)

    def __rand__(self, other: Optional[Union["Rule", T_RuleChecker]]) -> "Rule":
        if other is None:
            return self
        elif isinstance(other, Rule):
            return Rule(*other.checkers, *self.checkers)
        else:
            return Rule(other, *self.checkers)

    def __or__(self, other: object) -> NoReturn:
        raise RuntimeError("Or operation between rules is not allowed.")
