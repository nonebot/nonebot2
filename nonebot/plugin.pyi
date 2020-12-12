import re
from contextvars import ContextVar

from nonebot.typing import Rule, Matcher, Handler, Permission, RuleChecker
from nonebot.typing import Set, List, Dict, Type, Tuple, Union, Optional, ModuleType

plugins: Dict[str, "Plugin"] = ...

_tmp_matchers: ContextVar[Set[Type[Matcher]]] = ...
_export: ContextVar["Export"] = ...


class Export(dict):

    def __call__(self, func, **kwargs):
        ...

    def __setattr__(self, name, value):
        ...

    def __getattr__(self, name):
        ...


class Plugin(object):
    name: str
    module: ModuleType
    matcher: Set[Type[Matcher]]
    export: Export


def on(type: str = ...,
       rule: Optional[Union[Rule, RuleChecker]] = ...,
       permission: Optional[Permission] = ...,
       *,
       handlers: Optional[List[Handler]] = ...,
       temp: bool = ...,
       priority: int = ...,
       block: bool = ...,
       state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_metaevent(rule: Optional[Union[Rule, RuleChecker]] = ...,
                 *,
                 handlers: Optional[List[Handler]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_message(rule: Optional[Union[Rule, RuleChecker]] = ...,
               permission: Optional[Permission] = ...,
               *,
               handlers: Optional[List[Handler]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_notice(rule: Optional[Union[Rule, RuleChecker]] = ...,
              *,
              handlers: Optional[List[Handler]] = ...,
              temp: bool = ...,
              priority: int = ...,
              block: bool = ...,
              state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_request(rule: Optional[Union[Rule, RuleChecker]] = ...,
               *,
               handlers: Optional[List[Handler]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_startswith(msg: str,
                  rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
                  *,
                  permission: Optional[Permission] = ...,
                  handlers: Optional[List[Handler]] = ...,
                  temp: bool = ...,
                  priority: int = ...,
                  block: bool = ...,
                  state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
                *,
                permission: Optional[Permission] = ...,
                handlers: Optional[List[Handler]] = ...,
                temp: bool = ...,
                priority: int = ...,
                block: bool = ...,
                state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_keyword(keywords: Set[str],
               rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
               *,
               permission: Optional[Permission] = ...,
               handlers: Optional[List[Handler]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_command(cmd: Union[str, Tuple[str, ...]],
               rule: Optional[Union[Rule, RuleChecker]] = ...,
               aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
               *,
               permission: Optional[Permission] = ...,
               handlers: Optional[List[Handler]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Rule] = ...,
             *,
             permission: Optional[Permission] = ...,
             handlers: Optional[List[Handler]] = ...,
             temp: bool = ...,
             priority: int = ...,
             block: bool = ...,
             state: Optional[dict] = ...) -> Type[Matcher]:
    ...


def load_plugin(module_path: str) -> Optional[Plugin]:
    ...


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    ...


def load_builtin_plugins():
    ...


def get_plugin(name: str) -> Optional[Plugin]:
    ...


def get_loaded_plugins() -> Set[Plugin]:
    ...


def export() -> Export:
    ...


def require(name: str) -> Export:
    ...


class CommandGroup:

    def __init__(self,
                 cmd: Union[str, Tuple[str, ...]],
                 rule: Optional[Union[Rule, RuleChecker]] = ...,
                 permission: Optional[Permission] = ...,
                 *,
                 handlers: Optional[List[Handler]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[dict] = ...):
        ...

    def command(self,
                cmd: Union[str, Tuple[str, ...]],
                *,
                rule: Optional[Union[Rule, RuleChecker]] = ...,
                aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
                permission: Optional[Permission] = ...,
                handlers: Optional[List[Handler]] = ...,
                temp: bool = ...,
                priority: int = ...,
                block: bool = ...,
                state: Optional[dict] = ...) -> Type[Matcher]:
        ...


class MatcherGroup:

    def __init__(self,
                 *,
                 type: str = ...,
                 rule: Optional[Union[Rule, RuleChecker]] = ...,
                 permission: Optional[Permission] = ...,
                 handlers: Optional[List[Handler]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[dict] = ...):
        ...

    def on(self,
           *,
           type: str = ...,
           rule: Optional[Union[Rule, RuleChecker]] = ...,
           permission: Optional[Permission] = ...,
           handlers: Optional[List[Handler]] = ...,
           temp: bool = ...,
           priority: int = ...,
           block: bool = ...,
           state: Optional[dict] = ...) -> Type[Matcher]:
        ...

    def on_metaevent(self,
                     *,
                     rule: Optional[Union[Rule, RuleChecker]] = None,
                     handlers: Optional[List[Handler]] = None,
                     temp: bool = False,
                     priority: int = 1,
                     block: bool = False,
                     state: Optional[dict] = None) -> Type[Matcher]:
        ...

    def on_message(self,
                   *,
                   rule: Optional[Union[Rule, RuleChecker]] = None,
                   permission: Optional[Permission] = None,
                   handlers: Optional[List[Handler]] = None,
                   temp: bool = False,
                   priority: int = 1,
                   block: bool = True,
                   state: Optional[dict] = None) -> Type[Matcher]:
        ...

    def on_notice(self,
                  *,
                  rule: Optional[Union[Rule, RuleChecker]] = None,
                  handlers: Optional[List[Handler]] = None,
                  temp: bool = False,
                  priority: int = 1,
                  block: bool = False,
                  state: Optional[dict] = None) -> Type[Matcher]:
        ...

    def on_request(self,
                   *,
                   rule: Optional[Union[Rule, RuleChecker]] = None,
                   handlers: Optional[List[Handler]] = None,
                   temp: bool = False,
                   priority: int = 1,
                   block: bool = False,
                   state: Optional[dict] = None) -> Type[Matcher]:
        ...

    def on_startswith(self,
                      *,
                      msg: str,
                      rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
                      permission: Optional[Permission] = ...,
                      handlers: Optional[List[Handler]] = ...,
                      temp: bool = ...,
                      priority: int = ...,
                      block: bool = ...,
                      state: Optional[dict] = ...) -> Type[Matcher]:
        ...

    def on_endswith(self,
                    *,
                    msg: str,
                    rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
                    permission: Optional[Permission] = ...,
                    handlers: Optional[List[Handler]] = ...,
                    temp: bool = ...,
                    priority: int = ...,
                    block: bool = ...,
                    state: Optional[dict] = ...) -> Type[Matcher]:
        ...

    def on_keyword(self,
                   *,
                   keywords: Set[str],
                   rule: Optional[Optional[Union[Rule, RuleChecker]]] = ...,
                   permission: Optional[Permission] = ...,
                   handlers: Optional[List[Handler]] = ...,
                   temp: bool = ...,
                   priority: int = ...,
                   block: bool = ...,
                   state: Optional[dict] = ...) -> Type[Matcher]:
        ...

    def on_command(self,
                   *,
                   cmd: Union[str, Tuple[str, ...]],
                   rule: Optional[Union[Rule, RuleChecker]] = ...,
                   aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
                   permission: Optional[Permission] = ...,
                   handlers: Optional[List[Handler]] = ...,
                   temp: bool = ...,
                   priority: int = ...,
                   block: bool = ...,
                   state: Optional[dict] = ...) -> Type[Matcher]:
        ...

    def on_regex(self,
                 *,
                 pattern: str,
                 flags: Union[int, re.RegexFlag] = 0,
                 rule: Optional[Rule] = ...,
                 permission: Optional[Permission] = ...,
                 handlers: Optional[List[Handler]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[dict] = ...) -> Type[Matcher]:
        ...
