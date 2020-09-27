#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from nonebot.typing import Rule, Matcher, Handler, Permission, RuleChecker, MatcherGroup
from nonebot.typing import Set, List, Dict, Type, Tuple, Union, Optional, ModuleType

plugins: Dict[str, "Plugin"] = ...

_tmp_matchers: Set[Type[Matcher]] = ...


class Plugin(object):
    name: str
    module: ModuleType
    matcher: Set[Type[Matcher]]


def on(rule: Optional[Union[Rule, RuleChecker]] = None,
       permission: Optional[Permission] = None,
       *,
       handlers: Optional[List[Handler]] = None,
       temp: bool = False,
       priority: int = 1,
       block: bool = False,
       state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_metaevent(rule: Optional[Union[Rule, RuleChecker]] = None,
                 *,
                 handlers: Optional[List[Handler]] = None,
                 temp: bool = False,
                 priority: int = 1,
                 block: bool = False,
                 state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_message(rule: Optional[Union[Rule, RuleChecker]] = None,
               permission: Optional[Permission] = None,
               *,
               handlers: Optional[List[Handler]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = True,
               state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_notice(rule: Optional[Union[Rule, RuleChecker]] = None,
              *,
              handlers: Optional[List[Handler]] = None,
              temp: bool = False,
              priority: int = 1,
              block: bool = False,
              state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_request(rule: Optional[Union[Rule, RuleChecker]] = None,
               *,
               handlers: Optional[List[Handler]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = False,
               state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_startswith(msg: str,
                  rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                  permission: Optional[Permission] = None,
                  *,
                  handlers: Optional[List[Handler]] = None,
                  temp: bool = False,
                  priority: int = 1,
                  block: bool = True,
                  state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                permission: Optional[Permission] = None,
                *,
                handlers: Optional[List[Handler]] = None,
                temp: bool = False,
                priority: int = 1,
                block: bool = True,
                state: Optional[dict] = None) -> Type[Matcher]:
    ...


def on_command(
        cmd: Union[str, Tuple[str, ...]],
        rule: Optional[Union[Rule, RuleChecker]] = None,
        aliases: Set[Union[str, Tuple[str, ...]]] = None,
        permission: Optional[Permission] = None,
        *,
        handlers: Optional[List[Handler]] = None,
        temp: bool = False,
        priority: int = 1,
        block: bool = True,
        state: Optional[dict] = None) -> Union[Type[Matcher], MatcherGroup]:
    ...


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = None,
             permission: Optional[Permission] = None,
             *,
             handlers: Optional[List[Handler]] = None,
             temp: bool = False,
             priority: int = 1,
             block: bool = True,
             state: Optional[dict] = None) -> Type[Matcher]:
    ...


def load_plugin(module_path: str) -> Optional[Plugin]:
    ...


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    ...


def load_builtin_plugins():
    ...


def get_loaded_plugins() -> Set[Plugin]:
    ...


class CommandGroup:

    def __init__(self,
                 cmd: Union[str, Tuple[str, ...]],
                 rule: Optional[Union[Rule, RuleChecker]] = None,
                 permission: Optional[Permission] = None,
                 *,
                 handlers: Optional[List[Handler]] = None,
                 temp: bool = False,
                 priority: int = 1,
                 block: bool = True,
                 state: Optional[dict] = None):
        ...

    def command(
            self,
            cmd: Union[str, Tuple[str, ...]],
            rule: Optional[Union[Rule, RuleChecker]] = None,
            aliases: Set[Union[str, Tuple[str, ...]]] = None,
            permission: Optional[Permission] = None,
            *,
            handlers: Optional[List[Handler]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = True,
            state: Optional[dict] = None) -> Union[Type[Matcher], MatcherGroup]:
        ...
