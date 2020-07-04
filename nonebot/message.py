#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .log import logger
from .event import Event
from .matcher import matchers


async def handle_message(bot, event: Event):
    # TODO: PreProcess

    for priority in sorted(matchers.keys()):
        for index in range(len(matchers[priority])):
            Matcher = matchers[priority][index]
            if not Matcher.check_rule(event):
                continue

            matcher = Matcher()
            if Matcher.temp:
                del matchers[priority][index]

            try:
                await matcher.run(bot, event)
            except Exception as e:
                logger.exception(e)
            return
