from collections.abc import AsyncGenerator

from nonebot.adapters import Event
from nonebot.message import IgnoredException, event_preprocessor
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="唯一会话",
    description="限制同一会话内同时只能运行一个响应器",
    usage="加载插件后自动生效",
    type="application",
    homepage="https://github.com/nonebot/nonebot2/blob/master/nonebot/plugins/single_session.py",
    config=None,
    supported_adapters=None,
)

_running_matcher: dict[str, int] = {}


async def matcher_mutex(event: Event) -> AsyncGenerator[bool, None]:
    result = False
    try:
        session_id = event.get_session_id()
    except Exception:
        yield result
    else:
        current_event_id = id(event)
        if event_id := _running_matcher.get(session_id):
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
