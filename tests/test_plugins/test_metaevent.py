from nonebot.typing import State
from nonebot.adapters import Bot, Event
from nonebot.plugin import on_metaevent


async def heartbeat(bot: Bot, event: Event, state: State) -> bool:
    return event.detail_type == "heartbeat"


test_matcher = on_metaevent(heartbeat)


@test_matcher.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: dict):
    print("[i] Heartbeat")
