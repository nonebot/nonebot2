from typing import Dict, Optional

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor, run_postprocessor, IgnoredException

_running_matcher: Dict[str, bool] = {}


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    # TODO
    pass


@run_postprocessor
async def _(matcher: Matcher, exception: Optional[Exception], bot: Bot, event: Event, state: T_State):
    # TODO
    pass
