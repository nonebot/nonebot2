from nonebot.adapters import Event

type AliasedEvent = Event


async def aliased_event(e: AliasedEvent) -> Event:
    return e
