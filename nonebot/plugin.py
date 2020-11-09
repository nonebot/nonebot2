"""
插件
====

为 NoneBot 插件开发提供便携的定义函数。
"""

import re
import sys
import pkgutil
import importlib
from dataclasses import dataclass
from importlib._bootstrap import _load

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.typing import Handler, RuleChecker
from nonebot.rule import Rule, startswith, endswith, keyword, command, regex
from nonebot.typing import Any, Set, List, Dict, Type, Tuple, Union, Optional, ModuleType

plugins: Dict[str, "Plugin"] = {}
"""
:类型: ``Dict[str, Plugin]``
:说明: 已加载的插件
"""

_tmp_matchers: Set[Type[Matcher]] = set()


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


def on(type: str = "",
       rule: Optional[Union[Rule, RuleChecker]] = None,
       permission: Optional[Permission] = None,
       *,
       handlers: Optional[List[Handler]] = None,
       temp: bool = False,
       priority: int = 1,
       block: bool = False,
       state: Optional[dict] = None) -> Type[Matcher]:
    """
    :说明:
      注册一个基础事件响应器，可自定义类型。
    :参数:
      * ``type: str``: 事件响应器类型
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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
    """
    :说明:
      注册一个元事件响应器。
    :参数:
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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
    """
    :说明:
      注册一个消息事件响应器。
    :参数:
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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
    """
    :说明:
      注册一个通知事件响应器。
    :参数:
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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
    """
    :说明:
      注册一个请求事件响应器。
    :参数:
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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
                          default_state=state)
    _tmp_matchers.add(matcher)
    return matcher


def on_startswith(msg: str,
                  rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                  **kwargs) -> Type[Matcher]:
    """
    :说明:
      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容开头时响应。
    :参数:
      * ``msg: str``: 指定消息开头内容
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
    :返回:
      - ``Type[Matcher]``
    """
    return on_message(startswith(msg) & rule, **kwargs)


def on_endswith(msg: str,
                rule: Optional[Optional[Union[Rule, RuleChecker]]] = None,
                **kwargs) -> Type[Matcher]:
    """
    :说明:
      注册一个消息事件响应器，并且当消息的**文本部分**以指定内容结尾时响应。
    :参数:
      * ``msg: str``: 指定消息结尾内容
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
    :返回:
      - ``Type[Matcher]``
    """
    return on_message(endswith(msg) & rule, **kwargs)


def on_keyword(keywords: Set[str],
               rule: Optional[Union[Rule, RuleChecker]] = None,
               **kwargs) -> Type[Matcher]:
    """
    :说明:
      注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应。
    :参数:
      * ``keywords: Set[str]``: 关键词列表
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
    :返回:
      - ``Type[Matcher]``
    """
    return on_message(keyword(*keywords) & rule, **kwargs)


def on_command(cmd: Union[str, Tuple[str, ...]],
               rule: Optional[Union[Rule, RuleChecker]] = None,
               aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
               **kwargs) -> Type[Matcher]:
    """
    :说明:
      注册一个消息事件响应器，并且当消息以指定命令开头时响应。

      命令匹配规则参考: `命令形式匹配 <rule.html#command-command>`_
    :参数:
      * ``cmd: Union[str, Tuple[str, ...]]``: 指定命令内容
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``aliases: Optional[Set[Union[str, Tuple[str, ...]]]]``: 命令别名
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
    :返回:
      - ``Type[Matcher]``
    """

    async def _strip_cmd(bot, event, state: dict):
        message = event.message
        event.message = message.__class__(
            str(message)[len(state["_prefix"]["raw_command"]):].strip())

    handlers = kwargs.pop("handlers", [])
    handlers.insert(0, _strip_cmd)

    commands = set([cmd]) | (aliases or set())
    return on_message(command(*commands) & rule, handlers=handlers, **kwargs)


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
      * ``rule: Optional[Union[Rule, RuleChecker]]``: 事件响应规则
      * ``permission: Optional[Permission]``: 事件响应权限
      * ``handlers: Optional[List[Handler]]``: 事件处理函数列表
      * ``temp: bool``: 是否为临时事件响应器（仅执行一次）
      * ``priority: int``: 事件响应器优先级
      * ``block: bool``: 是否阻止事件向更低优先级传递
      * ``state: Optional[dict]``: 默认的 state
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


def load_plugin(module_path: str) -> Optional[Plugin]:
    """
    :说明:
      使用 ``importlib`` 加载单个插件，可以是本地插件或是通过 ``pip`` 安装的插件。
    :参数:
      * ``module_path: str``: 插件名称 ``path.to.your.plugin``
    :返回:
      - ``Optional[Plugin]``
    """
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
    """
    :说明:
      导入目录下多个插件，以 ``_`` 开头的插件不会被导入！
    :参数:
      - ``*plugin_dir: str``: 插件路径
    :返回:
      - ``Set[Plugin]``
    """
    loaded_plugins = set()
    for module_info in pkgutil.iter_modules(plugin_dir):
        _tmp_matchers.clear()
        name = module_info.name
        if name.startswith("_"):
            continue

        spec = module_info.module_finder.find_spec(name, None)
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


def load_builtin_plugins() -> Optional[Plugin]:
    """
    :说明:
      导入 NoneBot 内置插件
    :返回:
      - ``Plugin``
    """
    return load_plugin("nonebot.plugins.base")


def get_loaded_plugins() -> Set[Plugin]:
    """
    :说明:
      获取当前已导入的插件。
    :返回:
      - ``Set[Plugin]``
    """
    return set(plugins.values())
