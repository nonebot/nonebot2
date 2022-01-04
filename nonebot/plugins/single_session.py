from typing import Dict

from nonebot.adapters import Event
from nonebot.message import (
    IgnoredException,
    run_preprocessor,
    run_postprocessor,
)

_running_matcher: Dict[str, int] = {}


@run_preprocessor
async def preprocess(event: Event):
    try:
        session_id = event.get_session_id()
    except Exception:
        return
    current_event_id = id(event)
    event_id = _running_matcher.get(session_id, None)
    if event_id and event_id != current_event_id:
        raise IgnoredException("Another matcher running")

    _running_matcher[session_id] = current_event_id


@run_postprocessor
async def postprocess(event: Event):
    try:
        session_id = event.get_session_id()
    except Exception:
        return
    if session_id in _running_matcher:
        del _running_matcher[session_id]
