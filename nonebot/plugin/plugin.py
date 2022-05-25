"""本模块定义插件对象。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.plugin 模块
"""
from types import ModuleType
from dataclasses import field, dataclass
from typing import TYPE_CHECKING, Set, Type, Optional

from nonebot.matcher import Matcher

from .export import Export
from . import _plugins as plugins  # FIXME: backport for nonebug

if TYPE_CHECKING:
    from .manager import PluginManager


@dataclass(eq=False)
class Plugin(object):
    """存储插件信息"""

    name: str
    """插件名称，使用 文件/文件夹 名称作为插件名"""
    module: ModuleType
    """插件模块对象"""
    module_name: str
    """点分割模块路径"""
    manager: "PluginManager"
    """导入该插件的插件管理器"""
    export: Export = field(default_factory=Export)
    """**Deprecated:** 插件内定义的导出内容"""
    matcher: Set[Type[Matcher]] = field(default_factory=set)
    """插件内定义的 `Matcher`"""
    parent_plugin: Optional["Plugin"] = None
    """父插件"""
    sub_plugins: Set["Plugin"] = field(default_factory=set)
    """子插件集合"""
