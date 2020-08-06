#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import Rule
from nonebot.event import Event
from nonebot.plugin import on_metaevent


def heartbeat(bot, event: Event) -> bool:
    return event.detail_type == "heartbeat"


test_matcher = on_metaevent(Rule(heartbeat))


@test_matcher.handle()
async def handle_heartbeat(bot, event: Event, state: dict):
    print("[i] Heartbeat")
