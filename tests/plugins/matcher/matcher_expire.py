from datetime import datetime, timedelta

from nonebot.matcher import Matcher

test_temp_matcher = Matcher.new("test", temp=True)
test_datetime_matcher = Matcher.new("test", expire_time=datetime.now())
test_timedelta_matcher = Matcher.new("test", expire_time=timedelta(seconds=-1))
