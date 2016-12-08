from datetime import datetime, timedelta

from cachetools import TTLCache as TTLDict

from filter import add_filter
from little_shit import get_target
from commands import core

_freq_count = TTLDict(maxsize=10000, ttl=2 * 60 * 60)
_max_message_count_per_hour = 150


def _limiter(ctx_msg):
    target = get_target(ctx_msg)
    if target not in _freq_count:
        # First message of this target in 2 hours (_freq_count's ttl)
        _freq_count[target] = (0, datetime.now())

    count, last_check_dt = _freq_count[target]
    now_dt = datetime.now()
    delta = now_dt - last_check_dt

    if delta >= timedelta(hours=1):
        count = 0
        last_check_dt = now_dt

    if count >= _max_message_count_per_hour:
        # Too many messages in this hour
        core.echo('我们聊天太频繁啦，休息一会儿再聊吧～', ctx_msg)
        count = -1

    if count >= 0:
        count += 1

    _freq_count[target] = (count, last_check_dt)
    return count >= 0


add_filter(_limiter, 100)
