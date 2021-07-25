from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import HeartbeatMetaEvent

from . import match


async def heartbeat(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, HeartbeatMetaEvent)


test = match.on_metaevent(rule=heartbeat)


@test.receive()
async def handle_heartbeat(bot: Bot):
    print("[i] Heartbeat")
