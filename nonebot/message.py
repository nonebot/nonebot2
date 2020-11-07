import asyncio
from datetime import datetime

from nonebot.log import logger
from nonebot.rule import TrieRule
from nonebot.utils import escape_tag
from nonebot.matcher import matchers
from nonebot.exception import IgnoredException, ExpiredException
from nonebot.exception import StopPropagation, _ExceptionContainer
from nonebot.typing import Set, Type, Union, NoReturn, Bot, Event, Matcher
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


async def _run_matcher(Matcher: Type[Matcher], bot: Bot, event: Event,
                       state: dict) -> Union[None, NoReturn]:
    if Matcher.expire_time and datetime.now() > Matcher.expire_time:
        raise _ExceptionContainer([ExpiredException])

    try:
        if not await Matcher.check_perm(
                bot, event) or not await Matcher.check_rule(bot, event, state):
            return
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Rule check failed for {Matcher}.</bg #f8bbd0></r>")
        return

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

    exceptions = []

    try:
        logger.debug(f"Running matcher {matcher}")
        await matcher.run(bot, event, state)
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f"<r><bg #f8bbd0>Running matcher {matcher} failed.</bg #f8bbd0></r>"
        )
        exceptions.append(e)

    if Matcher.temp:
        exceptions.append(ExpiredException)
    if Matcher.block:
        exceptions.append(StopPropagation)

    coros = list(
        map(lambda x: x(matcher, exceptions, bot, event, state),
            _run_postprocessors))
    if coros:
        try:
            await asyncio.gather(*coros)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running RunPostProcessors</bg #f8bbd0></r>"
            )

    if exceptions:
        raise _ExceptionContainer(exceptions)


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

        pending_tasks = [
            _run_matcher(matcher, bot, event, state.copy())
            for matcher in matchers[priority]
        ]

        if show_log:
            logger.debug(f"Checking for matchers in priority {priority}...")
        results = await asyncio.gather(*pending_tasks, return_exceptions=True)

        i = 0
        for index, result in enumerate(results):
            if isinstance(result, _ExceptionContainer):
                e_list = result.exceptions
                if StopPropagation in e_list:
                    if not break_flag:
                        break_flag = True
                        logger.debug("Stop event propagation")
                if ExpiredException in e_list:
                    logger.debug(
                        f"Matcher {matchers[priority][index - i]} will be removed."
                    )
                    del matchers[priority][index - i]
                    i += 1

    coros = list(map(lambda x: x(bot, event, state), _event_postprocessors))
    if coros:
        try:
            logger.debug("Running PostProcessors...")
            await asyncio.gather(*coros)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Error when running EventPostProcessors</bg #f8bbd0></r>"
            )
