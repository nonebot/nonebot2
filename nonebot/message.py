#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime

from nonebot.log import logger
from nonebot.rule import TrieRule
from nonebot.matcher import matchers
from nonebot.typing import Set, Type, Union, NoReturn
from nonebot.typing import Bot, Event, Matcher, PreProcessor
from nonebot.exception import IgnoredException, ExpiredException
from nonebot.exception import StopPropagation, _ExceptionContainer

_event_preprocessors: Set[PreProcessor] = set()


def event_preprocessor(func: PreProcessor) -> PreProcessor:
    _event_preprocessors.add(func)
    return func


async def _run_matcher(Matcher: Type[Matcher], bot: Bot, event: Event,
                       state: dict) -> Union[None, NoReturn]:
    if datetime.now() > Matcher.expire_time:
        raise _ExceptionContainer([ExpiredException])

    try:
        if not await Matcher.check_perm(
                bot, event) or not await Matcher.check_rule(bot, event, state):
            return
    except Exception as e:
        logger.error(f"Rule check failed for matcher {Matcher}. Ignored.")
        logger.exception(e)
        return

    matcher = Matcher()
    # TODO: BeforeMatcherRun
    try:
        logger.debug(f"Running matcher {matcher}")
        await matcher.run(bot, event, state)
    except Exception as e:
        logger.error(f"Running matcher {matcher} failed.")
        logger.exception(e)

    exceptions = []
    if Matcher.temp:
        exceptions.append(ExpiredException)
    if Matcher.block:
        exceptions.append(StopPropagation)
    if exceptions:
        raise _ExceptionContainer(exceptions)


async def handle_event(bot: Bot, event: Event):
    coros = []
    state = {}
    for preprocessor in _event_preprocessors:
        coros.append(preprocessor(bot, event, state))
    if coros:
        try:
            await asyncio.gather(*coros)
        except IgnoredException:
            logger.info(f"Event {event} is ignored")
            return

    # Trie Match
    if event.type == "message":
        _, _ = TrieRule.get_value(bot, event, state)

    break_flag = False
    for priority in sorted(matchers.keys()):
        if break_flag:
            break

        pending_tasks = [
            _run_matcher(matcher, bot, event, state.copy())
            for matcher in matchers[priority]
        ]

        results = await asyncio.gather(*pending_tasks, return_exceptions=True)

        i = 0
        for index, result in enumerate(results):
            if isinstance(result, _ExceptionContainer):
                e_list = result.exceptions
                if StopPropagation in e_list:
                    break_flag = True
                if ExpiredException in e_list:
                    del matchers[priority][index - i]
                    i += 1
