"""本模块定义插件对象。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.plugin 模块
"""
from types import ModuleType
from dataclasses import field, dataclass
from typing import TYPE_CHECKING, Set, Dict, Type, Optional

from nonebot.matcher import Matcher

from .export import Export

if TYPE_CHECKING:
    from .manager import PluginManager

plugins: Dict[str, "Plugin"] = {}
"""已加载的插件"""


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
    """插件内定义的导出内容"""
    matcher: Set[Type[Matcher]] = field(default_factory=set)
    """插件内定义的 `Matcher`"""
    parent_plugin: Optional["Plugin"] = None
    """父插件"""
    sub_plugins: Set["Plugin"] = field(default_factory=set)
    """子插件集合"""


def get_plugin(name: str) -> Optional[Plugin]:
    """获取已经导入的某个插件。

    如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

    参数:
        name: 插件名，即 {ref}`nonebot.plugin.plugin.Plugin.name`。
    """
    return plugins.get(name)


def get_loaded_plugins() -> Set[Plugin]:
    """获取当前已导入的所有插件。"""
    return set(plugins.values())


def _new_plugin(fullname: str, module: ModuleType, manager: "PluginManager") -> Plugin:
    name = fullname.rsplit(".", 1)[-1] if "." in fullname else fullname
    if name in plugins:
        raise RuntimeError("Plugin already exists! Check your plugin name.")
    plugin = Plugin(name, module, fullname, manager)
    return plugin


def _confirm_plugin(plugin: Plugin) -> None:
    if plugin.name in plugins:
        raise RuntimeError("Plugin already exists! Check your plugin name.")
    plugins[plugin.name] = plugin
