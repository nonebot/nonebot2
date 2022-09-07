from typing import Union

from nonebot.adapters import Event, Message
from nonebot.params import event_type, event_to_me, event_message, event_plain_text


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


async def not_event(e: Union[int, Event]):
    ...


async def event_type_test(t: str = event_type()) -> str:
    return t


async def event_message_test(msg: Message = event_message()) -> Message:
    return msg


async def event_plain_text_test(text: str = event_plain_text()) -> str:
    return text


async def event_to_me_test(to_me: bool = event_to_me()) -> bool:
    return to_me
