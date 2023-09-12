from nonebot import MatcherGroup


async def falsy():
    return False


async def truthy():
    return True


async def error():
    raise RuntimeError


test_check = MatcherGroup(type="test")
