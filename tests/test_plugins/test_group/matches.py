from nonebot.typing import State
from nonebot.adapters import Bot, Event

from . import match


async def heartbeat(bot: Bot, event: Event, state: State) -> bool:
    return event.detail_type == "heartbeat"


test = match.on_metaevent(rule=heartbeat)


@test.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: State):
    print("[i] Heartbeat")
