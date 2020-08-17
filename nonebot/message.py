#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime

from nonebot.log import logger
from nonebot.rule import TrieRule
from nonebot.matcher import matchers
from nonebot.exception import IgnoredException
from nonebot.typing import Bot, Set, Event, PreProcessor

_event_preprocessors: Set[PreProcessor] = set()


def event_preprocessor(func: PreProcessor) -> PreProcessor:
    _event_preprocessors.add(func)
    return func


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
    _, _ = TrieRule.get_value(bot, event, state)

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
                if not await Matcher.check_perm(
                        bot, event) or not await Matcher.check_rule(
                            bot, event, state):
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
                await matcher.run(bot, event, state)
            except Exception as e:
                logger.error(f"Running matcher {matcher} failed.")
                logger.exception(e)
            return
