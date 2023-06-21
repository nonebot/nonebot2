from nonebot.matcher import Matcher
from nonebot.permission import USER, Permission

default_permission = Permission()
new_permission = Permission()

test_permission_updater = Matcher.new(permission=default_permission)

test_user_permission_updater = Matcher.new(
    permission=USER("test", perm=default_permission)
)

test_custom_updater = Matcher.new(permission=default_permission)


@test_custom_updater.permission_updater
async def _() -> Permission:
    return new_permission
