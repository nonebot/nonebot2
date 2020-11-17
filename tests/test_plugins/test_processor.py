from nonebot.typing import Bot, Event, Matcher
from nonebot.message import event_preprocessor, run_preprocessor


@event_preprocessor
async def handle(bot: Bot, event: Event, state: dict):
    state["preprocessed"] = True
    print(event)


@run_preprocessor
async def run(matcher: Matcher, bot: Bot, event: Event, state: dict):
    print(matcher)
