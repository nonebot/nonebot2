#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import Rule
from nonebot.typing import Event
from nonebot.plugin import on_message
from nonebot.adapters.cqhttp import Bot, Message

print(repr(Message("asdfasdf[CQ:at,qq=123][CQ:at,qq=all]")))

test_matcher = on_message(Rule(), state={"default": 1})


@test_matcher.handle()
async def test_handler(bot: Bot, event: Event, state: dict):
    print("Test Matcher Received:", event)
    print("Current State:", state)
    state["event"] = event


@test_matcher.receive()
async def test_receive(bot: Bot, event: Event, state: dict):
    print("Test Matcher Received next time:", event)
    print("Current State:", state)
