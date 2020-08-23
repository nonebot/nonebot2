#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.rule import to_me
from nonebot.typing import Event
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot

test_command = on_command("帮助", to_me())


@test_command.handle()
async def test_handler(bot: Bot, event: Event, state: dict):
    print("[!] Command:", state["_prefix"])
    args = str(event.message)[len(state["_prefix"]):].strip()
    if args:
        state["help"] = args
    else:
        await bot.send_private_msg(message="命令:\n1. test1\n2. test2",
                                   user_id=event.user_id)


@test_command.got("help", prompt="你要帮助的命令是？")
async def test_handler(bot: Bot, event: Event, state: dict):
    print("[!] Command 帮助:", state["help"])
    if state["help"] not in ["test1", "test2"]:
        await bot.send_private_msg(message=f"{state['help']} 不支持，请重新输入！")
        test_command.reject()
    await bot.send_private_msg(message=f"{state['help']} 帮助:\n...")
