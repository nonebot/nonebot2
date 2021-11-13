from nonebot.typing import T_State
from nonebot.processor import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor, event_preprocessor


@event_preprocessor
async def handle(bot: Bot, event: Event, state: T_State):
    state["preprocessed"] = True
    print(type(event), event)


@run_preprocessor
async def run(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    print(matcher)
