from typing import Dict, AsyncGenerator

from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot.message import IgnoredException, event_preprocessor

_running_matcher: Dict[str, int] = {}


async def matcher_mutex(event: Event) -> AsyncGenerator[bool, None]:
    result = False
    try:
        session_id = event.get_session_id()
    except Exception:
        yield result
    else:
        current_event_id = id(event)
        event_id = _running_matcher.get(session_id, None)
        if event_id:
            result = event_id != current_event_id
        else:
            _running_matcher[session_id] = current_event_id
        yield result
        if not result:
            del _running_matcher[session_id]


@event_preprocessor
async def preprocess(mutex: bool = Depends(matcher_mutex)):
    if mutex:
        raise IgnoredException("Another matcher running")
