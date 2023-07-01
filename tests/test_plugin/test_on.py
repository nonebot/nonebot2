from typing import Type, Callable, Optional

import pytest

import nonebot
from nonebot.adapters import Event
from nonebot.typing import T_RuleChecker
from nonebot.matcher import Matcher, matchers
from nonebot.rule import (
    RegexRule,
    IsTypeRule,
    CommandRule,
    EndswithRule,
    KeywordsRule,
    FullmatchRule,
    StartswithRule,
    ShellCommandRule,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("matcher_name", "pre_rule_factory", "has_permission"),
    [
        pytest.param("matcher_on", None, True),
        pytest.param("matcher_on_metaevent", None, False),
        pytest.param("matcher_on_message", None, True),
        pytest.param("matcher_on_notice", None, False),
        pytest.param("matcher_on_request", None, False),
        pytest.param(
            "matcher_on_startswith", lambda e: StartswithRule(("test",)), True
        ),
        pytest.param("matcher_on_endswith", lambda e: EndswithRule(("test",)), True),
        pytest.param("matcher_on_fullmatch", lambda e: FullmatchRule(("test",)), True),
        pytest.param("matcher_on_keyword", lambda e: KeywordsRule("test"), True),
        pytest.param("matcher_on_command", lambda e: CommandRule([("test",)]), True),
        pytest.param(
            "matcher_on_shell_command",
            lambda e: ShellCommandRule([("test",)], None),
            True,
        ),
        pytest.param("matcher_on_regex", lambda e: RegexRule("test"), True),
        pytest.param("matcher_on_type", lambda e: IsTypeRule(e), True),
        pytest.param(
            "matcher_prefix_cmd",
            lambda e: CommandRule([("prefix", "sub"), ("help",), ("help", "foo")]),
            True,
        ),
        pytest.param(
            "matcher_prefix_shell_cmd",
            lambda e: ShellCommandRule(
                [("prefix", "sub"), ("help",), ("help", "foo")], None
            ),
            True,
        ),
        pytest.param(
            "matcher_prefix_aliases_cmd",
            lambda e: CommandRule(
                [("prefix", "sub"), ("prefix", "help"), ("prefix", "help", "foo")]
            ),
            True,
        ),
        pytest.param(
            "matcher_prefix_aliases_shell_cmd",
            lambda e: ShellCommandRule(
                [("prefix", "sub"), ("prefix", "help"), ("prefix", "help", "foo")], None
            ),
            True,
        ),
        pytest.param("matcher_group_on", None, True),
        pytest.param("matcher_group_on_metaevent", None, False),
        pytest.param("matcher_group_on_message", None, True),
        pytest.param("matcher_group_on_notice", None, False),
        pytest.param("matcher_group_on_request", None, False),
        pytest.param(
            "matcher_group_on_startswith",
            lambda e: StartswithRule(("test",)),
            True,
        ),
        pytest.param(
            "matcher_group_on_endswith",
            lambda e: EndswithRule(("test",)),
            True,
        ),
        pytest.param(
            "matcher_group_on_fullmatch",
            lambda e: FullmatchRule(("test",)),
            True,
        ),
        pytest.param("matcher_group_on_keyword", lambda e: KeywordsRule("test"), True),
        pytest.param(
            "matcher_group_on_command",
            lambda e: CommandRule([("test",)]),
            True,
        ),
        pytest.param(
            "matcher_group_on_shell_command",
            lambda e: ShellCommandRule([("test",)], None),
            True,
        ),
        pytest.param("matcher_group_on_regex", lambda e: RegexRule("test"), True),
        pytest.param("matcher_group_on_type", lambda e: IsTypeRule(e), True),
    ],
)
async def test_on(
    matcher_name: str,
    pre_rule_factory: Optional[Callable[[Type[Event]], T_RuleChecker]],
    has_permission: bool,
):
    import plugins.plugin.matchers as module
    from plugins.plugin.matchers import (
        TestEvent,
        rule,
        state,
        handler,
        priority,
        permission,
        expire_time,
    )

    matcher = getattr(module, matcher_name)
    assert issubclass(matcher, Matcher), f"{matcher_name} should be a Matcher"

    pre_rule = pre_rule_factory(TestEvent) if pre_rule_factory else None

    plugin = nonebot.get_plugin("plugin")
    assert plugin, "plugin should be loaded"

    assert {dependent.call for dependent in matcher.rule.checkers} == (
        {pre_rule, rule} if pre_rule else {rule}
    )
    if has_permission:
        assert {dependent.call for dependent in matcher.permission.checkers} == {
            permission
        }
    else:
        assert not matcher.permission.checkers
    assert [dependent.call for dependent in matcher.handlers] == [handler]
    assert matcher.temp is True
    assert matcher.expire_time == expire_time
    assert matcher in matchers[priority]
    assert matcher.block is True
    assert matcher._default_state == state

    assert matcher.plugin is plugin
    assert matcher in plugin.matcher
    assert matcher.module is module
    assert matcher.plugin_name == "plugin"
    assert matcher.module_name == "plugins.plugin.matchers"


@pytest.mark.asyncio
async def test_runtime_on():
    import plugins.plugin.matchers as module
    from plugins.plugin.matchers import matcher_on_factory

    matcher = matcher_on_factory()

    plugin = nonebot.get_plugin("plugin")
    assert plugin, "plugin should be loaded"

    try:
        assert matcher.plugin is plugin
        assert matcher not in plugin.matcher
        assert matcher.module is module
        assert matcher.plugin_name == "plugin"
        assert matcher.module_name == "plugins.plugin.matchers"
    finally:
        matcher.destroy()
