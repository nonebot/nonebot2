from contextlib import suppress
import re

from exceptiongroup import BaseExceptionGroup
from nonebug import App
import pytest

from nonebot.consts import (
    ARG_KEY,
    CMD_ARG_KEY,
    CMD_KEY,
    CMD_START_KEY,
    CMD_WHITESPACE_KEY,
    ENDSWITH_KEY,
    FULLMATCH_KEY,
    KEYWORD_KEY,
    PREFIX_KEY,
    RAW_CMD_KEY,
    RECEIVE_KEY,
    REGEX_MATCHED,
    SHELL_ARGS,
    SHELL_ARGV,
    STARTSWITH_KEY,
)
from nonebot.dependencies import Dependent
from nonebot.exception import PausedException, RejectedException, TypeMisMatch
from nonebot.matcher import Matcher
from nonebot.params import (
    ArgParam,
    BotParam,
    DefaultParam,
    DependParam,
    EventParam,
    ExceptionParam,
    MatcherParam,
    StateParam,
)
from utils import FakeMessage, make_fake_event

UNKNOWN_PARAM = "Unknown parameter"


@pytest.mark.anyio
async def test_depend(app: App):
    from plugins.param.param_depend import (
        ClassDependency,
        annotated_class_depend,
        annotated_depend,
        annotated_multi_depend,
        annotated_prior_depend,
        cache_exception_func1,
        cache_exception_func2,
        class_depend,
        depends,
        runned,
        sub_type_mismatch,
        test_depends,
        validate,
        validate_fail,
        validate_field,
        validate_field_fail,
    )

    async with app.test_dependent(depends, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)

    assert len(runned) == 1
    assert runned[0] == 1

    runned.clear()

    async with app.test_matcher(test_depends) as ctx:
        bot = ctx.create_bot()
        event_next = make_fake_event()()
        ctx.receive_event(bot, event_next)

    assert runned == [1, 1]

    runned.clear()

    async with app.test_dependent(class_depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(ClassDependency(x=1, y=2))

    async with app.test_dependent(annotated_depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)

    async with app.test_dependent(
        annotated_prior_depend, allow_types=[DependParam]
    ) as ctx:
        ctx.should_return(1)

    async with app.test_dependent(
        annotated_multi_depend, allow_types=[DependParam]
    ) as ctx:
        ctx.should_return(1)

    assert runned == [1, 1, 1]

    runned.clear()

    async with app.test_dependent(
        annotated_class_depend, allow_types=[DependParam]
    ) as ctx:
        ctx.should_return(ClassDependency(x=1, y=2))

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:  # noqa: PT012
        async with app.test_dependent(
            sub_type_mismatch, allow_types=[DependParam, BotParam]
        ) as ctx:
            bot = ctx.create_bot()
            ctx.pass_params(bot=bot)

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    async with app.test_dependent(validate, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:
        async with app.test_dependent(validate_fail, allow_types=[DependParam]) as ctx:
            ...

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    async with app.test_dependent(validate_field, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:
        async with app.test_dependent(
            validate_field_fail, allow_types=[DependParam]
        ) as ctx:
            ...

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    # test cache reuse when exception raised
    dependency_cache = {}
    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:
        async with app.test_dependent(
            cache_exception_func1, allow_types=[DependParam]
        ) as ctx:
            ctx.pass_params(dependency_cache=dependency_cache)

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    # dependency solve tasks should be shielded even if one of them raises an exception
    assert len(dependency_cache) == 2

    async with app.test_dependent(
        cache_exception_func2, allow_types=[DependParam]
    ) as ctx:
        ctx.pass_params(dependency_cache=dependency_cache)
        ctx.should_return(1)


@pytest.mark.anyio
async def test_bot(app: App):
    from plugins.param.param_bot import (
        FooBot,
        generic_bot,
        generic_bot_none,
        get_bot,
        legacy_bot,
        not_bot,
        not_legacy_bot,
        postpone_bot,
        sub_bot,
        union_bot,
    )

    async with app.test_dependent(get_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot()
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    async with app.test_dependent(postpone_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot()
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    async with app.test_dependent(legacy_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot()
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_legacy_bot, allow_types=[BotParam])

    async with app.test_dependent(sub_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot(base=FooBot)
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:  # noqa: PT012
        async with app.test_dependent(sub_bot, allow_types=[BotParam]) as ctx:
            bot = ctx.create_bot()
            ctx.pass_params(bot=bot)

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    async with app.test_dependent(union_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot(base=FooBot)
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    async with app.test_dependent(generic_bot, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot()
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    async with app.test_dependent(generic_bot_none, allow_types=[BotParam]) as ctx:
        bot = ctx.create_bot()
        ctx.pass_params(bot=bot)
        ctx.should_return(bot)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_bot, allow_types=[BotParam])


@pytest.mark.anyio
async def test_event(app: App):
    from plugins.param.param_event import (
        FooEvent,
        event,
        event_message,
        event_plain_text,
        event_to_me,
        event_type,
        generic_event,
        generic_event_none,
        legacy_event,
        not_event,
        not_legacy_event,
        postpone_event,
        sub_event,
        union_event,
    )

    fake_message = FakeMessage("text")
    fake_event = make_fake_event(_message=fake_message)()
    fake_fooevent = make_fake_event(_base=FooEvent)()

    async with app.test_dependent(event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event)

    async with app.test_dependent(postpone_event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event)

    async with app.test_dependent(legacy_event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_legacy_event, allow_types=[EventParam])

    async with app.test_dependent(sub_event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_fooevent)
        ctx.should_return(fake_fooevent)

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:
        async with app.test_dependent(sub_event, allow_types=[EventParam]) as ctx:
            ctx.pass_params(event=fake_event)

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    async with app.test_dependent(union_event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_fooevent)
        ctx.should_return(fake_fooevent)

    async with app.test_dependent(generic_event, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event)

    async with app.test_dependent(generic_event_none, allow_types=[EventParam]) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_event, allow_types=[EventParam])

    async with app.test_dependent(
        event_type, allow_types=[EventParam, DependParam]
    ) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event.get_type())

    async with app.test_dependent(
        event_message, allow_types=[EventParam, DependParam]
    ) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event.get_message())

    async with app.test_dependent(
        event_plain_text, allow_types=[EventParam, DependParam]
    ) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event.get_plaintext())

    async with app.test_dependent(
        event_to_me, allow_types=[EventParam, DependParam]
    ) as ctx:
        ctx.pass_params(event=fake_event)
        ctx.should_return(fake_event.is_tome())


@pytest.mark.anyio
async def test_state(app: App):
    from plugins.param.param_state import (
        command,
        command_arg,
        command_start,
        command_whitespace,
        endswith,
        fullmatch,
        keyword,
        legacy_state,
        not_legacy_state,
        postpone_state,
        raw_command,
        regex_dict,
        regex_group,
        regex_matched,
        regex_str,
        shell_command_args,
        shell_command_argv,
        startswith,
        state,
    )

    fake_message = FakeMessage("text")
    fake_matched = re.match(r"\[cq:(?P<type>.*?),(?P<arg>.*?)\]", "[cq:test,arg=value]")
    fake_state = {
        PREFIX_KEY: {
            CMD_KEY: ("cmd",),
            RAW_CMD_KEY: "/cmd",
            CMD_START_KEY: "/",
            CMD_ARG_KEY: fake_message,
            CMD_WHITESPACE_KEY: " ",
        },
        SHELL_ARGV: ["-h"],
        SHELL_ARGS: {"help": True},
        REGEX_MATCHED: fake_matched,
        STARTSWITH_KEY: "startswith",
        ENDSWITH_KEY: "endswith",
        FULLMATCH_KEY: "fullmatch",
        KEYWORD_KEY: "keyword",
    }

    async with app.test_dependent(state, allow_types=[StateParam]) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state)

    async with app.test_dependent(postpone_state, allow_types=[StateParam]) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state)

    async with app.test_dependent(legacy_state, allow_types=[StateParam]) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_legacy_state, allow_types=[StateParam])

    async with app.test_dependent(
        command, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[PREFIX_KEY][CMD_KEY])

    async with app.test_dependent(
        raw_command, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[PREFIX_KEY][RAW_CMD_KEY])

    async with app.test_dependent(
        command_arg, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[PREFIX_KEY][CMD_ARG_KEY])

    async with app.test_dependent(
        command_start, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[PREFIX_KEY][CMD_START_KEY])

    async with app.test_dependent(
        command_whitespace, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[PREFIX_KEY][CMD_WHITESPACE_KEY])

    async with app.test_dependent(
        shell_command_argv, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[SHELL_ARGV])

    async with app.test_dependent(
        shell_command_args, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[SHELL_ARGS])

    async with app.test_dependent(
        regex_matched, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[REGEX_MATCHED])

    async with app.test_dependent(
        regex_str, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(
            ("[cq:test,arg=value]", "test", "arg=value", ("test", "arg=value"))
        )

    async with app.test_dependent(
        regex_group, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(("test", "arg=value"))

    async with app.test_dependent(
        regex_dict, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return({"type": "test", "arg": "arg=value"})

    async with app.test_dependent(
        startswith, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[STARTSWITH_KEY])

    async with app.test_dependent(
        endswith, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[ENDSWITH_KEY])

    async with app.test_dependent(
        fullmatch, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[FULLMATCH_KEY])

    async with app.test_dependent(
        keyword, allow_types=[StateParam, DependParam]
    ) as ctx:
        ctx.pass_params(state=fake_state)
        ctx.should_return(fake_state[KEYWORD_KEY])


@pytest.mark.anyio
async def test_matcher(app: App):
    from plugins.param.param_matcher import (
        FooMatcher,
        generic_matcher,
        generic_matcher_none,
        last_receive,
        legacy_matcher,
        matcher,
        not_legacy_matcher,
        not_matcher,
        pause_prompt_result,
        postpone_matcher,
        receive,
        receive_prompt_result,
        sub_matcher,
        union_matcher,
    )

    fake_matcher = Matcher()
    foo_matcher = FooMatcher()

    async with app.test_dependent(matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(fake_matcher)

    async with app.test_dependent(postpone_matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(fake_matcher)

    async with app.test_dependent(legacy_matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(fake_matcher)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_legacy_matcher, allow_types=[MatcherParam])

    async with app.test_dependent(sub_matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=foo_matcher)
        ctx.should_return(foo_matcher)

    with pytest.raises((TypeMisMatch, BaseExceptionGroup)) as exc_info:
        async with app.test_dependent(sub_matcher, allow_types=[MatcherParam]) as ctx:
            ctx.pass_params(matcher=fake_matcher)

    if isinstance(exc_info.value, BaseExceptionGroup):
        assert exc_info.group_contains(TypeMisMatch)

    async with app.test_dependent(union_matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=foo_matcher)
        ctx.should_return(foo_matcher)

    async with app.test_dependent(generic_matcher, allow_types=[MatcherParam]) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(fake_matcher)

    async with app.test_dependent(
        generic_matcher_none, allow_types=[MatcherParam]
    ) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(fake_matcher)

    with pytest.raises(ValueError, match=UNKNOWN_PARAM):
        app.test_dependent(not_matcher, allow_types=[MatcherParam])

    event = make_fake_event()()
    fake_matcher.set_receive("test", event)
    event_next = make_fake_event()()
    fake_matcher.set_receive("", event_next)

    async with app.test_dependent(
        receive, allow_types=[MatcherParam, DependParam]
    ) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(event)

    async with app.test_dependent(
        last_receive, allow_types=[MatcherParam, DependParam]
    ) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(event_next)

    fake_matcher.set_target(RECEIVE_KEY.format(id="test"), cache=False)

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        ctx.should_call_send(event, "test", result=True, bot=bot)
        with fake_matcher.ensure_context(bot, event):
            with suppress(RejectedException):
                await fake_matcher.reject("test")

    async with app.test_dependent(
        receive_prompt_result, allow_types=[MatcherParam, DependParam]
    ) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(True)

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        ctx.should_call_send(event, "test", result=False, bot=bot)
        with fake_matcher.ensure_context(bot, event):
            fake_matcher.set_target("test")
            with suppress(PausedException):
                await fake_matcher.pause("test")

    async with app.test_dependent(
        pause_prompt_result, allow_types=[MatcherParam, DependParam]
    ) as ctx:
        ctx.pass_params(matcher=fake_matcher)
        ctx.should_return(False)


@pytest.mark.anyio
async def test_arg(app: App):
    from plugins.param.param_arg import (
        annotated_arg,
        annotated_arg_plain_text,
        annotated_arg_prompt_result,
        annotated_arg_str,
        annotated_multi_arg,
        annotated_prior_arg,
        arg,
        arg_plain_text,
        arg_str,
    )

    matcher = Matcher()
    event = make_fake_event()()
    message = FakeMessage("text")
    matcher.set_arg("key", message)

    async with app.test_dependent(arg, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message)

    async with app.test_dependent(arg_str, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(str(message))

    async with app.test_dependent(arg_plain_text, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message.extract_plain_text())

    async with app.test_dependent(annotated_arg, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message)

    async with app.test_dependent(annotated_arg_str, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(str(message))

    async with app.test_dependent(
        annotated_arg_plain_text, allow_types=[ArgParam]
    ) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message.extract_plain_text())

    matcher.set_target(ARG_KEY.format(key="key"), cache=False)

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        ctx.should_call_send(event, "test", result="arg", bot=bot)
        with matcher.ensure_context(bot, event):
            with suppress(RejectedException):
                await matcher.reject("test")

    async with app.test_dependent(
        annotated_arg_prompt_result, allow_types=[ArgParam]
    ) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return("arg")

    async with app.test_dependent(annotated_multi_arg, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message.extract_plain_text())

    async with app.test_dependent(annotated_prior_arg, allow_types=[ArgParam]) as ctx:
        ctx.pass_params(matcher=matcher)
        ctx.should_return(message.extract_plain_text())


@pytest.mark.anyio
async def test_exception(app: App):
    from plugins.param.param_exception import exc, legacy_exc

    exception = ValueError("test")
    async with app.test_dependent(exc, allow_types=[ExceptionParam]) as ctx:
        ctx.pass_params(exception=exception)
        ctx.should_return(exception)

    async with app.test_dependent(legacy_exc, allow_types=[ExceptionParam]) as ctx:
        ctx.pass_params(exception=exception)
        ctx.should_return(exception)


@pytest.mark.anyio
async def test_default(app: App):
    from plugins.param.param_default import default

    async with app.test_dependent(default, allow_types=[DefaultParam]) as ctx:
        ctx.should_return(1)


def test_priority():
    from plugins.param.priority import complex_priority

    dependent = Dependent[None].parse(
        call=complex_priority,
        allow_types=[
            DependParam,
            BotParam,
            EventParam,
            StateParam,
            MatcherParam,
            ArgParam,
            ExceptionParam,
            DefaultParam,
        ],
    )
    for param in dependent.params:
        if param.name == "sub":
            assert isinstance(param.field_info, DependParam)
        elif param.name == "bot":
            assert isinstance(param.field_info, BotParam)
        elif param.name == "event":
            assert isinstance(param.field_info, EventParam)
        elif param.name == "state":
            assert isinstance(param.field_info, StateParam)
        elif param.name == "matcher":
            assert isinstance(param.field_info, MatcherParam)
        elif param.name == "arg":
            assert isinstance(param.field_info, ArgParam)
        elif param.name == "exception":
            assert isinstance(param.field_info, ExceptionParam)
        elif param.name == "default":
            assert isinstance(param.field_info, DefaultParam)
        else:
            raise ValueError(f"unknown param {param.name}")
