"""
插件
====

为 NoneBot 插件开发提供便携的定义函数。
"""

import re
import sys
import pkgutil
import importlib
from types import ModuleType
from dataclasses import dataclass
from importlib._bootstrap import _load
from contextvars import Context, ContextVar, copy_context
from typing import Any, Set, List, Dict, Type, Tuple, Union, Optional, TYPE_CHECKING

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.typing import T_State, T_StateFactory, T_Handler, T_RuleChecker
from nonebot.rule import Rule, startswith, endswith, keyword, command, shell_command, ArgumentParser, regex

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event

plugins: Dict[str, "Plugin"] = {}
"""
:类型: ``Dict[str, Plugin]``
:说明: 已加载的插件
"""

_export: ContextVar["Export"] = ContextVar("_export")
_tmp_matchers: ContextVar[Set[Type[Matcher]]] = ContextVar("_tmp_matchers")


class Export(dict):
    """
    :说明:

      插件导出内容以使得其他插件可以获得。

    :示例:

    .. code-block:: python

        nonebot.export().default = "bar"

        @nonebot.export()
        def some_function():
            pass

        # this doesn't work before python 3.9
        # use
        # export = nonebot.export(); @export.sub
        # instead
        # See also PEP-614: https://www.python.org/dev/peps/pep-0614/
        @nonebot.export().sub
        def something_else():
            pass
    """

    def __call__(self, func, **kwargs):
        self[func.__name__] = func
        self.update(kwargs)
        return func

    def __setitem__(self, key, value):
        super().__setitem__(key,
                            Export(value) if isinstance(value, dict) else value)

    def __setattr__(self, name, value):
        self[name] = Export(value) if isinstance(value, dict) else value

    def __getattr__(self, name):
        if name not in self:
            self[name] = Export()
        return self[name]


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
    matcher: Set[Type[Matcher]]
    """
    - **类型**: ``Set[Type[Matcher]]``
    - **说明**: 插件内定义的 ``Matcher``
    """
    export: Export
    """
    - **类型**: ``Export``
    - **说明**: 插件内定义的导出内容
    """


def on(type: str = "",
       rule: Optional[Union[Rule, T_RuleChecker]] = None,
       permission: Optional[Permission] = None,
       *,
       handlers: Optional[List[T_Handler]] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
                          default_state=state,
                          default_state_factory=state_factory)
    _tmp_matchers.get().add(matcher)
    return matcher


def on_metaevent(
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        *,
        handlers: Optional[List[T_Handler]] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
                          default_state=state,
                          default_state_factory=state_factory)
    _tmp_matchers.get().add(matcher)
    return matcher


def on_message(rule: Optional[Union[Rule, T_RuleChecker]] = None,
               permission: Optional[Permission] = None,
               *,
               handlers: Optional[List[T_Handler]] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
                          default_state=state,
                          default_state_factory=state_factory)
    _tmp_matchers.get().add(matcher)
    return matcher


def on_notice(rule: Optional[Union[Rule, T_RuleChecker]] = None,
              *,
              handlers: Optional[List[T_Handler]] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
                          default_state=state,
                          default_state_factory=state_factory)
    _tmp_matchers.get().add(matcher)
    return matcher


def on_request(rule: Optional[Union[Rule, T_RuleChecker]] = None,
               *,
               handlers: Optional[List[T_Handler]] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
                          default_state=state,
                          default_state_factory=state_factory)
    _tmp_matchers.get().add(matcher)
    return matcher


def on_startswith(msg: str,
                  rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
                  **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

    :参数:

      * ``msg: str``: 指定消息开头内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(startswith(msg) & rule, **kwargs)


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
                **kwargs) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

    :参数:

      * ``msg: str``: 指定消息结尾内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state
      * ``state_factory: Optional[T_StateFactory]``: 默认 state 的工厂函数

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(endswith(msg) & rule, **kwargs)


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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
             rule: Optional[Rule] = None,
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
      * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``**kwargs``: 其他传递给 ``on_command`` 的参数，将会覆盖命令组默认值

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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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

    def on_startswith(self, msg: str, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

        :参数:

          * ``msg: str``: 指定消息开头内容
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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

    def on_endswith(self, msg: str, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

        :参数:

          * ``msg: str``: 指定消息结尾内容
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Permission]``: 事件响应权限
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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
          * ``handlers: Optional[List[T_Handler]]``: 事件处理函数列表
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


def load_plugin(module_path: str) -> Optional[Plugin]:
    """
    :说明:

      使用 ``importlib`` 加载单个插件，可以是本地插件或是通过 ``pip`` 安装的插件。

    :参数:

      * ``module_path: str``: 插件名称 ``path.to.your.plugin``

    :返回:

      - ``Optional[Plugin]``
    """

    def _load_plugin(module_path: str) -> Optional[Plugin]:
        try:
            _tmp_matchers.set(set())
            _export.set(Export())
            if module_path in plugins:
                return plugins[module_path]
            elif module_path in sys.modules:
                logger.warning(
                    f"Module {module_path} has been loaded by other plugins! Ignored"
                )
                return None
            module = importlib.import_module(module_path)
            for m in _tmp_matchers.get():
                m.module = module_path
            plugin = Plugin(module_path, module, _tmp_matchers.get(),
                            _export.get())
            plugins[module_path] = plugin
            logger.opt(
                colors=True).info(f'Succeeded to import "<y>{module_path}</y>"')
            return plugin
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f'<r><bg #f8bbd0>Failed to import "{module_path}"</bg #f8bbd0></r>'
            )
            return None

    context: Context = copy_context()
    return context.run(_load_plugin, module_path)


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    """
    :说明:

      导入目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``*plugin_dir: str``: 插件路径

    :返回:

      - ``Set[Plugin]``
    """

    def _load_plugin(module_info) -> Optional[Plugin]:
        _tmp_matchers.set(set())
        _export.set(Export())
        name = module_info.name
        if name.startswith("_"):
            return None

        spec = module_info.module_finder.find_spec(name, None)
        if not spec:
            logger.warning(
                f"Module {name} cannot be loaded! Check module name first.")
        elif spec.name in plugins:
            return None
        elif spec.name in sys.modules:
            logger.warning(
                f"Module {spec.name} has been loaded by other plugin! Ignored")
            return None

        try:
            module = _load(spec)

            for m in _tmp_matchers.get():
                m.module = name
            plugin = Plugin(name, module, _tmp_matchers.get(), _export.get())
            plugins[name] = plugin
            logger.opt(colors=True).info(f'Succeeded to import "<y>{name}</y>"')
            return plugin
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f'<r><bg #f8bbd0>Failed to import "{name}"</bg #f8bbd0></r>')
            return None

    loaded_plugins = set()
    for module_info in pkgutil.iter_modules(plugin_dir):
        context: Context = copy_context()
        result = context.run(_load_plugin, module_info)
        if result:
            loaded_plugins.add(result)
    return loaded_plugins


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


def export() -> Export:
    """
    :说明:

      获取插件的导出内容对象

    :返回:

      - ``Export``
    """
    return _export.get()


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
