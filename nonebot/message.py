"""本模块定义了事件处理主要流程。

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 2
    description: nonebot.message 模块
"""

import contextlib
from contextlib import AsyncExitStack
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Optional

import anyio
from exceptiongroup import BaseExceptionGroup, catch

from nonebot.dependencies import Dependent
from nonebot.exception import (
    IgnoredException,
    NoLogException,
    SkippedException,
    StopPropagation,
)
from nonebot.internal.params import (
    ArgParam,
    BotParam,
    DefaultParam,
    DependParam,
    EventParam,
    ExceptionParam,
    MatcherParam,
    StateParam,
)
from nonebot.log import logger
from nonebot.matcher import Matcher, matchers
from nonebot.rule import TrieRule
from nonebot.typing import (
    T_DependencyCache,
    T_EventPostProcessor,
    T_EventPreProcessor,
    T_RunPostProcessor,
    T_RunPreProcessor,
    T_State,
)
from nonebot.utils import (
    escape_tag,
    flatten_exception_group,
    run_coro_with_catch,
    run_coro_with_shield,
)

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event

_event_preprocessors: set[Dependent[Any]] = set()
_event_postprocessors: set[Dependent[Any]] = set()
_run_preprocessors: set[Dependent[Any]] = set()
_run_postprocessors: set[Dependent[Any]] = set()

EVENT_PCS_PARAMS = (
    DependParam,
    BotParam,
    EventParam,
    StateParam,
    DefaultParam,
)
RUN_PREPCS_PARAMS = (
    DependParam,
    BotParam,
    EventParam,
    StateParam,
    ArgParam,
    MatcherParam,
    DefaultParam,
)
RUN_POSTPCS_PARAMS = (
    DependParam,
    ExceptionParam,
    BotParam,
    EventParam,
    StateParam,
    ArgParam,
    MatcherParam,
    DefaultParam,
)


def event_preprocessor(func: T_EventPreProcessor) -> T_EventPreProcessor:
    """事件预处理。

    装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。
    """
    _event_preprocessors.add(
        Dependent[Any].parse(call=func, allow_types=EVENT_PCS_PARAMS)
    )
    return func


def event_postprocessor(func: T_EventPostProcessor) -> T_EventPostProcessor:
    """事件后处理。

    装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。
    """
    _event_postprocessors.add(
        Dependent[Any].parse(call=func, allow_types=EVENT_PCS_PARAMS)
    )
    return func


def run_preprocessor(func: T_RunPreProcessor) -> T_RunPreProcessor:
    """运行预处理。

    装饰一个函数，使它在每次事件响应器运行前执行。
    """
    _run_preprocessors.add(
        Dependent[Any].parse(call=func, allow_types=RUN_PREPCS_PARAMS)
    )
    return func


def run_postprocessor(func: T_RunPostProcessor) -> T_RunPostProcessor:
    """运行后处理。

    装饰一个函数，使它在每次事件响应器运行后执行。
    """
    _run_postprocessors.add(
        Dependent[Any].parse(call=func, allow_types=RUN_POSTPCS_PARAMS)
    )
    return func


def _handle_ignored_exception(
    msg: str,
) -> Callable[[BaseExceptionGroup[IgnoredException]], None]:
    def _handle(exc_group: BaseExceptionGroup[IgnoredException]) -> None:
        logger.opt(colors=True).info(msg)

    return _handle


def _handle_exception(msg: str) -> Callable[[BaseExceptionGroup[Exception]], None]:
    def _handle(exc_group: BaseExceptionGroup[Exception]) -> None:
        for exc in flatten_exception_group(exc_group):
            logger.opt(colors=True, exception=exc).error(msg)

    return _handle


async def _apply_event_preprocessors(
    bot: "Bot",
    event: "Event",
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
    show_log: bool = True,
) -> bool:
    """运行事件预处理。

    参数:
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        stack: 异步上下文栈
        dependency_cache: 依赖缓存
        show_log: 是否显示日志

    返回:
        是否继续处理事件
    """
    if not _event_preprocessors:
        return True

    if show_log:
        logger.debug("Running PreProcessors...")

    with catch(
        {
            IgnoredException: _handle_ignored_exception(
                f"Event {escape_tag(event.get_event_name())} is <b>ignored</b>"
            ),
            Exception: _handle_exception(
                "<r><bg #f8bbd0>Error when running EventPreProcessors. "
                "Event ignored!</bg #f8bbd0></r>"
            ),
        }
    ):
        async with anyio.create_task_group() as tg:
            for proc in _event_preprocessors:
                tg.start_soon(
                    run_coro_with_catch,
                    proc(
                        bot=bot,
                        event=event,
                        state=state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    ),
                    (SkippedException,),
                )

        return True

    return False


