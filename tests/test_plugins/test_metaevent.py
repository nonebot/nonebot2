from nonebot.typing import T_State
from nonebot.plugin import on_metaevent
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import HeartbeatMetaEvent


async def heartbeat(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, HeartbeatMetaEvent)


test_matcher = on_metaevent(heartbeat)


@test_matcher.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: T_State):
    print("[i] Heartbeat")
