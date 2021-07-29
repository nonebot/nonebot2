"""
插件
====

为 NoneBot 插件开发提供便携的定义函数。
"""
import re
import json
from types import ModuleType
from dataclasses import dataclass
from collections import defaultdict
from contextvars import Context, copy_context
from typing import Any, Set, List, Dict, Type, Tuple, Union, Optional, TYPE_CHECKING

import tomlkit
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.handler import Handler
from nonebot.permission import Permission
from nonebot.typing import T_State, T_StateFactory, T_Handler, T_RuleChecker
from nonebot.rule import Rule, startswith, endswith, keyword, command, shell_command, ArgumentParser, regex

from .export import Export, export, _export
from .manager import PluginManager, _current_plugin

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event

plugins: Dict[str, "Plugin"] = {}
"""
:类型: ``Dict[str, Plugin]``
:说明: 已加载的插件
"""
PLUGIN_NAMESPACE = "nonebot.loaded_plugins"

_plugin_matchers: Dict[str, Set[Type[Matcher]]] = defaultdict(set)


@dataclass(eq=False)
class Plugin(object):
    """存储插件信息"""
    name: str
    """
    - **类型**: ``str``
    - **说明**: 插件名称，使用 文件/文件夹 名称作为插件名
    """
    module: ModuleType
    """
    - **类型**: ``ModuleType``
    - **说明**: 插件模块对象
    """

    @property
    def export(self) -> Export:
        """
        - **类型**: ``Export``
        - **说明**: 插件内定义的导出内容
        """
        return getattr(self.module, "__export__", Export())

    @property
    def matcher(self) -> Set[Type[Matcher]]:
        """
        - **类型**: ``Set[Type[Matcher]]``
        - **说明**: 插件内定义的 ``Matcher``
        """
        # return reduce(
        #     lambda x, y: x | _plugin_matchers[y],
        #     filter(lambda x: x.startswith(self.name), _plugin_matchers.keys()),
        #     set())
        return _plugin_matchers.get(self.name, set())


def _store_matcher(matcher: Type[Matcher]):
    if matcher.plugin_name:
        _plugin_matchers[matcher.plugin_name].add(matcher)


def on(type: str = "",
       rule: Optional[Union[Rule, T_RuleChecker]] = None,
       permission: Optional[Permission] = None,
       *,
       handlers: Optional[List[Union[T_Handler, Handler]]] = None,
       temp: bool = False,
       priority: int = 1,
       block: bool = False,
       state: Optional[T_State] = None,
       state_factory: Optional[T_StateFactory] = None) -> Type[Matcher]:
    """
    :说明:

      注册一个基础事件响应器，可自定义类型。

    :参数:

      * ``type: str``: 事件响应器类型
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(type,
                          Rule() & rule,
                          permission or Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          module=_current_plugin.get(),
                          default_state=state,
                          default_state_factory=state_factory)
    _store_matcher(matcher)
    return matcher


def on_metaevent(
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        *,
        handlers: Optional[List[Union[T_Handler, Handler]]] = None,
        temp: bool = False,
        priority: int = 1,
        block: bool = False,
        state: Optional[T_State] = None,
        state_factory: Optional[T_StateFactory] = None) -> Type[Matcher]:
    """
    :说明:

      注册一个元事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new("meta_event",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          module=_current_plugin.get(),
                          default_state=state,
                          default_state_factory=state_factory)
    _store_matcher(matcher)
    return matcher


