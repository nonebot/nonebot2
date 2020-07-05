#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import importlib
from types import ModuleType
from typing import Set, Dict, Type, Optional

from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.matcher import Matcher

plugins: Dict[str, "Plugin"] = {}

_tmp_matchers: Set[Type[Matcher]] = set()


class Plugin(object):

    # TODO: store plugin informations
    def __init__(self, module_path: str, module: ModuleType,
                 matchers: Set[Type[Matcher]]):
        self.module_path = module_path
        self.module = module
        self.matchers = matchers


def on_message(rule: Rule,
               *,
               handlers=[],
               temp=False,
               priority: int = 1,
               state={}) -> Type[Matcher]:
    matcher = Matcher.new(rule,
                          temp=temp,
                          priority=priority,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


# def on_startswith(msg,
#                   start: int = None,
#                   end: int = None,
#                   rule: Optional[Rule] = None,
#                   **kwargs) -> Type[Matcher]:
#     return on_message(startswith(msg, start, end) &
#                       rule, **kwargs) if rule else on_message(
#                           startswith(msg, start, end), **kwargs)

# def on_regex(pattern,
#              flags: Union[int, re.RegexFlag] = 0,
#              rule: Optional[Rule] = None,
#              **kwargs) -> Type[Matcher]:
#     return on_message(regex(pattern, flags) &
#                       rule, **kwargs) if rule else on_message(
#                           regex(pattern, flags), **kwargs)


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


def load_plugins(plugin_dir: str) -> Set[Plugin]:
    plugins = set()
    for name in os.listdir(plugin_dir):
        path = os.path.join(plugin_dir, name)
        if os.path.isfile(path) and \
                (name.startswith("_") or not name.endswith(".py")):
            continue
        if os.path.isdir(path) and \
                (name.startswith("_") or not os.path.exists(
                    os.path.join(path, "__init__.py"))):
            continue

        m = re.match(r"([_A-Z0-9a-z]+)(.py)?", name)
        if not m:
            continue

        result = load_plugin(f"{plugin_dir.replace(os.sep, '.')}.{m.group(1)}")
        if result:
            plugins.add(result)
    return plugins


def get_loaded_plugins() -> Set[Plugin]:
    return set(plugins.values())
