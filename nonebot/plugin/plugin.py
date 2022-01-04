from types import ModuleType
from dataclasses import field, dataclass
from typing import TYPE_CHECKING, Set, Dict, Type, Optional

from .export import Export
from nonebot.matcher import Matcher

if TYPE_CHECKING:
    from .manager import PluginManager

plugins: Dict[str, "Plugin"] = {}
"""
:类型: ``Dict[str, Plugin]``
:说明: 已加载的插件
"""


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
    module_name: str
    """
    - **类型**: ``str``
    - **说明**: 点分割模块路径
    """
    manager: "PluginManager"
    """
    - **类型**: ``PluginManager``
    - **说明**: 导入该插件的插件管理器
    """
    export: Export = field(default_factory=Export)
    """
    - **类型**: ``Export``
    - **说明**: 插件内定义的导出内容
    """
    matcher: Set[Type[Matcher]] = field(default_factory=set)
    """
    - **类型**: ``Set[Type[Matcher]]``
    - **说明**: 插件内定义的 ``Matcher``
    """
    parent_plugin: Optional["Plugin"] = None
    """
    - **类型**: ``Optional[Plugin]``
    - **说明**: 父插件
    """
    sub_plugins: Set["Plugin"] = field(default_factory=set)
    """
    - **类型**: ``Set[Plugin]``
    - **说明**: 子插件集合
    """


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


def _new_plugin(fullname: str, module: ModuleType, manager: "PluginManager") -> Plugin:
    name = fullname.rsplit(".", 1)[-1] if "." in fullname else fullname
    if name in plugins:
        raise RuntimeError("Plugin already exists! Check your plugin name.")
    plugin = Plugin(name, module, fullname, manager)
    plugins[name] = plugin
    return plugin
