#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.plugin import on_metaevent
from nonebot.typing import Bot, Event


async def heartbeat(bot: Bot, event: Event, state: dict) -> bool:
    return event.detail_type == "heartbeat"


test_matcher = on_metaevent(heartbeat)


@test_matcher.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: dict):
    print("[i] Heartbeat")
