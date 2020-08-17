#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pkgutil
import importlib
from importlib.util import module_from_spec

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.rule import Rule, startswith, endswith, command, regex
from nonebot.permission import Permission, METAEVENT, MESSAGE, NOTICE, REQUEST
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


def on_metaevent(rule: Union[Rule, RuleChecker] = Rule(),
                 *,
                 handlers=[],
                 temp=False,
                 priority: int = 1,
                 state={}) -> Type[Matcher]:
    matcher = Matcher.new(Rule() & rule,
                          METAEVENT,
                          temp=temp,
                          priority=priority,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_message(rule: Union[Rule, RuleChecker] = Rule(),
               permission: Permission = MESSAGE,
               *,
               handlers=[],
               temp=False,
               priority: int = 1,
               state={}) -> Type[Matcher]:
    matcher = Matcher.new(Rule() & rule,
                          permission,
                          temp=temp,
                          priority=priority,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_notice(rule: Union[Rule, RuleChecker] = Rule(),
              *,
              handlers=[],
              temp=False,
              priority: int = 1,
              state={}) -> Type[Matcher]:
    matcher = Matcher.new(Rule() & rule,
                          NOTICE,
                          temp=temp,
                          priority=priority,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_request(rule: Union[Rule, RuleChecker] = Rule(),
               *,
               handlers=[],
               temp=False,
               priority: int = 1,
               state={}) -> Type[Matcher]:
    matcher = Matcher.new(Rule() & rule,
                          REQUEST,
                          temp=temp,
                          priority=priority,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_startswith(msg: str,
                  rule: Optional[Union[Rule, RuleChecker]] = None,
                  permission: Permission = MESSAGE,
                  **kwargs) -> Type[Matcher]:
    return on_message(startswith(msg) &
                      rule, permission, **kwargs) if rule else on_message(
                          startswith(msg), permission, **kwargs)


def on_endswith(msg: str,
                rule: Optional[Union[Rule, RuleChecker]] = None,
                permission: Permission = MESSAGE,
                **kwargs) -> Type[Matcher]:
    return on_message(endswith(msg) &
                      rule, permission, **kwargs) if rule else on_message(
                          startswith(msg), permission, **kwargs)


def on_command(cmd: Tuple[str],
               rule: Optional[Union[Rule, RuleChecker]] = None,
               permission: Permission = MESSAGE,
               **kwargs) -> Type[Matcher]:
    return on_message(command(cmd) &
                      rule, permission, **kwargs) if rule else on_message(
                          command(cmd), permission, **kwargs)


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = None,
             **kwargs) -> Type[Matcher]:
    return on_message(regex(pattern, flags) &
                      rule, **kwargs) if rule else on_message(
                          regex(pattern, flags), **kwargs)


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

        try:
            spec = module_info.module_finder.find_spec(name)
            module = module_from_spec(spec)

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
