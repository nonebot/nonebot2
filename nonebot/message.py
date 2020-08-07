#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime

from nonebot.log import logger
from nonebot.event import Event
from nonebot.matcher import matchers
from nonebot.typing import Set, Callable
from nonebot.exception import IgnoredException

_event_preprocessors: Set[Callable] = set()


def event_preprocessor(func: Callable) -> Callable:
    _event_preprocessors.add(func)
    return func


async def handle_event(bot, event: Event):
    # TODO: PreProcess
    coros = []
    for preprocessor in _event_preprocessors:
        coros.append(preprocessor(bot, event))
    if coros:
        try:
            await asyncio.gather(*coros)
        except IgnoredException:
            logger.info(f"Event {event} is ignored")
            return

    for priority in sorted(matchers.keys()):
        index = 0
        while index <= len(matchers[priority]):
            Matcher = matchers[priority][index]

            # Delete expired Matcher
            if datetime.now() > Matcher.expire_time:
                del matchers[priority][index]
                continue

            # Check rule
            try:
                if not Matcher.check_rule(bot, event):
                    index += 1
                    continue
            except Exception as e:
                logger.error(
                    f"Rule check failed for matcher {Matcher}. Ignored.")
                logger.exception(e)
                continue

            matcher = Matcher()
            # TODO: BeforeMatcherRun
            if Matcher.temp:
                del matchers[priority][index]

            try:
                await matcher.run(bot, event)
            except Exception as e:
                logger.error(f"Running matcher {matcher} failed.")
                logger.exception(e)
            return
