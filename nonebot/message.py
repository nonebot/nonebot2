#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.log import logger
from nonebot.event import Event
from nonebot.matcher import matchers


async def handle_event(bot, event: Event):
    # TODO: PreProcess

    for priority in sorted(matchers.keys()):
        for index in range(len(matchers[priority])):
            Matcher = matchers[priority][index]
            try:
                if not Matcher.check_rule(event):
                    continue
            except Exception as e:
                logger.error(
                    f"Rule check failed for matcher {Matcher}. Ignored.")
                logger.exception(e)
                continue

            matcher = Matcher()
            if Matcher.temp:
                del matchers[priority][index]

            try:
                await matcher.run(bot, event)
            except Exception as e:
                logger.error(f"Running matcher {matcher} failed.")
                logger.exception(e)
            return
