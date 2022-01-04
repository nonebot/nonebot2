from nonebot.adapters import Event, Message
from nonebot.params import EventToMe, EventType, EventMessage, EventPlainText


async def event(e: Event) -> Event:
    return e


async def event_type(t: str = EventType()) -> str:
    return t


async def event_message(msg: Message = EventMessage()) -> Message:
    return msg


async def event_plain_text(text: str = EventPlainText()) -> str:
    return text


async def event_to_me(to_me: bool = EventToMe()) -> bool:
    return to_me
