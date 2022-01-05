from typing import Tuple, Union

import pytest
from nonebug import App

from utils import make_fake_event, make_fake_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg,ignorecase,type,text,expected",
    [
        ("prefix", False, "message", "prefix_", True),
        ("prefix", False, "message", "Prefix_", False),
        ("prefix", True, "message", "prefix_", True),
        ("prefix", True, "message", "Prefix_", True),
    ],
)
async def test_startswith(
    app: App,
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: str,
    expected: bool,
):
    from nonebot.rule import StartswithRule, startswith

    test_startswith = startswith(msg, ignorecase)
    dependent = list(test_startswith.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, StartswithRule)
    assert checker.msg == (msg,) if isinstance(msg, str) else msg
    assert checker.ignorecase == ignorecase

    message = make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg,ignorecase,type,text,expected",
    [
        ("suffix", False, "message", "_suffix", True),
        ("suffix", False, "message", "_Suffix", False),
        ("suffix", True, "message", "_suffix", True),
        ("suffix", True, "message", "_Suffix", True),
    ],
)
async def test_endswith(
    app: App,
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: str,
    expected: bool,
):
    from nonebot.rule import EndswithRule, endswith

    test_endswith = endswith(msg, ignorecase)
    dependent = list(test_endswith.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, EndswithRule)
    assert checker.msg == (msg,) if isinstance(msg, str) else msg
    assert checker.ignorecase == ignorecase

    message = make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
async def test_command(app: App):
    from nonebot.rule import CommandRule, command
    from nonebot.consts import CMD_KEY, PREFIX_KEY

    test_command = command("help")
    dependent = list(test_command.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, CommandRule)
    assert checker.cmds == [("help",)]

    state = {PREFIX_KEY: {CMD_KEY: ("help",)}}
    assert await dependent(state=state)
