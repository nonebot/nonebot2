from nonebot import MatcherGroup


async def falsy():
    return False


async def truthy():
    return True


async def error():
    raise RuntimeError


test_check = MatcherGroup(type="test")
test_check.on(permission=falsy)
test_check.on(permission=truthy)
test_check.on(permission=error)
test_check.on(rule=falsy)
test_check.on(rule=truthy)
test_check.on(rule=error)
