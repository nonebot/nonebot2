from typing import Union, TypeVar

from nonebot.adapters import Event, Message
from nonebot.params import EventToMe, EventType, EventMessage, EventPlainText


async def event(e: Event) -> Event:
    return e


async def legacy_event(event):
    return event


async def not_legacy_event(event: int):
    ...


class FooEvent(Event):
    ...


async def sub_event(e: FooEvent) -> FooEvent:
    return e


class BarEvent(Event):
    ...


async def union_event(e: Union[FooEvent, BarEvent]) -> Union[FooEvent, BarEvent]:
    return e


E = TypeVar("E", bound=Event)


async def generic_event(e: E) -> E:
    return e


CE = TypeVar("CE", Event, None)


async def generic_event_none(e: CE) -> CE:
    return e


async def not_event(e: Union[int, Event]):
    ...


async def event_type(t: str = EventType()) -> str:
    return t


async def event_message(msg: Message = EventMessage()) -> Message:
    return msg


async def event_plain_text(text: str = EventPlainText()) -> str:
    return text


async def event_to_me(to_me: bool = EventToMe()) -> bool:
    return to_me
