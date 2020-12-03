from nonebot.typing import Bot, Event

from . import match


async def heartbeat(bot: Bot, event: Event, state: dict) -> bool:
    return event.detail_type == "heartbeat"


test = match.on_metaevent(rule=heartbeat)


@test.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: dict):
    print("[i] Heartbeat")
