from typing import Type, Optional

import pytest

import nonebot
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
async def test_on():
    import plugins.plugin.matchers as module
    from plugins.plugin.matchers import (
        TestEvent,
        rule,
        state,
        handler,
        priority,
        matcher_on,
        permission,
        expire_time,
        matcher_on_type,
        matcher_sub_cmd,
        matcher_group_on,
        matcher_on_regex,
        matcher_on_notice,
        matcher_on_command,
        matcher_on_keyword,
        matcher_on_message,
        matcher_on_request,
        matcher_on_endswith,
        matcher_on_fullmatch,
        matcher_on_metaevent,
        matcher_group_on_type,
        matcher_on_startswith,
        matcher_sub_shell_cmd,
        matcher_group_on_regex,
        matcher_group_on_notice,
        matcher_group_on_command,
        matcher_group_on_keyword,
        matcher_group_on_message,
        matcher_group_on_request,
        matcher_on_shell_command,
        matcher_group_on_endswith,
        matcher_group_on_fullmatch,
        matcher_group_on_metaevent,
        matcher_group_on_startswith,
        matcher_group_on_shell_command,
    )

    plugin = nonebot.get_plugin("plugin")

    def _check(
        matcher: Type[Matcher],
        pre_rule: Optional[T_RuleChecker],
        has_permission: bool,
    ):
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
        assert matcher.module is module
        assert matcher.plugin_name == "plugin"
        assert matcher.module_name == "plugins.plugin.matchers"

    _check(matcher_on, None, True)
    _check(matcher_on_metaevent, None, False)
    _check(matcher_on_message, None, True)
    _check(matcher_on_notice, None, False)
    _check(matcher_on_request, None, False)
    _check(matcher_on_startswith, StartswithRule(("test",)), True)
    _check(matcher_on_endswith, EndswithRule(("test",)), True)
    _check(matcher_on_fullmatch, FullmatchRule(("test",)), True)
    _check(matcher_on_keyword, KeywordsRule("test"), True)
    _check(matcher_on_command, CommandRule([("test",)]), True)
    _check(matcher_on_shell_command, ShellCommandRule([("test",)], None), True)
    _check(matcher_on_regex, RegexRule("test"), True)
    _check(matcher_on_type, IsTypeRule(TestEvent), True)
    _check(matcher_sub_cmd, CommandRule([("test", "sub")]), True)
    _check(matcher_sub_shell_cmd, ShellCommandRule([("test", "sub")], None), True)
    _check(matcher_group_on, None, True)
    _check(matcher_group_on_metaevent, None, False)
    _check(matcher_group_on_message, None, True)
    _check(matcher_group_on_notice, None, False)
    _check(matcher_group_on_request, None, False)
    _check(matcher_group_on_startswith, StartswithRule(("test",)), True)
    _check(matcher_group_on_endswith, EndswithRule(("test",)), True)
    _check(matcher_group_on_fullmatch, FullmatchRule(("test",)), True)
    _check(matcher_group_on_keyword, KeywordsRule("test"), True)
    _check(matcher_group_on_command, CommandRule([("test",)]), True)
    _check(matcher_group_on_shell_command, ShellCommandRule([("test",)], None), True)
    _check(matcher_group_on_regex, RegexRule("test"), True)
    _check(matcher_group_on_type, IsTypeRule(TestEvent), True)
