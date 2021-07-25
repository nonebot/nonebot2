from typing import Dict, Optional

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor, run_postprocessor, IgnoredException

_running_matcher: Dict[str, int] = {}


@run_preprocessor
async def preprocess(matcher: Matcher, bot: Bot, event: Event, state: T_State):
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
async def postprocess(matcher: Matcher, exception: Optional[Exception],
                      bot: Bot, event: Event, state: T_State):
    try:
        session_id = event.get_session_id()
    except Exception:
        return
    if session_id in _running_matcher:
        del _running_matcher[session_id]
