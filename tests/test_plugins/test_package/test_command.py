#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import Rule
from nonebot.typing import Event
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot

test_command = on_command(("帮助",))


@test_command.handle()
async def test_handler(bot: Bot, event: Event, state: dict):
    print(state["_prefix"])
