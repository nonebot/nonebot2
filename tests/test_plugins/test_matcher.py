#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import Rule
from nonebot.event import Event
from nonebot.plugin import on_message

test_matcher = on_message(Rule(), state={"default": 1})


@test_matcher.handle()
async def test_handler(bot, event: Event, state: dict):
    print(state)
