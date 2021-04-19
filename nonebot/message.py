"""
事件处理
========

NoneBot 内部处理并按优先级分发事件给所有事件响应器，提供了多个插槽以进行事件的预处理等。
"""

import asyncio
from datetime import datetime
from typing import Set, Type, Optional, TYPE_CHECKING

from nonebot.log import logger
from nonebot.rule import TrieRule
from nonebot.matcher import matchers, Matcher
from nonebot.exception import IgnoredException, StopPropagation, NoLogException
from nonebot.typing import T_State, T_EventPreProcessor, T_RunPreProcessor, T_EventPostProcessor, T_RunPostProcessor

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event

_event_preprocessors: Set[T_EventPreProcessor] = set()
_event_postprocessors: Set[T_EventPostProcessor] = set()
_run_preprocessors: Set[T_RunPreProcessor] = set()
_run_postprocessors: Set[T_RunPostProcessor] = set()


def event_preprocessor(func: T_EventPreProcessor) -> T_EventPreProcessor:
    """
    :说明:

      事件预处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之前执行。

    :参数:

      事件预处理函数接收三个参数。

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
      * ``state: T_State``: 当前 State
    """
    _event_preprocessors.add(func)
    return func


def event_postprocessor(func: T_EventPostProcessor) -> T_EventPostProcessor:
    """
    :说明:

      事件后处理。装饰一个函数，使它在每次接收到事件并分发给各响应器之后执行。

    :参数:

      事件后处理函数接收三个参数。

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
      * ``state: T_State``: 当前事件运行前 State
    """
    _event_postprocessors.add(func)
    return func


def run_preprocessor(func: T_RunPreProcessor) -> T_RunPreProcessor:
    """
    :说明:

      运行预处理。装饰一个函数，使它在每次事件响应器运行前执行。

    :参数:

      运行预处理函数接收四个参数。

      * ``matcher: Matcher``: 当前要运行的事件响应器
      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
      * ``state: T_State``: 当前 State
    """
    _run_preprocessors.add(func)
    return func


def run_postprocessor(func: T_RunPostProcessor) -> T_RunPostProcessor:
    """
    :说明:

      运行后处理。装饰一个函数，使它在每次事件响应器运行后执行。

    :参数:

      运行后处理函数接收五个参数。

      * ``matcher: Matcher``: 运行完毕的事件响应器
      * ``exception: Optional[Exception]``: 事件响应器运行错误（如果存在）
      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
      * ``state: T_State``: 当前 State
    """
    _run_postprocessors.add(func)
    return func


async def _check_matcher(priority: int, Matcher: Type[Matcher], bot: "Bot",
                         event: "Event", state: T_State) -> None:
    if Matcher.expire_time and datetime.now() > Matcher.expire_time:
        try:
            matchers[priority].remove(Matcher)
        except Exception:
            pass
        return

    try:
        if not await Matcher.check_perm(
                bot, event) or not await Matcher.check_rule(bot, event, state):
            return
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Rule check failed for {Matcher}.</bg #f8bbd0></r>")
        return

    if Matcher.temp:
        try:
            matchers[priority].remove(Matcher)
        except Exception:
            pass

    await _run_matcher(Matcher, bot, event, state)


async def _run_matcher(Matcher: Type[Matcher], bot: "Bot", event: "Event",
                       state: T_State) -> None:
    logger.info(f"Event will be handled by {Matcher}")

    matcher = Matcher()

    coros = list(
        map(lambda x: x(matcher, bot, event, state), _run_preprocessors))
    if coros:
        try:
            await asyncio.gather(*coros)
        except IgnoredException:
            logger.opt(colors=True).info(
                f"Matcher {matcher} running is <b>cancelled</b>")
            return
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running RunPreProcessors. "
                "Running cancelled!</bg #f8bbd0></r>")
            return

    exception = None

    try:
        logger.debug(f"Running matcher {matcher}")
        await matcher.run(bot, event, state)
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Running matcher {matcher} failed.</bg #f8bbd0></r>"
        )
        exception = e

    coros = list(
        map(lambda x: x(matcher, exception, bot, event, state),
            _run_postprocessors))
    if coros:
        try:
            await asyncio.gather(*coros)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running RunPostProcessors</bg #f8bbd0></r>"
            )

    if matcher.block:
        raise StopPropagation
    return


async def handle_event(bot: "Bot", event: "Event") -> Optional[Exception]:
    """
    :说明:

       处理一个事件。调用该函数以实现分发事件。

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象

    :示例:

    .. code-block:: python

        import asyncio
        asyncio.create_task(handle_event(bot, event))
    """
    show_log = True
    log_msg = f"<m>{bot.type.upper()} {bot.self_id}</m> | "
    try:
        log_msg += event.get_log_string()
    except NoLogException:
        show_log = False
    if show_log:
        logger.opt(colors=True).success(log_msg)

    state = {}
    coros = list(map(lambda x: x(bot, event, state), _event_preprocessors))
    if coros:
        try:
            if show_log:
                logger.debug("Running PreProcessors...")
            await asyncio.gather(*coros)
        except IgnoredException as e:
            logger.opt(colors=True).info(
                f"Event {event.get_event_name()} is <b>ignored</b>")
            return e
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running EventPreProcessors. "
                "Event ignored!</bg #f8bbd0></r>")
            return e

    # Trie Match
    _, _ = TrieRule.get_value(bot, event, state)

    break_flag = False
    for priority in sorted(matchers.keys()):
        if break_flag:
            break

        if show_log:
            logger.debug(f"Checking for matchers in priority {priority}...")

        pending_tasks = [
            _check_matcher(priority, matcher, bot, event, state.copy())
            for matcher in matchers[priority]
        ]

        results = await asyncio.gather(*pending_tasks, return_exceptions=True)

        for result in results:
            if not isinstance(result, Exception):
                continue
            if isinstance(result, StopPropagation):
                break_flag = True
                logger.debug("Stop event propagation")
            else:
                logger.opt(colors=True, exception=result).error(
                    "<r><bg #f8bbd0>Error when checking Matcher.</bg #f8bbd0></r>"
                )
            return result

    coros = list(map(lambda x: x(bot, event, state), _event_postprocessors))
    if coros:
        try:
            if show_log:
                logger.debug("Running PostProcessors...")
            await asyncio.gather(*coros)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running EventPostProcessors</bg #f8bbd0></r>"
            )
            return e
