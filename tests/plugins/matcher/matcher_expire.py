from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from nonebot.matcher import Matcher

test_temp_matcher = Matcher.new("test", temp=True)
test_datetime_matcher = Matcher.new(
    "test", expire_time=datetime.now() - timedelta(seconds=1)
)
test_aware_datetime_matcher = Matcher.new(
    "test",
    expire_time=datetime(
        2000, 11, 5, 1, 30, tzinfo=ZoneInfo("America/New_York"), fold=1
    ),
)
test_timedelta_matcher = Matcher.new("test", expire_time=timedelta(seconds=-1))
