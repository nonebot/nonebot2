from nonebot.internal.rule import Rule
from nonebot.internal.matcher import Matcher
from nonebot.internal.permission import Permission


async def bad():
    _ = 1 / 0
    return True


async def falsy():
    return False


def to_falsy_rule_matcher(handle):
    return Matcher.new(handlers=[handle], rule=Rule(falsy))


def to_bad_rule_matcher(handle):
    return Matcher.new(handlers=[handle], rule=Rule(bad))


def to_falsy_perm_matcher(handle):
    return Matcher.new(handlers=[handle], permission=Permission(falsy))


def to_bad_perm_matcher(handle):
    return Matcher.new(handlers=[handle], permission=Permission(bad))
