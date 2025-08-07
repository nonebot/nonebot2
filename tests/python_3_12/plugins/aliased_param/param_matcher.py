from nonebot.matcher import Matcher

type AliasedMatcher = Matcher


async def aliased_matcher(m: AliasedMatcher) -> Matcher:
    return m
