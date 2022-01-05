from typing import Tuple, Union

import pytest
from nonebug import App

from utils import make_fake_event, make_fake_message


@pytest.mark.asyncio
async def test_rule(app: App):
    from nonebot.rule import Rule
    from nonebot.exception import SkippedException

    async def falsy():
        return False

    async def truthy():
        return True

    async def skipped() -> bool:
        raise SkippedException

    event = make_fake_event()()

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert await Rule(falsy)(bot, event, {}) == False
        assert await Rule(truthy)(bot, event, {}) == True
        assert await Rule(skipped)(bot, event, {}) == False
        assert await Rule(truthy, falsy)(bot, event, {}) == False
        assert await Rule(truthy, skipped)(bot, event, {}) == False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg,ignorecase,type,text,expected",
    [
        ("prefix", False, "message", "prefix_", True),
        ("prefix", False, "message", "Prefix_", False),
        ("prefix", True, "message", "prefix_", True),
        ("prefix", True, "message", "Prefix_", True),
        ("prefix", False, "message", "prefoo", False),
        ("prefix", False, "message", "fooprefix", False),
        (("prefix", "foo"), False, "message", "fooprefix", True),
        ("prefix", False, "notice", "foo", False),
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
        ("suffix", False, "message", "suffoo", False),
        ("suffix", False, "message", "suffixfoo", False),
        (("suffix", "foo"), False, "message", "suffixfoo", True),
        ("suffix", False, "notice", "foo", False),
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
@pytest.mark.parametrize(
    "kws,type,text,expected",
    [
        (("key",), "message", "_key_", True),
        (("key", "foo"), "message", "_foo_", True),
        (("key",), "notice", "foo", False),
    ],
)
async def test_keyword(
    app: App,
    kws: Tuple[str, ...],
    type: str,
    text: str,
    expected: bool,
):
    from nonebot.rule import KeywordsRule, keyword

    test_keyword = keyword(*kws)
    dependent = list(test_keyword.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, KeywordsRule)
    assert checker.keywords == kws

    message = make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cmds", [(("help",),), (("help", "foo"),), (("help",), ("foo",))]
)
async def test_command(app: App, cmds: Tuple[Tuple[str, ...]]):
    from nonebot.rule import CommandRule, command
    from nonebot.consts import CMD_KEY, PREFIX_KEY

    test_command = command(*cmds)
    dependent = list(test_command.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, CommandRule)
    assert checker.cmds == list(cmds)

    for cmd in cmds:
        state = {PREFIX_KEY: {CMD_KEY: cmd}}
        assert await dependent(state=state)


# TODO: shell command

# TODO: regex


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [True, False])
async def test_to_me(app: App, expected: bool):
    from nonebot.rule import ToMeRule, to_me

    test_keyword = to_me()
    dependent = list(test_keyword.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, ToMeRule)

    event = make_fake_event(_to_me=expected)()
    assert await dependent(event=event) == expected
