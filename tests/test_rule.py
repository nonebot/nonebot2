import sys
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

    def _is_eq(a: Rule, b: Rule) -> bool:
        return {d.call for d in a.checkers} == {d.call for d in b.checkers}

    assert _is_eq(Rule(truthy) & None, Rule(truthy))
    assert _is_eq(Rule(truthy) & falsy, Rule(truthy, falsy))
    assert _is_eq(Rule(truthy) & Rule(falsy), Rule(truthy, falsy))

    assert _is_eq(None & Rule(truthy), Rule(truthy))
    assert _is_eq(truthy & Rule(falsy), Rule(truthy, falsy))

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
    "msg,ignorecase,type,text,expected",
    [
        ("fullmatch", False, "message", "fullmatch", True),
        ("fullmatch", False, "message", "Fullmatch", False),
        ("fullmatch", True, "message", "fullmatch", True),
        ("fullmatch", True, "message", "Fullmatch", True),
        ("fullmatch", False, "message", "fullfoo", False),
        ("fullmatch", False, "message", "_fullmatch_", False),
        (("fullmatch", "foo"), False, "message", "fullmatchfoo", False),
        ("fullmatch", False, "notice", "foo", False),
    ],
)
async def test_fullmatch(
    app: App,
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: str,
    expected: bool,
):
    from nonebot.rule import FullmatchRule, fullmatch

    test_fullmatch = fullmatch(msg, ignorecase)
    dependent = list(test_fullmatch.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, FullmatchRule)
    assert checker.msg == {msg} if isinstance(msg, str) else {*msg}
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


@pytest.mark.asyncio
async def test_shell_command(app: App):
    from nonebot.typing import T_State
    from nonebot.exception import ParserExit
    from nonebot.consts import CMD_KEY, PREFIX_KEY, SHELL_ARGS, SHELL_ARGV, CMD_ARG_KEY
    from nonebot.rule import Namespace, ArgumentParser, ShellCommandRule, shell_command

    state: T_State
    CMD = ("test",)
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    test_not_cmd = shell_command(CMD)
    dependent = list(test_not_cmd.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = Message()
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: ("not",), CMD_ARG_KEY: message}}
    assert not await dependent(event=event, state=state)

    test_no_parser = shell_command(CMD)
    dependent = list(test_no_parser.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = Message()
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
    assert await dependent(event=event, state=state)
    assert state[SHELL_ARGV] == []
    assert SHELL_ARGS not in state

    parser = ArgumentParser("test")
    parser.add_argument("-a", required=True)

    test_simple_parser = shell_command(CMD, parser=parser)
    dependent = list(test_simple_parser.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = Message("-a 1")
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
    assert await dependent(event=event, state=state)
    assert state[SHELL_ARGV] == ["-a", "1"]
    assert state[SHELL_ARGS] == Namespace(a="1")

    test_parser_help = shell_command(CMD, parser=parser)
    dependent = list(test_parser_help.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = Message("-h")
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
    assert await dependent(event=event, state=state)
    assert state[SHELL_ARGV] == ["-h"]
    assert isinstance(state[SHELL_ARGS], ParserExit)
    assert state[SHELL_ARGS].status == 0
    assert state[SHELL_ARGS].message == parser.format_help()

    test_parser_error = shell_command(CMD, parser=parser)
    dependent = list(test_parser_error.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = Message()
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
    assert await dependent(event=event, state=state)
    assert state[SHELL_ARGV] == []
    assert isinstance(state[SHELL_ARGS], ParserExit)
    assert state[SHELL_ARGS].status != 0

    test_message_parser = shell_command(CMD, parser=parser)
    dependent = list(test_message_parser.checkers)[0]
    checker = dependent.call
    assert isinstance(checker, ShellCommandRule)
    message = MessageSegment.text("-a") + MessageSegment.image("test")
    event = make_fake_event(_message=message)()
    state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
    assert await dependent(event=event, state=state)
    assert state[SHELL_ARGV] == ["-a", MessageSegment.image("test")]
    assert state[SHELL_ARGS] == Namespace(a=MessageSegment.image("test"))

    if sys.version_info >= (3, 9):
        parser = ArgumentParser("test", exit_on_error=False)
        parser.add_argument("-a", required=True)

        test_not_exit = shell_command(CMD, parser=parser)
        dependent = list(test_not_exit.checkers)[0]
        checker = dependent.call
        assert isinstance(checker, ShellCommandRule)
        message = Message()
        event = make_fake_event(_message=message)()
        state = {PREFIX_KEY: {CMD_KEY: CMD, CMD_ARG_KEY: message}}
        assert await dependent(event=event, state=state)
        assert state[SHELL_ARGV] == []
        assert isinstance(state[SHELL_ARGS], ParserExit)
        assert state[SHELL_ARGS].status != 0


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
