import re
import sys
import inspect
from types import ModuleType
from typing import Any, Set, Dict, List, Type, Tuple, Union, Optional

from nonebot.matcher import Matcher
from .manager import _current_plugin
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.typing import (
    T_State,
    T_Handler,
    T_RuleChecker,
    T_PermissionChecker,
)
from nonebot.rule import (
    Rule,
    ArgumentParser,
    regex,
    command,
    keyword,
    endswith,
    startswith,
    shell_command,
)


def _store_matcher(matcher: Type[Matcher]) -> None:
    plugin = _current_plugin.get()
    # only store the matcher defined in the plugin
    if plugin:
        plugin.matcher.add(matcher)


def _get_matcher_module(depth: int = 1) -> Optional[ModuleType]:
    current_frame = inspect.currentframe()
    if current_frame is None:
        return None
    frame = inspect.getouterframes(current_frame)[depth + 1].frame
    module_name = frame.f_globals["__name__"]
    return sys.modules.get(module_name)


def on(
    type: str = "",
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    permission: Optional[Union[Permission, T_PermissionChecker]] = None,
    *,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    priority: int = 1,
    block: bool = False,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[Matcher]:
    """
    :说明:

      注册一个基础事件响应器，可自定义类型。

    :参数:

      * ``type: str``: 事件响应器类型
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(
        type,
        Rule() & rule,
        Permission() | permission,
        temp=temp,
        priority=priority,
        block=block,
        handlers=handlers,
        plugin=_current_plugin.get(),
        module=_get_matcher_module(_depth + 1),
        default_state=state,
    )
    _store_matcher(matcher)
    return matcher


def on_metaevent(
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    *,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    priority: int = 1,
    block: bool = False,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[Matcher]:
    """
    :说明:

      注册一个元事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(
        "meta_event",
        Rule() & rule,
        Permission(),
        temp=temp,
        priority=priority,
        block=block,
        handlers=handlers,
        plugin=_current_plugin.get(),
        module=_get_matcher_module(_depth + 1),
        default_state=state,
    )
    _store_matcher(matcher)
    return matcher


def on_message(
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    permission: Optional[Union[Permission, T_PermissionChecker]] = None,
    *,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    priority: int = 1,
    block: bool = True,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(
        "message",
        Rule() & rule,
        Permission() | permission,
        temp=temp,
        priority=priority,
        block=block,
        handlers=handlers,
        plugin=_current_plugin.get(),
        module=_get_matcher_module(_depth + 1),
        default_state=state,
    )
    _store_matcher(matcher)
    return matcher


def on_notice(
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    *,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    priority: int = 1,
    block: bool = False,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[Matcher]:
    """
    :说明:

      注册一个通知事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(
        "notice",
        Rule() & rule,
        Permission(),
        temp=temp,
        priority=priority,
        block=block,
        handlers=handlers,
        plugin=_current_plugin.get(),
        module=_get_matcher_module(_depth + 1),
        default_state=state,
    )
    _store_matcher(matcher)
    return matcher


def on_request(
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    *,
    handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
    temp: bool = False,
    priority: int = 1,
    block: bool = False,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> Type[Matcher]:
    """
    :说明:

      注册一个请求事件响应器。

    :参数:

      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    matcher = Matcher.new(
        "request",
        Rule() & rule,
        Permission(),
        temp=temp,
        priority=priority,
        block=block,
        handlers=handlers,
        plugin=_current_plugin.get(),
        module=_get_matcher_module(_depth + 1),
        default_state=state,
    )
    _store_matcher(matcher)
    return matcher


def on_startswith(
    msg: Union[str, Tuple[str, ...]],
    rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
    ignorecase: bool = False,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

    :参数:

      * ``msg: Union[str, Tuple[str, ...]]``: 指定消息开头内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``ignorecase: bool``: 是否忽略大小写
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(startswith(msg, ignorecase) & rule, **kwargs, _depth=_depth + 1)


def on_endswith(
    msg: Union[str, Tuple[str, ...]],
    rule: Optional[Optional[Union[Rule, T_RuleChecker]]] = None,
    ignorecase: bool = False,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

    :参数:

      * ``msg: Union[str, Tuple[str, ...]]``: 指定消息结尾内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``ignorecase: bool``: 是否忽略大小写
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(endswith(msg, ignorecase) & rule, **kwargs, _depth=_depth + 1)


def on_keyword(
    keywords: Set[str],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

    :参数:

      * ``keywords: Set[str]``: 关键词列表
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(keyword(*keywords) & rule, **kwargs, _depth=_depth + 1)


def on_command(
    cmd: Union[str, Tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息以指定命令开头时响应。

      命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`_

    :参数:

      * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """

    commands = set([cmd]) | (aliases or set())
    block = kwargs.pop("block", False)
    return on_message(
        command(*commands) & rule, block=block, **kwargs, _depth=_depth + 1
    )


def on_shell_command(
    cmd: Union[str, Tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
    parser: Optional[ArgumentParser] = None,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
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
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """

    commands = set([cmd]) | (aliases or set())
    return on_message(
        shell_command(*commands, parser=parser) & rule,
        **kwargs,
        _depth=_depth + 1,
    )


def on_regex(
    pattern: str,
    flags: Union[int, re.RegexFlag] = 0,
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> Type[Matcher]:
    """
    :说明:

      注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

      命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`_

    :参数:

      * ``pattern: str``: 正则表达式
      * ``flags: Union[int, re.RegexFlag]``: 正则匹配标志
      * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
      * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[T_State]``: 默认 state

    :返回:

      - ``Type[Matcher]``
    """
    return on_message(regex(pattern, flags) & rule, **kwargs, _depth=_depth + 1)


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

    def command(self, cmd: Union[str, Tuple[str, ...]], **kwargs) -> Type[Matcher]:
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
        return on_command(cmd, **final_kwargs, _depth=1)

    def shell_command(
        self, cmd: Union[str, Tuple[str, ...]], **kwargs
    ) -> Type[Matcher]:
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
        return on_shell_command(cmd, **final_kwargs, _depth=1)


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
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        matcher = on(**final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_metaevent(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个元事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        final_kwargs.pop("permission", None)
        matcher = on_metaevent(**final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_message(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_message(**final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_notice(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个通知事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_notice(**final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_request(self, **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个请求事件响应器。

        :参数:

          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_request(**final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_startswith(
        self, msg: Union[str, Tuple[str, ...]], **kwargs
    ) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

        :参数:

          * ``msg: Union[str, Tuple[str, ...]]``: 指定消息开头内容
          * ``ignorecase: bool``: 是否忽略大小写
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_startswith(msg, **final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_endswith(self, msg: Union[str, Tuple[str, ...]], **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

        :参数:

          * ``msg: Union[str, Tuple[str, ...]]``: 指定消息结尾内容
          * ``ignorecase: bool``: 是否忽略大小写
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_endswith(msg, **final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_keyword(self, keywords: Set[str], **kwargs) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

        :参数:

          * ``keywords: Set[str]``: 关键词列表
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_keyword(keywords, **final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_command(
        self,
        cmd: Union[str, Tuple[str, ...]],
        aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
        **kwargs,
    ) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息以指定命令开头时响应。

          命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`_

        :参数:

          * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
          * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_command(cmd, aliases=aliases, **final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher

    def on_shell_command(
        self,
        cmd: Union[str, Tuple[str, ...]],
        aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
        parser: Optional[ArgumentParser] = None,
        **kwargs,
    ) -> Type[Matcher]:
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
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_shell_command(
            cmd, aliases=aliases, parser=parser, **final_kwargs, _depth=1
        )
        self.matchers.append(matcher)
        return matcher

    def on_regex(
        self, pattern: str, flags: Union[int, re.RegexFlag] = 0, **kwargs
    ) -> Type[Matcher]:
        """
        :说明:

          注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

          命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`_

        :参数:

          * ``pattern: str``: 正则表达式
          * ``flags: Union[int, re.RegexFlag]``: 正则匹配标志
          * ``rule: Optional[Union[Rule, T_RuleChecker]]``: 事件响应规则
          * ``permission: Optional[Union[Permission, T_PermissionChecker]] =]]``: 事件响应权限
          * ``handlers: Optional[List[Union[T_Handler, Dependent]]]``: 事件处理函数列表
          * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
          * ``priority: int``: 事件响应器优先级
          * ``block: bool``: 是否阻止事件向更低优先级传递
          * ``state: Optional[T_State]``: 默认 state

        :返回:

          - ``Type[Matcher]``
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        final_kwargs.pop("type", None)
        matcher = on_regex(pattern, flags=flags, **final_kwargs, _depth=1)
        self.matchers.append(matcher)
        return matcher
