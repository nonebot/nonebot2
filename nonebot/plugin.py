#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import pkgutil
import importlib
from importlib._bootstrap import _load

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.rule import Rule, startswith, endswith, command, regex
from nonebot.typing import Set, Dict, Type, Tuple, Union, Optional, ModuleType, RuleChecker

plugins: Dict[str, "Plugin"] = {}

_tmp_matchers: Set[Type[Matcher]] = set()


class Plugin(object):

    # TODO: store plugin informations
    def __init__(self, module_path: str, module: ModuleType,
                 matchers: Set[Type[Matcher]]):
        self.module_path = module_path
        self.module = module
        self.matchers = matchers


def on(rule: Union[Rule, RuleChecker] = Rule(),
       permission: Permission = Permission(),
       *,
       handlers=[],
       temp=False,
       priority: int = 1,
       block: bool = False,
       state={}) -> Type[Matcher]:
    matcher = Matcher.new("",
                          Rule() & rule,
                          permission,
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_metaevent(rule: Union[Rule, RuleChecker] = Rule(),
                 *,
                 handlers=[],
                 temp=False,
                 priority: int = 1,
                 block: bool = False,
                 state={}) -> Type[Matcher]:
    matcher = Matcher.new("meta_event",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_message(rule: Union[Rule, RuleChecker] = Rule(),
               permission: Permission = Permission(),
               *,
               handlers=[],
               temp=False,
               priority: int = 1,
               block: bool = True,
               state={}) -> Type[Matcher]:
    matcher = Matcher.new("message",
                          Rule() & rule,
                          permission,
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_notice(rule: Union[Rule, RuleChecker] = Rule(),
              *,
              handlers=[],
              temp=False,
              priority: int = 1,
              block: bool = False,
              state={}) -> Type[Matcher]:
    matcher = Matcher.new("notice",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_request(rule: Union[Rule, RuleChecker] = Rule(),
               *,
               handlers=[],
               temp=False,
               priority: int = 1,
               block: bool = False,
               state={}) -> Type[Matcher]:
    matcher = Matcher.new("request",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_startswith(msg: str,
                  rule: Optional[Union[Rule, RuleChecker]] = None,
                  permission: Permission = Permission(),
                  **kwargs) -> Type[Matcher]:
    return on_message(startswith(msg) &
                      rule, permission, **kwargs) if rule else on_message(
                          startswith(msg), permission, **kwargs)


def on_endswith(msg: str,
                rule: Optional[Union[Rule, RuleChecker]] = None,
                permission: Permission = Permission(),
                **kwargs) -> Type[Matcher]:
    return on_message(endswith(msg) &
                      rule, permission, **kwargs) if rule else on_message(
                          startswith(msg), permission, **kwargs)


def on_command(cmd: Union[str, Tuple[str]],
               rule: Optional[Union[Rule, RuleChecker]] = None,
               permission: Permission = Permission(),
               **kwargs) -> Type[Matcher]:
    if isinstance(cmd, str):
        cmd = (cmd,)
    return on_message(command(cmd) &
                      rule, permission, **kwargs) if rule else on_message(
                          command(cmd), permission, **kwargs)


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = None,
             permission: Permission = Permission(),
             **kwargs) -> Type[Matcher]:
    return on_message(regex(pattern, flags) &
                      rule, permission, **kwargs) if rule else on_message(
                          regex(pattern, flags), permission, **kwargs)


def load_plugin(module_path: str) -> Optional[Plugin]:
    try:
        _tmp_matchers.clear()
        module = importlib.import_module(module_path)
        plugin = Plugin(module_path, module, _tmp_matchers.copy())
        plugins[module_path] = plugin
        logger.info(f"Succeeded to import \"{module_path}\"")
        return plugin
    except Exception as e:
        logger.error(f"Failed to import \"{module_path}\", error: {e}")
        logger.exception(e)
        return None


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    loaded_plugins = set()
    for module_info in pkgutil.iter_modules(plugin_dir):
        _tmp_matchers.clear()
        name = module_info.name
        if name.startswith("_"):
            continue

        spec = module_info.module_finder.find_spec(name)
        if spec.name in sys.modules:
            continue

        try:
            module = _load(spec)

            plugin = Plugin(name, module, _tmp_matchers.copy())
            plugins[name] = plugin
            loaded_plugins.add(plugin)
            logger.info(f"Succeeded to import \"{name}\"")
        except Exception as e:
            logger.error(f"Failed to import \"{name}\", error: {e}")
            logger.exception(e)
    return loaded_plugins


def get_loaded_plugins() -> Set[Plugin]:
    return set(plugins.values())
