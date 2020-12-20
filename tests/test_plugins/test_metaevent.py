from nonebot.typing import T_State
from nonebot.plugin import on_metaevent
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import HeartbeatMetaEvent


async def heartbeat(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, HeartbeatMetaEvent)


async def factory(bot: Bot, event: Event) -> T_State:
    return {"factory": True}


test_matcher = on_metaevent(heartbeat, state_factory=factory)


@test_matcher.receive()
async def handle_heartbeat(bot: Bot, event: Event, state: T_State):
    print(state)
    print("[i] Heartbeat")
