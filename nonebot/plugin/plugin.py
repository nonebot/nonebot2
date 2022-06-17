"""本模块定义插件对象。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.plugin 模块
"""
from types import ModuleType
from dataclasses import field, dataclass
from typing import TYPE_CHECKING, Any, Set, Dict, Type, Optional

from pydantic import BaseModel

from nonebot.matcher import Matcher

from .export import Export
from . import _plugins as plugins  # FIXME: backport for nonebug

if TYPE_CHECKING:
    from .manager import PluginManager


@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件可阅读名称"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    config: Optional[Type[BaseModel]] = None
    """插件配置项"""
    extra: Dict[Any, Any] = field(default_factory=dict)


@dataclass(eq=False)
class Plugin:
    """存储插件信息"""

    name: str
    """插件索引标识，NoneBot 使用 文件/文件夹 名称作为标识符"""
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
    metadata: Optional[PluginMetadata] = None