async def _apply_event_postprocessors(
    bot: "Bot",
    event: "Event",
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
    show_log: bool = True,
) -> None:
    """运行事件后处理。

    参数:
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        stack: 异步上下文栈
        dependency_cache: 依赖缓存
        show_log: 是否显示日志
    """
    if not _event_postprocessors:
        return

    if show_log:
        logger.debug("Running PostProcessors...")

    with catch(
        {
            Exception: _handle_exception(
                "<r><bg #f8bbd0>Error when running EventPostProcessors</bg #f8bbd0></r>"
            )
        }
    ):
        async with anyio.create_task_group() as tg:
            for proc in _event_postprocessors:
                tg.start_soon(
                    run_coro_with_catch,
                    proc(
                        bot=bot,
                        event=event,
                        state=state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    ),
                    (SkippedException,),
                )


async def _apply_run_preprocessors(
    bot: "Bot",
    event: "Event",
    state: T_State,
    matcher: Matcher,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
) -> bool:
    """运行事件响应器运行前处理。

    参数:
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        matcher: 事件响应器
        stack: 异步上下文栈
        dependency_cache: 依赖缓存

    返回:
        是否继续处理事件
    """
    if not _run_preprocessors:
        return True

    # ensure matcher function can be correctly called
    with (
        matcher.ensure_context(bot, event),
        catch(
            {
                IgnoredException: _handle_ignored_exception(
                    f"{matcher} running is <b>cancelled</b>"
                ),
                Exception: _handle_exception(
                    "<r><bg #f8bbd0>Error when running RunPreProcessors. "
                    "Running cancelled!</bg #f8bbd0></r>"
                ),
            }
        ),
    ):
        async with anyio.create_task_group() as tg:
            for proc in _run_preprocessors:
                tg.start_soon(
                    run_coro_with_catch,
                    proc(
                        matcher=matcher,
                        bot=bot,
                        event=event,
                        state=state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    ),
                    (SkippedException,),
                )

        return True

    return False


async def _apply_run_postprocessors(
    bot: "Bot",
    event: "Event",
    matcher: Matcher,
    exception: Optional[Exception] = None,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
) -> None:
    """运行事件响应器运行后处理。

    参数:
        bot: Bot 对象
        event: Event 对象
        matcher: 事件响应器
        exception: 事件响应器运行异常
        stack: 异步上下文栈
        dependency_cache: 依赖缓存
    """
    if not _run_postprocessors:
        return

    with (
        matcher.ensure_context(bot, event),
        catch(
            {
                Exception: _handle_exception(
                    "<r><bg #f8bbd0>Error when running RunPostProcessors"
                    "</bg #f8bbd0></r>"
                )
            }
        ),
    ):
        async with anyio.create_task_group() as tg:
            for proc in _run_postprocessors:
                tg.start_soon(
                    run_coro_with_catch,
                    proc(
                        matcher=matcher,
                        exception=exception,
                        bot=bot,
                        event=event,
                        state=matcher.state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    ),
                    (SkippedException,),
                )


async def _check_matcher(
    Matcher: type[Matcher],
    bot: "Bot",
    event: "Event",
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
) -> bool:
    """检查事件响应器是否符合运行条件。

    请注意，过时的事件响应器将被**销毁**。对于未过时的事件响应器，将会一次检查其响应类型、权限和规则。

    参数:
        Matcher: 要检查的事件响应器
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        stack: 异步上下文栈
        dependency_cache: 依赖缓存

    返回:
        bool: 是否符合运行条件
    """
    if Matcher.expire_time and datetime.now() > Matcher.expire_time:
        with contextlib.suppress(Exception):
            Matcher.destroy()
        return False

    try:
        if not await Matcher.check_perm(bot, event, stack, dependency_cache):
            logger.trace(f"Permission conditions not met for {Matcher}")
            return False
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Permission check failed for {Matcher}.</bg #f8bbd0></r>"
        )
        return False

    try:
        if not await Matcher.check_rule(bot, event, state, stack, dependency_cache):
            logger.trace(f"Rule conditions not met for {Matcher}")
            return False
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Rule check failed for {Matcher}.</bg #f8bbd0></r>"
        )
        return False

    return True


