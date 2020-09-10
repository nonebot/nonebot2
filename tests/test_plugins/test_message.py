#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import to_me
from nonebot.typing import Event
from nonebot.plugin import on_message
from nonebot.adapters.cqhttp import Bot

test_message = on_message(to_me(), state={"default": 1})


@test_message.handle()
async def test_handler(bot: Bot, event: Event, state: dict):
    print("[*] Test Matcher Received:", event)
    state["event"] = event
    await bot.send(message="Received", event=event)


@test_message.receive()
async def test_receive(bot: Bot, event: Event, state: dict):
    print("[*] Test Matcher Received next time:", event)
    print("[*] Current State:", state)
