import asyncio

from nonebot import on_message
from nonebot.permission import USER
from nonebot.typing import Bot, Event

a = on_message(priority=0, permission=USER(123123123), temp=True)


@a.handle()
async def test_a(bot: Bot, event: Event, state: dict):
    print("======== A Received ========")
    print("======== A Running Completed ========")


b = on_message(priority=0, permission=USER(123456789), temp=True)


@b.handle()
async def test_b(bot: Bot, event: Event, state: dict):
    print("======== B Received ========")
    await asyncio.sleep(10)
    print("======== B Running Completed ========")


c = on_message(priority=0, permission=USER(1111111111))


@c.handle()
async def test_c(bot: Bot, event: Event, state: dict):
    print("======== C Received ========")
