"""本模块定义事件响应器便携定义函数。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 2
    description: nonebot.plugin.on 模块
"""

from datetime import datetime, timedelta
import inspect
import re
from types import ModuleType
from typing import Any, Optional, Union
import warnings

from nonebot.adapters import Event
from nonebot.dependencies import Dependent
from nonebot.matcher import Matcher, MatcherSource
from nonebot.permission import Permission
from nonebot.rule import (
    ArgumentParser,
    Rule,
    command,
    endswith,
    fullmatch,
    is_type,
    keyword,
    regex,
    shell_command,
    startswith,
)
from nonebot.typing import T_Handler, T_PermissionChecker, T_RuleChecker, T_State

from . import get_plugin_by_module_name
from .manager import _current_plugin
from .model import Plugin


def store_matcher(matcher: type[Matcher]) -> None:
    """存储一个事件响应器到插件。

    参数:
        matcher: 事件响应器
    """
    # only store the matcher defined when plugin loading
    if plugin := _current_plugin.get():
        plugin.matcher.add(matcher)


def get_matcher_plugin(depth: int = 1) -> Optional[Plugin]:  # pragma: no cover
    """获取事件响应器定义所在插件。

    **Deprecated**, 请使用 {ref}`nonebot.plugin.on.get_matcher_source` 获取信息。

    参数:
        depth: 调用栈深度
    """
    warnings.warn(
        "`get_matcher_plugin` is deprecated, please use `get_matcher_source` instead",
        DeprecationWarning,
    )
    return (source := get_matcher_source(depth + 1)) and source.plugin


def get_matcher_module(depth: int = 1) -> Optional[ModuleType]:  # pragma: no cover
    """获取事件响应器定义所在模块。

    **Deprecated**, 请使用 {ref}`nonebot.plugin.on.get_matcher_source` 获取信息。

    参数:
        depth: 调用栈深度
    """
    warnings.warn(
        "`get_matcher_module` is deprecated, please use `get_matcher_source` instead",
        DeprecationWarning,
    )
    return (source := get_matcher_source(depth + 1)) and source.module


def get_matcher_source(depth: int = 0) -> Optional[MatcherSource]:
    """获取事件响应器定义所在源码信息。

    参数:
        depth: 调用栈深度
    """
    current_frame = inspect.currentframe()
    if current_frame is None:
        return None

    frame = current_frame
    d = depth + 1
    while d > 0:
        frame = frame.f_back
        if frame is None:
            raise ValueError("Depth out of range")
        d -= 1

    module_name = (module := inspect.getmodule(frame)) and module.__name__

    # matcher defined when plugin loading
    plugin: Optional["Plugin"] = _current_plugin.get()
    # matcher defined when plugin running
    if plugin is None and module_name:
        plugin = get_plugin_by_module_name(module_name)

    return MatcherSource(
        plugin_id=plugin and plugin.id_,
        module_name=module_name,
        lineno=frame.f_lineno,
    )


def on(
    type: str = "",
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    permission: Optional[Union[Permission, T_PermissionChecker]] = None,
    *,
    handlers: Optional[list[Union[T_Handler, Dependent[Any]]]] = None,
    temp: bool = False,
    expire_time: Optional[Union[datetime, timedelta]] = None,
    priority: int = 1,
    block: bool = False,
    state: Optional[T_State] = None,
    _depth: int = 0,
) -> type[Matcher]:
    """注册一个基础事件响应器，可自定义类型。

    参数:
        type: 事件响应器类型
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    matcher = Matcher.new(
        type,
        Rule() & rule,
        Permission() | permission,
        temp=temp,
        expire_time=expire_time,
        priority=priority,
        block=block,
        handlers=handlers,
        source=get_matcher_source(_depth + 1),
        default_state=state,
    )
    store_matcher(matcher)
    return matcher


def on_metaevent(*args, _depth: int = 0, **kwargs) -> type[Matcher]:
    """注册一个元事件响应器。

    参数:
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on("meta_event", *args, **kwargs, _depth=_depth + 1)


def on_message(*args, _depth: int = 0, **kwargs) -> type[Matcher]:
    """注册一个消息事件响应器。

    参数:
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    kwargs.setdefault("block", True)
    return on("message", *args, **kwargs, _depth=_depth + 1)


def on_notice(*args, _depth: int = 0, **kwargs) -> type[Matcher]:
    """注册一个通知事件响应器。

    参数:
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on("notice", *args, **kwargs, _depth=_depth + 1)


