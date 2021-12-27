import json
import warnings
from typing import Set, Iterable, Optional

import tomlkit

from . import _managers
from .export import Export
from .manager import PluginManager
from .plugin import Plugin, get_plugin


def load_plugin(module_path: str) -> Optional[Plugin]:
    """
    :说明:

      使用 ``PluginManager`` 加载单个插件，可以是本地插件或是通过 ``pip`` 安装的插件。

    :参数:

      * ``module_path: str``: 插件名称 ``path.to.your.plugin``

    :返回:

      - ``Optional[Plugin]``
    """

    manager = PluginManager([module_path])
    _managers.append(manager)
    return manager.load_plugin(module_path)


def load_plugins(*plugin_dir: str) -> Set[Plugin]:
    """
    :说明:

      导入目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``*plugin_dir: str``: 插件路径

    :返回:

      - ``Set[Plugin]``
    """
    manager = PluginManager(search_path=plugin_dir)
    _managers.append(manager)
    return manager.load_all_plugins()


def load_all_plugins(
    module_path: Iterable[str], plugin_dir: Iterable[str]
) -> Set[Plugin]:
    """
    :说明:

      导入指定列表中的插件以及指定目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``module_path: Iterable[str]``: 指定插件集合
      - ``plugin_dir: Iterable[str]``: 指定插件路径集合

    :返回:

      - ``Set[Plugin]``
    """
    manager = PluginManager(module_path, plugin_dir)
    _managers.append(manager)
    return manager.load_all_plugins()


def load_from_json(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """
    :说明:

      导入指定 json 文件中的 ``plugins`` 以及 ``plugin_dirs`` 下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``file_path: str``: 指定 json 文件路径
      - ``encoding: str``: 指定 json 文件编码

    :返回:

      - ``Set[Plugin]``
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = json.load(f)
    plugins = data.get("plugins")
    plugin_dirs = data.get("plugin_dirs")
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs, list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_from_toml(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """
    :说明:

      导入指定 toml 文件 ``[tool.nonebot]`` 中的 ``plugins`` 以及 ``plugin_dirs`` 下多个插件，
      以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``file_path: str``: 指定 toml 文件路径
      - ``encoding: str``: 指定 toml 文件编码

    :返回:

      - ``Set[Plugin]``
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = tomlkit.parse(f.read())  # type: ignore

    nonebot_data = data.get("tool", {}).get("nonebot")
    if not nonebot_data:
        nonebot_data = data.get("nonebot", {}).get("plugins")
        if nonebot_data:
            warnings.warn(
                "[nonebot.plugins] table are now deprecated. Use [tool.nonebot] instead.",
                DeprecationWarning,
            )
        else:
            raise ValueError("Cannot find '[tool.nonebot]' in given toml file!")
    plugins = nonebot_data.get("plugins", [])
    plugin_dirs = nonebot_data.get("plugin_dirs", [])
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs, list), "plugin_dirs must be a list of directories"
    return load_all_plugins(plugins, plugin_dirs)


def load_builtin_plugins(name: str) -> Optional[Plugin]:
    """
    :说明:

      导入 NoneBot 内置插件

    :返回:

      - ``Plugin``
    """
    return load_plugin(f"nonebot.plugins.{name}")


def require(name: str) -> Export:
    """
    :说明:

      获取一个插件的导出内容

    :参数:

      * ``name: str``: 插件名，与 ``load_plugin`` 参数一致。如果为 ``load_plugins`` 导入的插件，则为文件(夹)名。

    :返回:

      - ``Export``

    :异常:
      - ``RuntimeError``: 插件无法加载
    """
    plugin = get_plugin(name) or load_plugin(name)
    if not plugin:
        raise RuntimeError(f'Cannot load plugin "{name}"!')
    return plugin.export
