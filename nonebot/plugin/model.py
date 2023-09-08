"""本模块定义插件相关信息。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.model 模块
"""

import contextlib
from types import ModuleType
from dataclasses import field, dataclass
from typing import TYPE_CHECKING, Any, Set, Dict, Type, Optional

from pydantic import BaseModel

from nonebot.matcher import Matcher
from nonebot.utils import resolve_dot_notation

if TYPE_CHECKING:
    from nonebot.adapters import Adapter

    from .manager import PluginManager


@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件名称"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    type: Optional[str] = None
    """插件类型，用于商店分类"""
    homepage: Optional[str] = None
    """插件主页"""
    config: Optional[Type[BaseModel]] = None
    """插件配置项"""
    supported_adapters: Optional[Set[str]] = None
    """插件支持的适配器模块路径

    格式为 `<module>[:<Adapter>]`，`~` 为 `nonebot.adapters.` 的缩写。

    `None` 表示支持**所有适配器**。
    """
    extra: Dict[Any, Any] = field(default_factory=dict)
    """插件额外信息，可由插件编写者自由扩展定义"""

    def get_supported_adapters(self) -> Optional[Set[Type["Adapter"]]]:
        """获取当前已安装的插件支持适配器类列表"""
        if self.supported_adapters is None:
            return None

        adapters = set()
        for adapter in self.supported_adapters:
            with contextlib.suppress(ModuleNotFoundError, AttributeError):
                adapters.add(
                    resolve_dot_notation(adapter, "Adapter", "nonebot.adapters.")
                )
        return adapters


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
    matcher: Set[Type[Matcher]] = field(default_factory=set)
    """插件加载时定义的 `Matcher`"""
    parent_plugin: Optional["Plugin"] = None
    """父插件"""
    sub_plugins: Set["Plugin"] = field(default_factory=set)
    """子插件集合"""
    metadata: Optional[PluginMetadata] = None
