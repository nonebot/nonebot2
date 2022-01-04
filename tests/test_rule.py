import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_command(app: App):
    from nonebot.consts import CMD_KEY, PREFIX_KEY
    from nonebot.rule import Rule, CommandRule, command

    test_command = command("help")
    dependent = list(test_command.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, CommandRule)
    assert checker.cmds == [("help",)]

    state = {PREFIX_KEY: {CMD_KEY: ("help",)}}
    assert await dependent(state=state)
