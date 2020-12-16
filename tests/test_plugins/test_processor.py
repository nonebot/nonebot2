from nonebot.typing import State
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import event_preprocessor, run_preprocessor


@event_preprocessor
async def handle(bot: Bot, event: Event, state: State):
    state["preprocessed"] = True
    print(type(event), event)


@run_preprocessor
async def run(matcher: Matcher, bot: Bot, event: Event, state: State):
    print(matcher)
