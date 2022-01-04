from nonebot.matcher import Matcher

test_type_updater = Matcher.new(type_="test")

test_custom_updater = Matcher.new(type_="test")


@test_custom_updater.type_updater
async def _() -> str:
    return "custom"
