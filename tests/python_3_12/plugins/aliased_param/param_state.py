from nonebot.typing import T_State

type AliasedState = T_State


async def aliased_state(x: AliasedState) -> T_State:
    return x
