import sys
from typing import Dict, Tuple, Union, Optional

import pytest
from nonebug import App

from nonebot.typing import T_State
from utils import make_fake_event, make_fake_message
from nonebot.exception import ParserExit, SkippedException
from nonebot.consts import (
    CMD_KEY,
    REGEX_STR,
    PREFIX_KEY,
    REGEX_DICT,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    KEYWORD_KEY,
    REGEX_GROUP,
    ENDSWITH_KEY,
    FULLMATCH_KEY,
    REGEX_MATCHED,
    STARTSWITH_KEY,
)
from nonebot.rule import (
    Rule,
    ToMeRule,
    Namespace,
    RegexRule,
    IsTypeRule,
    CommandRule,
    EndswithRule,
    KeywordsRule,
    FullmatchRule,
    ArgumentParser,
    StartswithRule,
    ShellCommandRule,
    regex,
    to_me,
    command,
    is_type,
    keyword,
    endswith,
    fullmatch,
    startswith,
    shell_command,
)


@pytest.mark.asyncio
async def test_rule(app: App):
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
    "msg, ignorecase, type, text, expected",
    [
        ("prefix", False, "message", "prefix_", True),
        ("prefix", False, "message", "Prefix_", False),
        ("prefix", True, "message", "prefix_", True),
        ("prefix", True, "message", "Prefix_", True),
        ("prefix", False, "message", "prefoo", False),
        ("prefix", False, "message", "fooprefix", False),
        ("prefix", False, "message", None, False),
        (("prefix", "foo"), False, "message", "fooprefix", True),
        ("prefix", False, "notice", "foo", False),
    ],
)
async def test_startswith(
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: Optional[str],
    expected: bool,
):
    test_startswith = startswith(msg, ignorecase)
    dependent = list(test_startswith.checkers)[0]
    checker = dependent.call

    msg = (msg,) if isinstance(msg, str) else msg

    assert isinstance(checker, StartswithRule)
    assert checker.msg == msg
    assert checker.ignorecase == ignorecase

    message = text if text is None else make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    for prefix in msg:
        state = {STARTSWITH_KEY: prefix}
        assert await dependent(event=event, state=state) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg, ignorecase, type, text, expected",
    [
        ("suffix", False, "message", "_suffix", True),
        ("suffix", False, "message", "_Suffix", False),
        ("suffix", True, "message", "_suffix", True),
        ("suffix", True, "message", "_Suffix", True),
        ("suffix", False, "message", "suffoo", False),
        ("suffix", False, "message", "suffixfoo", False),
        ("suffix", False, "message", None, False),
        (("suffix", "foo"), False, "message", "suffixfoo", True),
        ("suffix", False, "notice", "foo", False),
    ],
)
async def test_endswith(
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: Optional[str],
    expected: bool,
):
    test_endswith = endswith(msg, ignorecase)
    dependent = list(test_endswith.checkers)[0]
    checker = dependent.call

    msg = (msg,) if isinstance(msg, str) else msg

    assert isinstance(checker, EndswithRule)
    assert checker.msg == msg
    assert checker.ignorecase == ignorecase

    message = text if text is None else make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    for suffix in msg:
        state = {ENDSWITH_KEY: suffix}
        assert await dependent(event=event, state=state) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg, ignorecase, type, text, expected",
    [
        ("fullmatch", False, "message", "fullmatch", True),
        ("fullmatch", False, "message", "Fullmatch", False),
        ("fullmatch", True, "message", "fullmatch", True),
        ("fullmatch", True, "message", "Fullmatch", True),
        ("fullmatch", False, "message", "fullfoo", False),
        ("fullmatch", False, "message", "_fullmatch_", False),
        ("fullmatch", False, "message", None, False),
        (("fullmatch", "foo"), False, "message", "fullmatchfoo", False),
        ("fullmatch", False, "notice", "foo", False),
    ],
)
async def test_fullmatch(
    msg: Union[str, Tuple[str, ...]],
    ignorecase: bool,
    type: str,
    text: Optional[str],
    expected: bool,
):
    test_fullmatch = fullmatch(msg, ignorecase)
    dependent = list(test_fullmatch.checkers)[0]
    checker = dependent.call

    msg = (msg,) if isinstance(msg, str) else msg

    assert isinstance(checker, FullmatchRule)
    assert checker.msg == msg
    assert checker.ignorecase == ignorecase

    message = text if text is None else make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    for full in msg:
        state = {FULLMATCH_KEY: full}
        assert await dependent(event=event, state=state) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kws, type, text, expected",
    [
        (("key",), "message", "_key_", True),
        (("key", "foo"), "message", "_foo_", True),
        (("key",), "message", None, False),
        (("key",), "notice", "foo", False),
        (("key",), "message", "foo", False),
    ],
)
async def test_keyword(
    kws: Tuple[str, ...],
    type: str,
    text: Optional[str],
    expected: bool,
):
    test_keyword = keyword(*kws)
    dependent = list(test_keyword.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, KeywordsRule)
    assert checker.keywords == kws

    message = text if text is None else make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    for kw in kws:
        state = {KEYWORD_KEY: kw}
        assert await dependent(event=event, state=state) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cmds", [(("help",),), (("help", "foo"),), (("help",), ("foo",))]
)
async def test_command(cmds: Tuple[Tuple[str, ...]]):
    test_command = command(*cmds)
    dependent = list(test_command.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, CommandRule)
    assert checker.cmds == cmds

    for cmd in cmds:
        state = {PREFIX_KEY: {CMD_KEY: cmd}}
        assert await dependent(state=state)


@pytest.mark.asyncio
async def test_shell_command():
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
    assert state[SHELL_ARGS].message.startswith(parser.format_usage() + "test: error:")

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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pattern, type, text, expected, matched, string, group, dict",
    [
        (
            r"(?P<key>key\d)",
            "message",
            "_key1_",
            True,
            "key1",
            "key1",
            ("key1",),
            {"key": "key1"},
        ),
        (r"foo", "message", None, False, None, None, None, None),
        (r"foo", "notice", "foo", False, None, None, None, None),
    ],
)
async def test_regex(
    pattern: str,
    type: str,
    text: Optional[str],
    expected: bool,
    matched: Optional[str],
    string: Optional[str],
    group: Optional[Tuple[str, ...]],
    dict: Optional[Dict[str, str]],
):
    test_regex = regex(pattern)
    dependent = list(test_regex.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, RegexRule)
    assert checker.regex == pattern

    message = text if text is None else make_fake_message()(text)
    event = make_fake_event(_type=type, _message=message)()
    state = {}
    assert await dependent(event=event, state=state) == expected
    assert state.get(REGEX_MATCHED) == matched
    assert state.get(REGEX_STR) == string
    assert state.get(REGEX_GROUP) == group
    assert state.get(REGEX_DICT) == dict


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [True, False])
async def test_to_me(expected: bool):
    test_to_me = to_me()
    dependent = list(test_to_me.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, ToMeRule)

    event = make_fake_event(_to_me=expected)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
async def test_is_type():
    Event1 = make_fake_event()
    Event2 = make_fake_event()
    Event3 = make_fake_event()

    test_type = is_type(Event1, Event2)
    dependent = list(test_type.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, IsTypeRule)

    event = Event1()
    assert await dependent(event=event)

    event = Event3()
    assert not await dependent(event=event)
