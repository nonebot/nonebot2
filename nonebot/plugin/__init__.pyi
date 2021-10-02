import re
from types import ModuleType
from dataclasses import dataclass
from typing import Set, Dict, List, Type, Tuple, Union, Optional

from nonebot.handler import Handler
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.rule import Rule, ArgumentParser
from nonebot.typing import T_State, T_Handler, T_RuleChecker, T_StateFactory

from .export import Export
from .export import export as export

plugins: Dict[str, "Plugin"] = ...
PLUGIN_NAMESPACE: str = ...


@dataclass(eq=False)
class Plugin(object):
    name: str
    module: ModuleType

    @property
    def export(self) -> Export:
        ...

    @property
    def matcher(self) -> Set[Type[Matcher]]:
        ...


def on(type: str = "",
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
        msg: Union[str, Tuple[str, ...]],
        rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
        ignorecase: bool = ...,
        *,
        permission: Optional[Permission] = ...,
        handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
        temp: bool = ...,
        priority: int = ...,
        block: bool = ...,
        state: Optional[T_State] = ...,
        state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_endswith(msg: Union[str, Tuple[str, ...]],
                rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = ...,
                ignorecase: bool = ...,
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


def on_shell_command(
        cmd: Union[str, Tuple[str, ...]],
        rule: Optional[Union[Rule, T_RuleChecker]] = ...,
        aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = ...,
        parser: Optional[ArgumentParser] = ...,
        *,
        permission: Optional[Permission] = ...,
        handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
        temp: bool = ...,
        priority: int = ...,
        block: bool = ...,
        state: Optional[T_State] = ...,
        state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
    ...


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = ...,
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


class CommandGroup:

    def __init__(self,
                 cmd: Union[str, Tuple[str, ...]],
                 *,
                 rule: Optional[Union[Rule, T_RuleChecker]] = ...,
                 permission: Optional[Permission] = ...,
                 handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
                 temp: bool = ...,
                 priority: int = ...,
                 block: bool = ...,
                 state: Optional[T_State] = ...,
                 state_factory: Optional[T_StateFactory] = ...):
        ...

    def command(self,
                cmd: Union[str, Tuple[str, ...]],
                *,
                aliases: Optional[Set[Union[str, Tuple[str, ...]]]],
                rule: Optional[Union[Rule, T_RuleChecker]] = ...,
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
            aliases: Optional[Set[Union[str, Tuple[str, ...]]]],
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
                 state: Optional[T_State] = ...,
                 state_factory: Optional[T_StateFactory] = ...):
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
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_message(
            self,
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

    def on_notice(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_request(
            self,
            *,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
            handlers: Optional[List[Union[T_Handler, Handler]]] = ...,
            temp: bool = ...,
            priority: int = ...,
            block: bool = ...,
            state: Optional[T_State] = ...,
            state_factory: Optional[T_StateFactory] = ...) -> Type[Matcher]:
        ...

    def on_startswith(
            self,
            msg: Union[str, Tuple[str, ...]],
            *,
            ignorecase: bool = ...,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
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
            msg: Union[str, Tuple[str, ...]],
            *,
            ignorecase: bool = ...,
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
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
            rule: Optional[Union[Rule, T_RuleChecker]] = ...,
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
            flags: Union[int, re.RegexFlag] = ...,
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


def load_builtin_plugins(name: str = ...) -> Optional[Plugin]:
    ...


def get_plugin(name: str) -> Optional[Plugin]:
    ...


def get_loaded_plugins() -> Set[Plugin]:
    ...


def require(name: str) -> Optional[Export]:
    ...