async def _run_matcher(
    Matcher: type[Matcher],
    bot: "Bot",
    event: "Event",
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
) -> None:
    """运行事件响应器。

    临时事件响应器将在运行前被**销毁**。

    参数:
        Matcher: 事件响应器
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        stack: 异步上下文栈
        dependency_cache: 依赖缓存

    异常:
        StopPropagation: 阻止事件继续传播
    """
    logger.info(f"Event will be handled by {Matcher}")

    if Matcher.temp:
        with contextlib.suppress(Exception):
            Matcher.destroy()

    matcher = Matcher()

    if not await _apply_run_preprocessors(
        bot=bot,
        event=event,
        state=state,
        matcher=matcher,
        stack=stack,
        dependency_cache=dependency_cache,
    ):
        return

    exception = None

    logger.debug(f"Running {matcher}")

    try:
        await matcher.run(bot, event, state, stack, dependency_cache)
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Running {matcher} failed.</bg #f8bbd0></r>"
        )
        exception = e

    await _apply_run_postprocessors(
        bot=bot,
        event=event,
        matcher=matcher,
        exception=exception,
        stack=stack,
        dependency_cache=dependency_cache,
    )

    if matcher.block:
        raise StopPropagation


async def check_and_run_matcher(
    Matcher: type[Matcher],
    bot: "Bot",
    event: "Event",
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
) -> None:
    """检查并运行事件响应器。

    参数:
        Matcher: 事件响应器
        bot: Bot 对象
        event: Event 对象
        state: 会话状态
        stack: 异步上下文栈
        dependency_cache: 依赖缓存
    """
    if not await _check_matcher(
        Matcher=Matcher,
        bot=bot,
        event=event,
        state=state,
        stack=stack,
        dependency_cache=dependency_cache,
    ):
        return

    await _run_matcher(
        Matcher=Matcher,
        bot=bot,
        event=event,
        state=state,
        stack=stack,
        dependency_cache=dependency_cache,
    )


async def handle_event(bot: "Bot", event: "Event") -> None:
    """处理一个事件。调用该函数以实现分发事件。

    参数:
        bot: Bot 对象
        event: Event 对象

    用法:
        ```python
        driver.task_group.start_soon(handle_event, bot, event)
        ```
    """
    show_log = True
    log_msg = f"<m>{escape_tag(bot.type)} {escape_tag(bot.self_id)}</m> | "
    try:
        log_msg += event.get_log_string()
    except NoLogException:
        show_log = False
    if show_log:
        logger.opt(colors=True).success(log_msg)

    state: dict[Any, Any] = {}
    dependency_cache: T_DependencyCache = {}

    # create event scope context
    async with AsyncExitStack() as stack:
        if not await _apply_event_preprocessors(
            bot=bot,
            event=event,
            state=state,
            stack=stack,
            dependency_cache=dependency_cache,
        ):
            return

        # Trie Match
        try:
            TrieRule.get_value(bot, event, state)
        except Exception as e:
            logger.opt(colors=True, exception=e).warning(
                "Error while parsing command for event"
            )

        break_flag = False

        def _handle_stop_propagation(exc_group: BaseExceptionGroup) -> None:
            nonlocal break_flag

            break_flag = True
            logger.debug("Stop event propagation")

        # iterate through all priority until stop propagation
        for priority in sorted(matchers.keys()):
            if break_flag:
                break

            if show_log:
                logger.debug(f"Checking for matchers in priority {priority}...")

            if not (priority_matchers := matchers[priority]):
                continue

            with catch(
                {
                    StopPropagation: _handle_stop_propagation,
                    Exception: _handle_exception(
                        "<r><bg #f8bbd0>Error when checking Matcher.</bg #f8bbd0></r>"
                    ),
                }
            ):
                async with anyio.create_task_group() as tg:
                    for matcher in priority_matchers:
                        tg.start_soon(
                            run_coro_with_shield,
                            check_and_run_matcher(
                                matcher,
                                bot,
                                event,
                                state.copy(),
                                stack,
                                dependency_cache,
                            ),
                        )

        if show_log:
            logger.debug("Checking for matchers completed")

        await _apply_event_postprocessors(bot, event, state, stack, dependency_cache)
