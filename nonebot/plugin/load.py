"""本模块定义插件加载接口。

FrontMatter:
    sidebar_position: 1
    description: nonebot.plugin.load 模块
"""

import json
from pathlib import Path
from types import ModuleType
from typing import Set, Union, Iterable, Optional

from nonebot.utils import path_to_module_name

from .plugin import Plugin
from .manager import PluginManager
from . import _managers, get_plugin, _current_plugin_chain, _module_name_to_plugin_name

try:  # pragma: py-gte-311
    import tomllib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:  # pragma: py-lt-311
    import tomli as tomllib


def load_plugin(module_path: Union[str, Path]) -> Optional[Plugin]:
    """加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。

    参数:
        module_path: 插件名称 `path.to.your.plugin`
            或插件路径 `pathlib.Path(path/to/your/plugin)`
    """
    module_path = (
        path_to_module_name(module_path)
        if isinstance(module_path, Path)
        else module_path
    )
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
    """导入指定 json 文件中的 `plugins` 以及 `plugin_dirs` 下多个插件。
    以 `_` 开头的插件不会被导入!

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
    with open(file_path, encoding=encoding) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise TypeError("json file must contains a dict!")
    plugins = data.get("plugins")
    plugin_dirs = data.get("plugin_dirs")
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs, list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_from_toml(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """导入指定 toml 文件 `[tool.nonebot]` 中的
    `plugins` 以及 `plugin_dirs` 下多个插件。
    以 `_` 开头的插件不会被导入!

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
    with open(file_path, encoding=encoding) as f:
        data = tomllib.loads(f.read())

    nonebot_data = data.get("tool", {}).get("nonebot")
    if nonebot_data is None:
        raise ValueError("Cannot find '[tool.nonebot]' in given toml file!")
    if not isinstance(nonebot_data, dict):
        raise TypeError("'[tool.nonebot]' must be a Table!")
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


def require(name: str) -> ModuleType:
    """获取一个插件的导出内容。

    如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

    参数:
        name: 插件名，即 {ref}`nonebot.plugin.plugin.Plugin.name`。

    异常:
        RuntimeError: 插件无法加载
    """
    plugin = get_plugin(_module_name_to_plugin_name(name))
    # if plugin not loaded
    if not plugin:
        # plugin already declared
        if manager := _find_manager_by_name(name):
            plugin = manager.load_plugin(name)
        # plugin not declared, try to declare and load it
        else:
            # clear current plugin chain, ensure plugin loaded in a new context
            _t = _current_plugin_chain.set(())
            try:
                plugin = load_plugin(name)
            finally:
                _current_plugin_chain.reset(_t)
    if not plugin:
        raise RuntimeError(f'Cannot load plugin "{name}"!')
    return plugin.module


def inherit_supported_adapters(*names: str) -> Optional[Set[str]]:
    """获取已加载插件的适配器支持状态集合。

    如果传入了多个插件名称，返回值会自动取交集。

    参数:
        names: 插件名称列表。

    异常:
        RuntimeError: 插件未加载
        ValueError: 插件缺少元数据
    """
    final_supported: Optional[Set[str]] = None

    for name in names:
        plugin = get_plugin(_module_name_to_plugin_name(name))
        if plugin is None:
            raise RuntimeError(f'Plugin "{name}" is not loaded!')
        meta = plugin.metadata
        if meta is None:
            raise ValueError(f'Plugin "{name}" has no metadata!')
        support = meta.supported_adapters
        if support is None:
            continue
        final_supported = (
            support if final_supported is None else (final_supported & support)
        )

    return final_supported and {
        f"nonebot.adapters.{adapter_name[1:]}"
        if adapter_name.startswith("~")
        else adapter_name
        for adapter_name in final_supported
    }