def on_request(*args, _depth: int = 0, **kwargs) -> type[Matcher]:
    """注册一个请求事件响应器。

    参数:
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on("request", *args, **kwargs, _depth=_depth + 1)


def on_startswith(
    msg: Union[str, tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    ignorecase: bool = False,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

    参数:
        msg: 指定消息开头内容
        rule: 事件响应规则
        ignorecase: 是否忽略大小写
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(startswith(msg, ignorecase) & rule, **kwargs, _depth=_depth + 1)


def on_endswith(
    msg: Union[str, tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    ignorecase: bool = False,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

    参数:
        msg: 指定消息结尾内容
        rule: 事件响应规则
        ignorecase: 是否忽略大小写
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(endswith(msg, ignorecase) & rule, **kwargs, _depth=_depth + 1)


def on_fullmatch(
    msg: Union[str, tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    ignorecase: bool = False,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

    参数:
        msg: 指定消息全匹配内容
        rule: 事件响应规则
        ignorecase: 是否忽略大小写
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(fullmatch(msg, ignorecase) & rule, **kwargs, _depth=_depth + 1)


def on_keyword(
    keywords: set[str],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

    参数:
        keywords: 关键词列表
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(keyword(*keywords) & rule, **kwargs, _depth=_depth + 1)


def on_command(
    cmd: Union[str, tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    aliases: Optional[set[Union[str, tuple[str, ...]]]] = None,
    force_whitespace: Optional[Union[str, bool]] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息以指定命令开头时响应。

    命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`_

    参数:
        cmd: 指定命令内容
        rule: 事件响应规则
        aliases: 命令别名
        force_whitespace: 是否强制命令后必须有指定空白符
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """

    commands = {cmd} | (aliases or set())
    kwargs.setdefault("block", False)
    return on_message(
        command(*commands, force_whitespace=force_whitespace) & rule,
        **kwargs,
        _depth=_depth + 1,
    )


