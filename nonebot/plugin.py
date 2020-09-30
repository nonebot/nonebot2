#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import pkgutil
import importlib
from dataclasses import dataclass
from importlib._bootstrap import _load

from nonebot.log import logger
from nonebot.permission import Permission
from nonebot.typing import Handler, RuleChecker
from nonebot.matcher import Matcher, MatcherGroup
from nonebot.rule import Rule, startswith, endswith, command, regex
from nonebot.typing import Set, List, Dict, Type, Tuple, Union, Optional, ModuleType

plugins: Dict[str, "Plugin"] = {}

_tmp_matchers: Set[Type[Matcher]] = set()


@dataclass(eq=False)
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
    matcher = Matcher.new("",
                          Rule() & rule,
                          permission or Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_metaevent(rule: Optional[Union[Rule, RuleChecker]] = None,
                 *,
                 handlers: Optional[List[Handler]] = None,
                 temp: bool = False,
                 priority: int = 1,
                 block: bool = False,
                 state: Optional[dict] = None) -> Type[Matcher]:
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


def on_message(rule: Optional[Union[Rule, RuleChecker]] = None,
               permission: Optional[Permission] = None,
               *,
               handlers: Optional[List[Handler]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = True,
               state: Optional[dict] = None) -> Type[Matcher]:
    matcher = Matcher.new("message",
                          Rule() & rule,
                          permission or Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_notice(rule: Optional[Union[Rule, RuleChecker]] = None,
              *,
              handlers: Optional[List[Handler]] = None,
              temp: bool = False,
              priority: int = 1,
              block: bool = False,
              state: Optional[dict] = None) -> Type[Matcher]:
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


def on_request(rule: Optional[Union[Rule, RuleChecker]] = None,
               *,
               handlers: Optional[List[Handler]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = False,
               state: Optional[dict] = None) -> Type[Matcher]:
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
                  rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                  **kwargs) -> Type[Matcher]:
    return on_message(startswith(msg) & rule, **kwargs) if rule else on_message(
        startswith(msg), **kwargs)


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                **kwargs) -> Type[Matcher]:
    return on_message(endswith(msg) & rule, **kwargs) if rule else on_message(
        startswith(msg), **kwargs)


def on_command(cmd: Union[str, Tuple[str, ...]],
               rule: Optional[Union[Rule, RuleChecker]] = None,
               aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
               **kwargs) -> Union[Type[Matcher], MatcherGroup]:
    if isinstance(cmd, str):
        cmd = (cmd,)

    async def _strip_cmd(bot, event, state: dict):
        message = event.message
        event.message = message.__class__(
            str(message)[len(state["_prefix"]["raw_command"]):].strip())

    handlers = kwargs.pop("handlers", [])
    handlers.insert(0, _strip_cmd)

    if aliases:
        aliases = set(map(lambda x: (x,) if isinstance(x, str) else x, aliases))
        group = MatcherGroup("message",
                             Rule() & rule,
                             handlers=handlers,
                             **kwargs)
        for cmd_ in [cmd, *aliases]:
            _tmp_matchers.add(group.new(rule=command(cmd_)))
        return group
    else:
        return on_message(command(cmd) & rule, handlers=handlers, **
                          kwargs) if rule else on_message(
                              command(cmd), handlers=handlers, **kwargs)


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
        if module_path in plugins:
            return plugins[module_path]
        elif module_path in sys.modules:
            logger.warning(
                f"Module {module_path} has been loaded by other plugins! Ignored"
            )
            return
        module = importlib.import_module(module_path)
        for m in _tmp_matchers:
            m.module = module_path
        plugin = Plugin(module_path, module, _tmp_matchers.copy())
        plugins[module_path] = plugin
        logger.opt(
            colors=True).info(f'Succeeded to import "<y>{module_path}</y>"')
        return plugin
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f'<r><bg #f8bbd0>Failed to import "{module_path}"</bg #f8bbd0></r>')
        return None


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    loaded_plugins = set()
    for module_info in pkgutil.iter_modules(plugin_dir):
        _tmp_matchers.clear()
        name = module_info.name
        if name.startswith("_"):
            continue

        spec = module_info.module_finder.find_spec(name)
        if spec.name in plugins:
            continue
        elif spec.name in sys.modules:
            logger.warning(
                f"Module {spec.name} has been loaded by other plugin! Ignored")
            continue

        try:
            module = _load(spec)

            for m in _tmp_matchers:
                m.module = name
            plugin = Plugin(name, module, _tmp_matchers.copy())
            plugins[name] = plugin
            loaded_plugins.add(plugin)
            logger.opt(colors=True).info(f'Succeeded to import "<y>{name}</y>"')
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f'<r><bg #f8bbd0>Failed to import "{name}"</bg #f8bbd0></r>')
    return loaded_plugins


def load_builtin_plugins():
    return load_plugin("nonebot.plugins.base")


def get_loaded_plugins() -> Set[Plugin]:
    return set(plugins.values())


class CommandGroup:

    def __init__(self, cmd: Union[str, Tuple[str, ...]], **kwargs):
        self.basecmd = (cmd,) if isinstance(cmd, str) else cmd
        if "aliases" in kwargs:
            del kwargs["aliases"]
        self.base_kwargs = kwargs

    def command(self, cmd: Union[str, Tuple[str, ...]],
                **kwargs) -> Union[Type[Matcher], MatcherGroup]:
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        cmd = self.basecmd + sub_cmd

        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        return on_command(cmd, **final_kwargs)