def on_message(rule: Optional[Union[Rule, T_RuleChecker]] = None,
               permission: Optional[Permission] = None,
               *,
               handlers: Optional[List[Union[T_Handler, Handler]]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = True,
               state: Optional[T_State] = None,
               state_factory: Optional[T_StateFactory] = None) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new("message",
                          Rule() & rule,
                          permission or Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          module=_current_plugin.get(),
                          default_state=state,
                          default_state_factory=state_factory)
    _store_matcher(matcher)
    return matcher


def on_notice(rule: Optional[Union[Rule, T_RuleChecker]] = None,
              *,
              handlers: Optional[List[Union[T_Handler, Handler]]] = None,
              temp: bool = False,
              priority: int = 1,
              block: bool = False,
              state: Optional[T_State] = None,
              state_factory: Optional[T_StateFactory] = None) -> Type[Matcher]:
    """
    :说明:

      注册一个通知事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new("notice",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          module=_current_plugin.get(),
                          default_state=state,
                          default_state_factory=state_factory)
    _store_matcher(matcher)
    return matcher


def on_request(rule: Optional[Union[Rule, T_RuleChecker]] = None,
               *,
               handlers: Optional[List[Union[T_Handler, Handler]]] = None,
               temp: bool = False,
               priority: int = 1,
               block: bool = False,
               state: Optional[T_State] = None,
               state_factory: Optional[T_StateFactory] = None) -> Type[Matcher]:
    """
    :说明:

      注册一个请求事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new("request",
                          Rule() & rule,
                          Permission(),
                          temp=temp,
                          priority=priority,
                          block=block,
                          handlers=handlers,
                          module=_current_plugin.get(),
                          default_state=state,
                          default_state_factory=state_factory)
    _store_matcher(matcher)
    return matcher


def on_startswith(msg: Union[str, Tuple[str, ...]],
                  rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
                  ignorecase: bool = False,
                  **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

    :参数:

      * ``msg: Union[str, Tuple[str, ...]]``: 指定消息开头内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``ignorecase: bool``: 是否忽略大小写
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(startswith(msg, ignorecase) & rule, **kwargs)


def on_endswith(msg: Union[str, Tuple[str, ...]],
                rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
                ignorecase: bool = False,
                **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

    :参数:

      * ``msg: Union[str, Tuple[str, ...]]``: 指定消息结尾内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``ignorecase: bool``: 是否忽略大小写
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(endswith(msg, ignorecase) & rule, **kwargs)


def on_keyword(keywords: Set[str],
               rule: Optional[Union[Rule, T_RuleChecker]] = None,
               **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

    :参数:

      * ``keywords: Set[str]``: 关键词列表
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(keyword(*keywords) & rule, **kwargs)


def on_command(cmd: Union[str, Tuple[str, ...]],
               rule: Optional[Union[Rule, T_RuleChecker]] = None,
               aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
               **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息以指定命令开头时响应。

      命令匹配规则参考: `命令形式匹配 <rule.html#command-command>`_

    :参数:

      * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """

    async def _strip_cmd(bot: "Bot", event: "Event", state: T_State):
        message = event.get_message()
        segment = message.pop(0)
        new_message = message.__class__(
            str(segment).lstrip()
            [len(state["_prefix"]["raw_command"]):].lstrip())  # type: ignore
        for new_segment in reversed(new_message):
            message.insert(0, new_segment)

    handlers = kwargs.pop("handlers", [])
    handlers.insert(0, _strip_cmd)

    commands = set([cmd]) | (aliases or set())
    return on_message(command(*commands) & rule, handlers=handlers, **kwargs)


def on_shell_command(cmd: Union[str, Tuple[str, ...]],
                     rule: Optional[Union[Rule, T_RuleChecker]] = None,
                     aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
                     parser: Optional[ArgumentParser] = None,
                     **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个支持 ``shell_like`` 解析参数的命令消息事件响应器。

      与普通的 ``on_command`` 不同的是，在添加 ``parser`` 参数时, 响应器会自动处理消息。

      并将用户输入的原始参数列表保存在 ``state["argv"]``, ``parser`` 处理的参数保存在 ``state["args"]`` 中

    :参数:

      * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
      * ``parser: Optional[ArgumentParser]``: ``nonebot.rule.ArgumentParser`` 对象
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """

    async def _strip_cmd(bot: "Bot", event: "Event", state: T_State):
        message = event.get_message()
        segment = message.pop(0)
        new_message = message.__class__(
            str(segment)
            [len(state["_prefix"]["raw_command"]):].strip())  # type: ignore
        for new_segment in reversed(new_message):
            message.insert(0, new_segment)

    handlers = kwargs.pop("handlers", [])
    handlers.insert(0, _strip_cmd)

    commands = set([cmd]) | (aliases or set())
    return on_message(shell_command(*commands, parser=parser) & rule,
                      handlers=handlers,
                      **kwargs)


def on_regex(pattern: str,
             flags: Union[int, re.RegexFlag] = 0,
             rule: Optional[Union[Rule, T_RuleChecker]] = None,
             **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

      命令匹配规则参考: `正则匹配 <rule.html#regex-regex-flags-0>`_

    :参数:

      * ``pattern: str``: 正则表达式
      * ``flags: Union[int, re.RegexFlag]``: 正则匹配标志
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(regex(pattern, flags) & rule, **kwargs)


class CommandGroup:
    """命令组，用于声明一组有相同名称前缀的命令。"""

    def __init__(self, cmd: Union[str, Tuple[str, ...]], **kwargs):
        """
        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 命令前缀
          * ``**kwargs``: 其他传递给 ``on_command`` 的参数默认值，参考 `on_command <#on-command-cmd-rule-none-aliases-none-kwargs>`_
        """
        self.basecmd: Tuple[str, ...] = (cmd,) if isinstance(cmd, str) else cmd
        """
        - **类型**: ``Tuple[str, ...]``
        - **说明**: 命令前缀
        """
        if "aliases" in kwargs:
            del kwargs["aliases"]
        self.base_kwargs: Dict[str, Any] = kwargs
        """
        - **类型**: ``Dict[str, Any]``
        - **说明**: 其他传递给 ``on_command`` 的参数默认值
        """

    def command(self, cmd: Union[str, Tuple[str, ...]],
                **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个新的命令。

        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 命令前缀
          * ``**kwargs``: 其他传递给 ``on_command`` 的参数，将会覆盖命令组默认值

        :返回:

          - ``Type[Matcher]``
        """
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        cmd = self.basecmd + sub_cmd

        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        return on_command(cmd, **final_kwargs)

    def shell_command(self, cmd: Union[str, Tuple[str, ...]],
                      **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个新的命令。

        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 命令前缀
          * ``**kwargs``: 其他传递给 ``on_shell_command`` 的参数，将会覆盖命令组默认值

        :返回:

          - ``Type[Matcher]``
        """
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        cmd = self.basecmd + sub_cmd

        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        return on_shell_command(cmd, **final_kwargs)


class MatcherGroup:
    """事件响应器组合，统一管理。为 ``Matcher`` 创建提供默认属性。"""

    def __init__(self, **kwargs):
        """
        :说明:

          创建一个事件响应器组合，参数为默认值，与 ``on`` 一致
        """
        self.matchers: List[Type[Matcher]] = []
        """
        :类型: ``List[Type[Matcher]]``
        :说明: 组内事件响应器列表
        """
        self.base_kwargs: Dict[str, Any] = kwargs
        """
        - **类型**: ``Dict[str, Any]``
        - **说明**: 其他传递给 ``on`` 的参数默认值
        """

    def on(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个基础事件响应器，可自定义类型。

        :参数:

          * ``type: str``: 事件响应器类型
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        matcher = on(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_metaevent(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个元事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        final_kwargs.pop("permission", None)
        matcher = on_metaevent(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_message(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_message(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_notice(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个通知事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_notice(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_request(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个请求事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_request(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_startswith(self, msg: Union[str, Tuple[str, ...]],
                      **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

        :参数:

          * ``msg: Union[str, Tuple[str, ...]]``: 指定消息开头内容
          * ``ignorecase: bool``: 是否忽略大小写
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_startswith(msg, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_endswith(self, msg: Union[str, Tuple[str, ...]],
                    **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

        :参数:

          * ``msg: Union[str, Tuple[str, ...]]``: 指定消息结尾内容
          * ``ignorecase: bool``: 是否忽略大小写
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_endswith(msg, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_keyword(self, keywords: Set[str], **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

        :参数:

          * ``keywords: Set[str]``: 关键词列表
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_keyword(keywords, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_command(self,
                   cmd: Union[str, Tuple[str, ...]],
                   aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
                   **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息以指定命令开头时响应。

          命令匹配规则参考: `命令形式匹配 <rule.html#command-command>`_

        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
          * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_command(cmd, aliases=aliases, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_shell_command(self,
                         cmd: Union[str, Tuple[str, ...]],
                         aliases: Optional[Set[Union[str, Tuple[str,
                                                                ...]]]] = None,
                         parser: Optional[ArgumentParser] = None,
                         **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个支持 ``shell_like`` 解析参数的命令消息事件响应器。

          与普通的 ``on_command`` 不同的是，在添加 ``parser`` 参数时, 响应器会自动处理消息。

          并将用户输入的原始参数列表保存在 ``state["argv"]``, ``parser`` 处理的参数保存在 ``state["args"]`` 中

        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
          * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
          * ``parser: Optional[ArgumentParser]``: ``nonebot.rule.ArgumentParser`` 对象
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_shell_command(cmd,
                                   aliases=aliases,
                                   parser=parser,
                                   **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_regex(self,
                 pattern: str,
                 flags: Union[int, re.RegexFlag] = 0,
                 **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

          命令匹配规则参考: `正则匹配 <rule.html#regex-regex-flags-0>`_

        :参数:

          * ``pattern: str``: 正则表达式
          * ``flags: Union[int, re.RegexFlag]``: 正则匹配标志
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Handler]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state
          * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_regex(pattern, flags=flags, **final_kwargs)
        self.matchers.append(matcher)
        return matcher


def _load_plugin(manager: PluginManager, plugin_name: str) -> Optional[Plugin]:
    if plugin_name.startswith("_"):
        return None

    if plugin_name in plugins:
        return None

    try:
        module = manager.load_plugin(plugin_name)

        plugin = Plugin(plugin_name, module)
        plugins[plugin_name] = plugin
        logger.opt(
            colors=True).success(f'Succeeded to import "<y>{plugin_name}</y>"')
        return plugin
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f'<r><bg #f8bbd0>Failed to import "{plugin_name}"</bg #f8bbd0></r>')
        return None


def load_plugin(module_path: str) -> Optional[Plugin]:
    """
    :说明:

      使用 ``PluginManager`` 加载单个插件，可以是本地插件或是通过 ``pip`` 安装的插件。

    :参数:

      * ``module_path: str``: 插件名称 ``path.to.your.plugin``

    :返回:

      - ``Optional[Plugin]``
    """

    context: Context = copy_context()
    manager = PluginManager(PLUGIN_NAMESPACE, plugins=[module_path])
    return context.run(_load_plugin, manager, module_path)


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    """
    :说明:

      导入目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``*plugin_dir: str``: 插件路径

    :返回:

      - ``Set[Plugin]``
    """
    loaded_plugins = set()
    manager = PluginManager(PLUGIN_NAMESPACE, search_path=plugin_dir)
    for plugin_name in manager.list_plugins():
        context: Context = copy_context()
        result = context.run(_load_plugin, manager, plugin_name)
        if result:
            loaded_plugins.add(result)
    return loaded_plugins


def load_all_plugins(module_path: Set[str],
                     plugin_dir: Set[str]) -> Set[Plugin]:
    """
    :说明:

      导入指定列表中的插件以及指定目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``module_path: Set[str]``: 指定插件集合
      - ``plugin_dir: Set[str]``: 指定插件路径集合

    :返回:

      - ``Set[Plugin]``
    """
    loaded_plugins = set()
    manager = PluginManager(PLUGIN_NAMESPACE, module_path, plugin_dir)
    for plugin_name in manager.list_plugins():
        context: Context = copy_context()
        result = context.run(_load_plugin, manager, plugin_name)
        if result:
            loaded_plugins.add(result)
    return loaded_plugins


def load_from_json(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """
    :说明:

      导入指定 json 文件中的 ``plugins`` 以及 ``plugin_dirs`` 下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``file_path: str``: 指定 json 文件路径
      - ``encoding: str``: 指定 json 文件编码

    :返回:

      - ``Set[Plugin]``
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = json.load(f)
    plugins = data.get("plugins")
    plugin_dirs = data.get("plugin_dirs")
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs,
                      list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_from_toml(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """
    :说明:

      导入指定 toml 文件 ``[nonebot.plugins]`` 中的 ``plugins`` 以及 ``plugin_dirs`` 下多个插件，
      以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``file_path: str``: 指定 toml 文件路径
      - ``encoding: str``: 指定 toml 文件编码

    :返回:

      - ``Set[Plugin]``
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = tomlkit.parse(f.read())

    nonebot_data = data.get("nonebot", {}).get("plugins")
    if not nonebot_data:
        raise ValueError("Cannot find '[nonebot.plugins]' in given toml file!")
    plugins = nonebot_data.get("plugins", [])
    plugin_dirs = nonebot_data.get("plugin_dirs", [])
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs,
                      list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_builtin_plugins(name: str = "echo") -> Optional[Plugin]:
    """
    :说明:

      导入 NoneBot 内置插件

    :返回:

      - ``Plugin``
    """
    return load_plugin(f"nonebot.plugins.{name}")


def get_plugin(name: str) -> Optional[Plugin]:
    """
    :说明:

      获取当前导入的某个插件。

    :参数:

      * ``name: str``: 插件名，与 ``load_plugin`` 参数一致。如果为 ``load_plugins`` 导入的插件，则为文件(夹)名。

    :返回:

      - ``Optional[Plugin]``
    """
    return plugins.get(name)


def get_loaded_plugins() -> Set[Plugin]:
    """
    :说明:

      获取当前已导入的所有插件。

    :返回:

      - ``Set[Plugin]``
    """
    return set(plugins.values())


def require(name: str) -> Optional[Export]:
    """
    :说明:

      获取一个插件的导出内容

    :参数:

      * ``name: str``: 插件名，与 ``load_plugin`` 参数一致。如果为 ``load_plugins`` 导入的插件，则为文件(夹)名。

    :返回:

      - ``Optional[Export]``
    """
    plugin = get_plugin(name) or load_plugin(name)
    return plugin.export if plugin else None
