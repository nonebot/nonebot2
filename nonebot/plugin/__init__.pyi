import re
from types import ModuleType
from contextvars import ContextVar
from typing import Any, Set, List, Dict, Type, Tuple, Union, Optional

from nonebot.matcher import Matcher
from nonebot.handler import Handler
from nonebot.permission import Permission
from nonebot.rule import Rule, ArgumentParser
from nonebot.typing import T_State, T_StateFactory, T_Handler, T_RuleChecker

plugins: Dict[str, "Plugin"] = ...

_export: ContextVar["Export"] = ...
_tmp_matchers: ContextVar[Set[Type[Matcher]]] = ...


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
       rule: Optional[Union[Rule, T_RuleChecker]] = ...,
       permission: Optional[Permission] = ...,
       *,
       handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
       temp: bool = ...,
       priority: int = ...,
       block: bool = ...,
       state: Optional[T_State] = ...,
       state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_metaevent(
        rule: Optional[Union[Rule, T_RuleChecker]] = ...,
        *,
        handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
        temp: bool = ...,
        priority: int = ...,
        block: bool = ...,
        state: Optional[T_State] = ...,
        state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_message(rule: Optional[Union[Rule, T_RuleChecker]] = ...,
               permission: Optional[Permission] = ...,
               *,
               handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[T_State] = ...,
               state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_notice(rule: Optional[Union[Rule, T_RuleChecker]] = ...,
              *,
              handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
              temp: bool = ...,
              priority: int = ...,
              block: bool = ...,
              state: Optional[T_State] = ...,
              state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_request(rule: Optional[Union[Rule, T_RuleChecker]] = ...,
               *,
               handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[T_State] = ...,
               state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_startswith(
        msg: str,
        rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
        *,
        permission: Optional[Permission] = ...,
        handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
        temp: bool = ...,
        priority: int = ...,
        block: bool = ...,
        state: Optional[T_State] = ...,
        state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
                *,
                permission: Optional[Permission] = ...,
                handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
                temp: bool = ...,
                priority: int = ...,
                block: bool = ...,
                state: Optional[T_State] = ...,
                state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_keyword(keywords: Set[str],
               rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
               *,
               permission: Optional[Permission] = ...,
               handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[T_State] = ...,
               state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_command(cmd: Union[str, Tuple[str, ...]],
               rule: Optional[Union[Rule, T_RuleChecker]] = ...,
               aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
               *,
               permission: Optional[Permission] = ...,
               handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
               temp: bool = ...,
               priority: int = ...,
               block: bool = ...,
               state: Optional[T_State] = ...,
               state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_shell_command(cmd: Union[str, Tuple[str, ...]],
                     rule: Optional[Union[Rule, T_RuleChecker]] = None,
                     aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
                     parser: Optional[ArgumentParser] = None,
                     **kwargs) -> Type[Matcher]:
    ...


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Union[Rule, T_RuleChecker]] = ...,
             *,
             permission: Optional[Permission] = ...,
             handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
             temp: bool = ...,
             priority: int = ...,
             block: bool = ...,
             state: Optional[T_State] = ...,
             state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def load_plugin(module_path: str) -> Optional[Plugin]:
    ...


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    ...


def load_all_plugins(module_path: Set[str],
                     plugin_dir: Set[str]) -> Set[Plugin]:
    ...


def load_from_json(file_path: str, encoding: str = ...) -> Set[Plugin]:
    ...


def load_from_toml(file_path: str, encoding: str = ...) -> Set[Plugin]:
    ...


def load_builtin_plugins(name: str = ...):
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
                 rule: Optional[Union[Rule, T_RuleChecker]] = ...,
                 permission: Optional[Permission] = ...,
                 *,
                 handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[T_State] = ...):
        self.basecmd: Tuple[str, ...] = ...
        self.base_kwargs: Dict[str, Any] = ...

    def command(self,
                cmd: Union[str, Tuple[str, ...]],
                *,
                rule: Optional[Union[Rule, T_RuleChecker]] = ...,
                aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
                permission: Optional[Permission] = ...,
                handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
                temp: bool = ...,
                priority: int = ...,
                block: bool = ...,
                state: Optional[T_State] = ...,
                state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def shell_command(
            self,
            cmd: Union[str, Tuple[str, ...]],
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
            parser: Optional[ArgumentParser] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...


class MatcherGroup:

    def __init__(self,
                 *,
                 type: str = ...,
                 rule: Optional[Union[Rule, T_RuleChecker]] = ...,
                 permission: Optional[Permission] = ...,
                 handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[T_State] = ...):
        ...

    def on(self,
           *,
           type: str = ...,
           rule: Optional[Union[Rule, T_RuleChecker]] = ...,
           permission: Optional[Permission] = ...,
           handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
           temp: bool = ...,
           priority: int = ...,
           block: bool = ...,
           state: Optional[T_State] = ...,
           state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_metaevent(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = None,
            handlers: Optional[List[Union[T_Handler, Handler]]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            state: Optional[T_State] = None,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_message(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = None,
            permission: Optional[Permission] = None,
            handlers: Optional[List[Union[T_Handler, Handler]]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = True,
            state: Optional[T_State] = None,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_notice(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = None,
            handlers: Optional[List[Union[T_Handler, Handler]]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            state: Optional[T_State] = None,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_request(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = None,
            handlers: Optional[List[Union[T_Handler, Handler]]] = None,
            temp: bool = False,
            priority: int = 1,
            block: bool = False,
            state: Optional[T_State] = None,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_startswith(
            self,
            msg: str,
            *,
            rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_endswith(
            self,
            msg: str,
            *,
            rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_keyword(
            self,
            keywords: Set[str],
            *,
            rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_command(
            self,
            cmd: Union[str, Tuple[str, ...]],
            aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_shell_command(
            self,
            cmd: Union[str, Tuple[str, ...]],
            aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
            parser: Optional[ArgumentParser] = ...,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_regex(
            self,
            pattern: str,
            flags: Union[int, re.RegexFlag] = 0,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            permission: Optional[Permission] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...
