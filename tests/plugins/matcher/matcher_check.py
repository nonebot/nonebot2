from nonebot import MatcherGroup


async def falsy():
    return False


async def truthy():
    return True


async def error():
    raise RuntimeError


checks = [(falsy, False), (truthy, True), (error, False)]

test_check = MatcherGroup(type="test")
for check, result in checks:
    test_check.on(permission=check, state={"expect": result})
    test_check.on(rule=check, state={"expect": result})
