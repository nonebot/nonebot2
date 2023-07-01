from typing import Type
from datetime import datetime, timezone

from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot import (
    CommandGroup,
    MatcherGroup,
    on,
    on_type,
    on_regex,
    on_notice,
    on_command,
    on_keyword,
    on_message,
    on_request,
    on_endswith,
    on_fullmatch,
    on_metaevent,
    on_startswith,
    on_shell_command,
)


async def rule() -> bool:
    return True


async def permission() -> bool:
    return True


async def handler():
    return


expire_time = datetime.now(timezone.utc)
priority = 100
state = {"test": "test"}


matcher_on = on(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


def matcher_on_factory() -> Type[Matcher]:
    return on(
        "test",
        rule=rule,
        permission=permission,
        handlers=[handler],
        temp=True,
        expire_time=expire_time,
        priority=priority,
        block=True,
        state=state,
    )


matcher_on_metaevent = on_metaevent(
    rule=rule,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_message = on_message(
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_notice = on_notice(
    rule=rule,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_request = on_request(
    rule=rule,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_startswith = on_startswith(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_endswith = on_endswith(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_fullmatch = on_fullmatch(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_keyword = on_keyword(
    {"test"},
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_command = on_command(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_shell_command = on_shell_command(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


matcher_on_regex = on_regex(
    "test",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


class TestEvent(Event):
    ...


matcher_on_type = on_type(
    TestEvent,
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)


cmd_group = CommandGroup(
    "prefix",
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)
matcher_prefix_cmd = cmd_group.command("sub", aliases={"help", ("help", "foo")})
matcher_prefix_shell_cmd = cmd_group.shell_command(
    "sub", aliases={"help", ("help", "foo")}
)


cmd_group_prefix_aliases = CommandGroup(
    "prefix",
    prefix_aliases=True,
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)
matcher_prefix_aliases_cmd = cmd_group_prefix_aliases.command(
    "sub", aliases={"help", ("help", "foo")}
)
matcher_prefix_aliases_shell_cmd = cmd_group_prefix_aliases.shell_command(
    "sub", aliases={"help", ("help", "foo")}
)


matcher_group = MatcherGroup(
    rule=rule,
    permission=permission,
    handlers=[handler],
    temp=True,
    expire_time=expire_time,
    priority=priority,
    block=True,
    state=state,
)
matcher_group_on = matcher_group.on(type="test")
matcher_group_on_metaevent = matcher_group.on_metaevent()
matcher_group_on_message = matcher_group.on_message()
matcher_group_on_notice = matcher_group.on_notice()
matcher_group_on_request = matcher_group.on_request()
matcher_group_on_startswith = matcher_group.on_startswith("test")
matcher_group_on_endswith = matcher_group.on_endswith("test")
matcher_group_on_fullmatch = matcher_group.on_fullmatch("test")
matcher_group_on_keyword = matcher_group.on_keyword({"test"})
matcher_group_on_command = matcher_group.on_command("test")
matcher_group_on_shell_command = matcher_group.on_shell_command("test")
matcher_group_on_regex = matcher_group.on_regex("test")
matcher_group_on_type = matcher_group.on_type(TestEvent)