def on_shell_command(
    cmd: Union[str, tuple[str, ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    aliases: Optional[set[Union[str, tuple[str, ...]]]] = None,
    parser: Optional[ArgumentParser] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

    与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

    可以通过 {ref}`nonebot.params.ShellCommandArgv` 获取原始参数列表，
    通过 {ref}`nonebot.params.ShellCommandArgs` 获取解析后的参数字典。

    参数:
        cmd: 指定命令内容
        rule: 事件响应规则
        aliases: 命令别名
        parser: `nonebot.rule.ArgumentParser` 对象
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """

    commands = {cmd} | (aliases or set())
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
) -> type[Matcher]:
    """注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

    命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`_

    参数:
        pattern: 正则表达式
        flags: 正则匹配标志
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(regex(pattern, flags) & rule, **kwargs, _depth=_depth + 1)


def on_type(
    types: Union[type[Event], tuple[type[Event], ...]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    *,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """注册一个事件响应器，并且当事件为指定类型时响应。

    参数:
        types: 事件类型
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    event_types = types if isinstance(types, tuple) else (types,)
    return on(rule=is_type(*event_types) & rule, **kwargs, _depth=_depth + 1)


class _Group:
    def __init__(self, **kwargs):
        """创建一个事件响应器组合，参数为默认值，与 `on` 一致"""
        self.matchers: list[type[Matcher]] = []
        """组内事件响应器列表"""
        self.base_kwargs: dict[str, Any] = kwargs
        """其他传递给 `on` 的参数默认值"""

    def _get_final_kwargs(
        self, update: dict[str, Any], *, exclude: Optional[set[str]] = None
    ) -> dict[str, Any]:
        """获取最终传递给 `on` 的参数

        参数:
            update: 更新的关键字参数
            exclude: 需要排除的参数
        """
        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(update)
        if exclude:
            for key in exclude:
                final_kwargs.pop(key, None)
        final_kwargs["_depth"] = 1
        return final_kwargs


class CommandGroup(_Group):
    """命令组，用于声明一组有相同名称前缀的命令。

    参数:
        cmd: 指定命令内容
        prefix_aliases: 是否影响命令别名，给命令别名加前缀
        rule: 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """

    def __init__(
        self, cmd: Union[str, tuple[str, ...]], prefix_aliases: bool = False, **kwargs
    ):
        """命令前缀"""
        super().__init__(**kwargs)
        self.basecmd: tuple[str, ...] = (cmd,) if isinstance(cmd, str) else cmd
        self.base_kwargs.pop("aliases", None)
        self.prefix_aliases = prefix_aliases

    def __repr__(self) -> str:
        return f"CommandGroup(cmd={self.basecmd}, matchers={len(self.matchers)})"

    def command(self, cmd: Union[str, tuple[str, ...]], **kwargs) -> type[Matcher]:
        """注册一个新的命令。新参数将会覆盖命令组默认值

        参数:
            cmd: 指定命令内容
            aliases: 命令别名
            force_whitespace: 是否强制命令后必须有指定空白符
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        cmd = self.basecmd + sub_cmd
        if self.prefix_aliases and (aliases := kwargs.get("aliases")):
            kwargs["aliases"] = {
                self.basecmd + ((alias,) if isinstance(alias, str) else alias)
                for alias in aliases
            }
        matcher = on_command(cmd, **self._get_final_kwargs(kwargs))
        self.matchers.append(matcher)
        return matcher

    def shell_command(
        self, cmd: Union[str, tuple[str, ...]], **kwargs
    ) -> type[Matcher]:
        """注册一个新的 `shell_like` 命令。新参数将会覆盖命令组默认值

        参数:
            cmd: 指定命令内容
            rule: 事件响应规则
            aliases: 命令别名
            parser: `nonebot.rule.ArgumentParser` 对象
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        cmd = self.basecmd + sub_cmd
        if self.prefix_aliases and (aliases := kwargs.get("aliases")):
            kwargs["aliases"] = {
                self.basecmd + ((alias,) if isinstance(alias, str) else alias)
                for alias in aliases
            }
        matcher = on_shell_command(cmd, **self._get_final_kwargs(kwargs))
        self.matchers.append(matcher)
        return matcher


class MatcherGroup(_Group):
    """事件响应器组合，统一管理。为 `Matcher` 创建提供默认属性。"""

    def __repr__(self) -> str:
        return f"MatcherGroup(matchers={len(self.matchers)})"

    def on(self, **kwargs) -> type[Matcher]:
        """注册一个基础事件响应器，可自定义类型。

        参数:
            type: 事件响应器类型
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        matcher = on(**self._get_final_kwargs(kwargs))
        self.matchers.append(matcher)
        return matcher

    def on_metaevent(self, **kwargs) -> type[Matcher]:
        """注册一个元事件响应器。

        参数:
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type", "permission"})
        matcher = on_metaevent(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_message(self, **kwargs) -> type[Matcher]:
        """注册一个消息事件响应器。

        参数:
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_message(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_notice(self, **kwargs) -> type[Matcher]:
        """注册一个通知事件响应器。

        参数:
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type", "permission"})
        matcher = on_notice(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_request(self, **kwargs) -> type[Matcher]:
        """注册一个请求事件响应器。

        参数:
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type", "permission"})
        matcher = on_request(**final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_startswith(
        self, msg: Union[str, tuple[str, ...]], **kwargs
    ) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。

        参数:
            msg: 指定消息开头内容
            ignorecase: 是否忽略大小写
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_startswith(msg, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_endswith(self, msg: Union[str, tuple[str, ...]], **kwargs) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。

        参数:
            msg: 指定消息结尾内容
            ignorecase: 是否忽略大小写
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_endswith(msg, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_fullmatch(self, msg: Union[str, tuple[str, ...]], **kwargs) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息的**文本部分**与指定内容完全一致时响应。

        参数:
            msg: 指定消息全匹配内容
            rule: 事件响应规则
            ignorecase: 是否忽略大小写
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_fullmatch(msg, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_keyword(self, keywords: set[str], **kwargs) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。

        参数:
            keywords: 关键词列表
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_keyword(keywords, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_command(
        self,
        cmd: Union[str, tuple[str, ...]],
        aliases: Optional[set[Union[str, tuple[str, ...]]]] = None,
        force_whitespace: Optional[Union[str, bool]] = None,
        **kwargs,
    ) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息以指定命令开头时响应。

        命令匹配规则参考: `命令形式匹配 <rule.md#command-command>`_

        参数:
            cmd: 指定命令内容
            aliases: 命令别名
            force_whitespace: 是否强制命令后必须有指定空白符
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_command(
            cmd, aliases=aliases, force_whitespace=force_whitespace, **final_kwargs
        )
        self.matchers.append(matcher)
        return matcher

    def on_shell_command(
        self,
        cmd: Union[str, tuple[str, ...]],
        aliases: Optional[set[Union[str, tuple[str, ...]]]] = None,
        parser: Optional[ArgumentParser] = None,
        **kwargs,
    ) -> type[Matcher]:
        """注册一个支持 `shell_like` 解析参数的命令消息事件响应器。

        与普通的 `on_command` 不同的是，在添加 `parser` 参数时, 响应器会自动处理消息。

        可以通过 {ref}`nonebot.params.ShellCommandArgv` 获取原始参数列表，
        通过 {ref}`nonebot.params.ShellCommandArgs` 获取解析后的参数字典。

        参数:
            cmd: 指定命令内容
            aliases: 命令别名
            parser: `nonebot.rule.ArgumentParser` 对象
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_shell_command(cmd, aliases=aliases, parser=parser, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_regex(
        self, pattern: str, flags: Union[int, re.RegexFlag] = 0, **kwargs
    ) -> type[Matcher]:
        """注册一个消息事件响应器，并且当消息匹配正则表达式时响应。

        命令匹配规则参考: `正则匹配 <rule.md#regex-regex-flags-0>`_

        参数:
            pattern: 正则表达式
            flags: 正则匹配标志
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_regex(pattern, flags=flags, **final_kwargs)
        self.matchers.append(matcher)
        return matcher

    def on_type(
        self, types: Union[type[Event], tuple[type[Event]]], **kwargs
    ) -> type[Matcher]:
        """注册一个事件响应器，并且当事件为指定类型时响应。

        参数:
            types: 事件类型
            rule: 事件响应规则
            permission: 事件响应权限
            handlers: 事件处理函数列表
            temp: 是否为临时事件响应器（仅执行一次）
            expire_time: 事件响应器最终有效时间点，过时即被删除
            priority: 事件响应器优先级
            block: 是否阻止事件向更低优先级传递
            state: 默认 state
        """
        final_kwargs = self._get_final_kwargs(kwargs, exclude={"type"})
        matcher = on_type(types, **final_kwargs)
        self.matchers.append(matcher)
        return matcher
