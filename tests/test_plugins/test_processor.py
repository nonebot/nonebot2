from nonebot.adapters import Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, event_preprocessor


@event_preprocessor
async def handle(event: Event, state: T_State):
    state["preprocessed"] = True
    print(type(event), event)


@run_preprocessor
async def run(matcher: Matcher):
    print(matcher)
