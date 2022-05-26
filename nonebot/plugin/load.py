"""本模块定义插件加载接口。

FrontMatter:
    sidebar_position: 1
    description: nonebot.plugin.load 模块
"""
import json
import warnings
from typing import Set, Iterable, Optional

import tomlkit

from .export import Export
from .plugin import Plugin
from .manager import PluginManager
from . import _managers, get_plugin, _module_name_to_plugin_name


def load_plugin(module_path: str) -> Optional[Plugin]:
    """加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。

    参数:
        module_path: 插件名称 `path.to.your.plugin`
    """

    manager = PluginManager([module_path])
    _managers.append(manager)
    return manager.load_plugin(module_path)


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    """导入文件夹下多个插件，以 `_` 开头的插件不会被导入!

    参数:
        plugin_dir: 文件夹路径
    """
    manager = PluginManager(search_path=plugin_dir)
    _managers.append(manager)
    return manager.load_all_plugins()


def load_all_plugins(
    module_path: Iterable[str], plugin_dir: Iterable[str]
) -> Set[Plugin]:
    """导入指定列表中的插件以及指定目录下多个插件，以 `_` 开头的插件不会被导入!

    参数:
        module_path: 指定插件集合
        plugin_dir: 指定文件夹路径集合
    """
    manager = PluginManager(module_path, plugin_dir)
    _managers.append(manager)
    return manager.load_all_plugins()


def load_from_json(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """导入指定 json 文件中的 `plugins` 以及 `plugin_dirs` 下多个插件，以 `_` 开头的插件不会被导入!

    参数:
        file_path: 指定 json 文件路径
        encoding: 指定 json 文件编码

    用法:
        ```json title=plugins.json
        {
            "plugins": ["some_plugin"],
            "plugin_dirs": ["some_dir"]
        }
        ```

        ```python
        nonebot.load_from_json("plugins.json")
        ```
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = json.load(f)
    plugins = data.get("plugins")
    plugin_dirs = data.get("plugin_dirs")
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs, list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_from_toml(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """导入指定 toml 文件 `[tool.nonebot]` 中的 `plugins` 以及 `plugin_dirs` 下多个插件，以 `_` 开头的插件不会被导入!

    参数:
        file_path: 指定 toml 文件路径
        encoding: 指定 toml 文件编码

    用法:
        ```toml title=pyproject.toml
        [tool.nonebot]
        plugins = ["some_plugin"]
        plugin_dirs = ["some_dir"]
        ```

        ```python
        nonebot.load_from_toml("pyproject.toml")
        ```
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = tomlkit.parse(f.read())  # type: ignore

    nonebot_data = data.get("tool", {}).get("nonebot")
    if not nonebot_data:
        nonebot_data = data.get("nonebot", {}).get("plugins")
        if nonebot_data:
            warnings.warn(
                "[nonebot.plugins] table is deprecated. Use [tool.nonebot] instead.",
                DeprecationWarning,
            )
        else:
            raise ValueError("Cannot find '[tool.nonebot]' in given toml file!")
    plugins = nonebot_data.get("plugins", [])
    plugin_dirs = nonebot_data.get("plugin_dirs", [])
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs, list), "plugin_dirs must be a list of directories"
    return load_all_plugins(plugins, plugin_dirs)


def load_builtin_plugin(name: str) -> Optional[Plugin]:
    """导入 NoneBot 内置插件。

    参数:
        name: 插件名称
    """
    return load_plugin(f"nonebot.plugins.{name}")


def load_builtin_plugins(*plugins: str) -> Set[Plugin]:
    """导入多个 NoneBot 内置插件。

    参数:
        plugins: 插件名称列表
    """
    return load_all_plugins([f"nonebot.plugins.{p}" for p in plugins], [])


def _find_manager_by_name(name: str) -> Optional[PluginManager]:
    for manager in reversed(_managers):
        if name in manager.plugins or name in manager.searched_plugins:
            return manager


def require(name: str) -> Export:
    """获取一个插件的导出内容。

    如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

    参数:
        name: 插件名，即 {ref}`nonebot.plugin.plugin.Plugin.name`。

    异常:
        RuntimeError: 插件无法加载
    """
    plugin = get_plugin(_module_name_to_plugin_name(name))
    if not plugin:
        manager = _find_manager_by_name(name)
        if manager:
            plugin = manager.load_plugin(name)
        else:
            plugin = load_plugin(name)
        if not plugin:
            raise RuntimeError(f'Cannot load plugin "{name}"!')
    return plugin.export
