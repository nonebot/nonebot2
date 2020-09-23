#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import to_me
from nonebot.typing import Event
from nonebot.plugin import on_startswith
from nonebot.adapters.cqhttp import Bot
from nonebot.permission import GROUP_ADMIN

test_command = on_startswith("hello", to_me(), permission=GROUP_ADMIN)


@test_command.handle()
async def test_handler(bot: Bot, event: Event, state: dict):
    await test_command.finish("hello")
