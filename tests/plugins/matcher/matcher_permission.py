from nonebot.matcher import Matcher
from nonebot.permission import Permission

default_permission = Permission()

test_permission_updater = Matcher.new(permission=default_permission)

test_custom_updater = Matcher.new(permission=default_permission)


@test_custom_updater.permission_updater
async def _() -> Permission:
    return default_permission
