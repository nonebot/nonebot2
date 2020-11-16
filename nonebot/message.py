"""
事件处理
========
"""

import asyncio
from datetime import datetime

from nonebot.log import logger
from nonebot.rule import TrieRule
from nonebot.utils import escape_tag
from nonebot.matcher import matchers, Matcher
from nonebot.typing import Set, Type, Union, Iterable, NoReturn, Bot, Event
from nonebot.exception import IgnoredException, ExpiredException, StopPropagation
from nonebot.typing import EventPreProcessor, RunPreProcessor, EventPostProcessor, RunPostProcessor

_event_preprocessors: Set[EventPreProcessor] = set()
_event_postprocessors: Set[EventPostProcessor] = set()
_run_preprocessors: Set[RunPreProcessor] = set()
_run_postprocessors: Set[RunPostProcessor] = set()


def event_preprocessor(func: EventPreProcessor) -> EventPreProcessor:
    _event_preprocessors.add(func)
    return func


def event_postprocessor(func: EventPostProcessor) -> EventPostProcessor:
    _event_postprocessors.add(func)
    return func


def run_preprocessor(func: RunPreProcessor) -> RunPreProcessor:
    _run_preprocessors.add(func)
    return func


def run_postprocessor(func: RunPostProcessor) -> RunPostProcessor:
    _run_postprocessors.add(func)
    return func


async def _check_matcher(priority: int, bot: Bot, event: Event,
                         state: dict) -> Iterable[Type[Matcher]]:
    current_matchers = matchers[priority].copy()

    async def _check(Matcher: Type[Matcher], bot: Bot, event: Event,
                     state: dict) -> Optional[Type[Matcher]]:
        try:
            if await Matcher.check_perm(
                    bot, event) and await Matcher.check_rule(bot, event, state):
                return Matcher
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Rule check failed for {Matcher}.</bg #f8bbd0></r>"
            )
        return None

    async def _check_expire(Matcher: Type[Matcher]) -> Optional[Type[Matcher]]:
        if Matcher.temp or (Matcher.expire_time and
                            datetime.now() > Matcher.expire_time):
            return Matcher
        return None

    checking_tasks = [
        _check(Matcher, bot, event, state) for Matcher in current_matchers
    ]
    checking_expire_tasks = [
        _check_expire(Matcher) for Matcher in current_matchers
    ]
    results = await asyncio.gather(*checking_tasks, return_exceptions=True)
    expired = await asyncio.gather(*checking_expire_tasks)
    for expired_matcher in filter(lambda x: issubclass(Matcher), expired):
        try:
            matchers[priority].remove(expired_matcher)
        except Exception:
            pass
    return filter(lambda x: issubclass(Matcher), results)


async def _run_matcher(Matcher: Type[Matcher], bot: Bot, event: Event,
                       state: dict) -> Union[None, NoReturn]:
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


async def handle_event(bot: Bot, event: Event):
    show_log = True
    log_msg = f"<m>{bot.type.upper()} </m>| {event.self_id} [{event.name}]: "
    if event.type == "message":
        log_msg += f"Message {event.id} from "
        log_msg += str(event.user_id)
        if event.detail_type == "group":
            log_msg += f"@[群:{event.group_id}]:"

        log_msg += ' "' + "".join(
            map(
                lambda x: escape_tag(str(x))
                if x.type == "text" else f"<le>{escape_tag(str(x))}</le>",
                event.message)) + '"'  # type: ignore
    elif event.type == "notice":
        log_msg += f"Notice {event.raw_event}"
    elif event.type == "request":
        log_msg += f"Request {event.raw_event}"
    elif event.type == "meta_event":
        # log_msg += f"MetaEvent {event.detail_type}"
        show_log = False
    if show_log:
        logger.opt(colors=True).info(log_msg)

    state = {}
    coros = list(map(lambda x: x(bot, event, state), _event_preprocessors))
    if coros:
        try:
            logger.debug("Running PreProcessors...")
            await asyncio.gather(*coros)
        except IgnoredException:
            logger.opt(
                colors=True).info(f"Event {event.name} is <b>ignored</b>")
            return
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running EventPreProcessors. "
                "Event ignored!</bg #f8bbd0></r>")
            return

    # Trie Match
    _, _ = TrieRule.get_value(bot, event, state)

    break_flag = False
    for priority in sorted(matchers.keys()):
        if break_flag:
            break

        if show_log:
            logger.debug(f"Checking for matchers in priority {priority}...")

        run_matchers = _check_matcher(priority, bot, event, state)

        pending_tasks = [
            _run_matcher(matcher, bot, event, state.copy())
            for matcher in run_matchers
        ]

        results = await asyncio.gather(*pending_tasks, return_exceptions=True)

        for result in results:
            if result is StopPropagation:
                if not break_flag:
                    break_flag = True
                    logger.debug("Stop event propagation")

    coros = list(map(lambda x: x(bot, event, state), _event_postprocessors))
    if coros:
        try:
            logger.debug("Running PostProcessors...")
            await asyncio.gather(*coros)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running EventPostProcessors</bg #f8bbd0></r>"
            )
