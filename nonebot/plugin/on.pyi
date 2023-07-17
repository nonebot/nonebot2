import re
from typing import Any
from types import ModuleType
from datetime import datetime, timedelta

from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.rule import Rule, ArgumentParser
from nonebot.typing import T_State, T_Handler, T_RuleChecker, T_PermissionChecker

from .plugin import Plugin

def store_matcher(matcher: type[Matcher]) -> None: ...
def get_matcher_plugin(depth: int = ...) -> Plugin | None: ...
def get_matcher_module(depth: int = ...) -> ModuleType | None: ...
def on(
    type: str = "",
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    *,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_metaevent(
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    *,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_message(
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    *,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_notice(
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    *,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_request(
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    *,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_startswith(
    msg: str | tuple[str, ...],
    rule: Rule | T_RuleChecker | None = ...,
    ignorecase: bool = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_endswith(
    msg: str | tuple[str, ...],
    rule: Rule | T_RuleChecker | None = ...,
    ignorecase: bool = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_fullmatch(
    msg: str | tuple[str, ...],
    rule: Rule | T_RuleChecker | None = ...,
    ignorecase: bool = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_keyword(
    keywords: set[str],
    rule: Rule | T_RuleChecker | None = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_command(
    cmd: str | tuple[str, ...],
    rule: Rule | T_RuleChecker | None = ...,
    aliases: set[str | tuple[str, ...]] | None = ...,
    force_whitespace: str | bool | None = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_shell_command(
    cmd: str | tuple[str, ...],
    rule: Rule | T_RuleChecker | None = ...,
    aliases: set[str | tuple[str, ...]] | None = ...,
    parser: ArgumentParser | None = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_regex(
    pattern: str,
    flags: int | re.RegexFlag = ...,
    rule: Rule | T_RuleChecker | None = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...
def on_type(
    types: type[Event] | tuple[type[Event], ...],
    rule: Rule | T_RuleChecker | None = ...,
    *,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> type[Matcher]: ...

class _Group:
    matchers: list[type[Matcher]] = ...
    base_kwargs: dict[str, Any] = ...
    def _get_final_kwargs(
        self, update: dict[str, Any], *, exclude: set[str] | None = None
    ) -> dict[str, Any]: ...

class CommandGroup(_Group):
    basecmd: tuple[str, ...] = ...
    prefix_aliases: bool = ...
    def __init__(
        self,
        cmd: str | tuple[str, ...],
        prefix_aliases: bool = ...,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ): ...
    def command(
        self,
        cmd: str | tuple[str, ...],
        *,
        rule: Rule | T_RuleChecker | None = ...,
        aliases: set[str | tuple[str, ...]] | None = ...,
        force_whitespace: str | bool | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def shell_command(
        self,
        cmd: str | tuple[str, ...],
        *,
        rule: Rule | T_RuleChecker | None = ...,
        aliases: set[str | tuple[str, ...]] | None = ...,
        parser: ArgumentParser | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...

class MatcherGroup(_Group):
    def __init__(
        self,
        *,
        type: str = ...,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ): ...
    def on(
        self,
        *,
        type: str = ...,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_metaevent(
        self,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_message(
        self,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_notice(
        self,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_request(
        self,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_startswith(
        self,
        msg: str | tuple[str, ...],
        *,
        ignorecase: bool = ...,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_endswith(
        self,
        msg: str | tuple[str, ...],
        *,
        ignorecase: bool = ...,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_fullmatch(
        self,
        msg: str | tuple[str, ...],
        *,
        ignorecase: bool = ...,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_keyword(
        self,
        keywords: set[str],
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_command(
        self,
        cmd: str | tuple[str, ...],
        aliases: set[str | tuple[str, ...]] | None = ...,
        force_whitespace: str | bool | None = ...,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_shell_command(
        self,
        cmd: str | tuple[str, ...],
        aliases: set[str | tuple[str, ...]] | None = ...,
        parser: ArgumentParser | None = ...,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_regex(
        self,
        pattern: str,
        flags: int | re.RegexFlag = ...,
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
    def on_type(
        self,
        types: type[Event] | tuple[type[Event]],
        *,
        rule: Rule | T_RuleChecker | None = ...,
        permission: Permission | T_PermissionChecker | None = ...,
        handlers: list[T_Handler | Dependent] | None = ...,
        temp: bool = ...,
        expire_time: datetime | timedelta | None = ...,
        priority: int = ...,
        block: bool = ...,
        state: T_State | None = ...,
    ) -> type[Matcher]: ...
