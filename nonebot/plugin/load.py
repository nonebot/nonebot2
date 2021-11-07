from typing import Set, Optional

from .export import Export
from .manager import PluginManager
from .plugin import Plugin, get_plugin


# TODO
def _load_plugin(manager: PluginManager, plugin_name: str) -> Optional[Plugin]:
    if plugin_name.startswith("_"):
        return None

    if plugin_name in plugins:
        return None

    try:
        module = manager.load_plugin(plugin_name)

        plugin = Plugin(plugin_name, module)
        plugins[plugin_name] = plugin
        logger.opt(colors=True).success(
            f'Succeeded to import "<y>{escape_tag(plugin_name)}</y>"')
        return plugin
    except Exception as e:
        logger.opt(colors=True, exception=e).error(
            f'<r><bg #f8bbd0>Failed to import "{escape_tag(plugin_name)}"</bg #f8bbd0></r>'
        )
        return None


def load_plugin(module_path: str) -> Optional[Plugin]:
    """
    :说明:

      使用 ``PluginManager`` 加载单个插件，可以是本地插件或是通过 ``pip`` 安装的插件。

    :参数:

      * ``module_path: str``: 插件名称 ``path.to.your.plugin``

    :返回:

      - ``Optional[Plugin]``
    """

    context: Context = copy_context()
    manager = PluginManager(PLUGIN_NAMESPACE, plugins=[module_path])
    return context.run(_load_plugin, manager, module_path)


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
    manager = PluginManager(PLUGIN_NAMESPACE, search_path=plugin_dir)
    for plugin_name in manager.list_plugins():
        context: Context = copy_context()
        result = context.run(_load_plugin, manager, plugin_name)
        if result:
            loaded_plugins.add(result)
    return loaded_plugins


def load_all_plugins(module_path: Set[str],
                     plugin_dir: Set[str]) -> Set[Plugin]:
    """
    :说明:

      导入指定列表中的插件以及指定目录下多个插件，以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``module_path: Set[str]``: 指定插件集合
      - ``plugin_dir: Set[str]``: 指定插件路径集合

    :返回:

      - ``Set[Plugin]``
    """
    loaded_plugins = set()
    manager = PluginManager(PLUGIN_NAMESPACE, module_path, plugin_dir)
    for plugin_name in manager.list_plugins():
        context: Context = copy_context()
        result = context.run(_load_plugin, manager, plugin_name)
        if result:
            loaded_plugins.add(result)
    return loaded_plugins


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
    assert isinstance(plugin_dirs,
                      list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_from_toml(file_path: str, encoding: str = "utf-8") -> Set[Plugin]:
    """
    :说明:

      导入指定 toml 文件 ``[nonebot.plugins]`` 中的 ``plugins`` 以及 ``plugin_dirs`` 下多个插件，
      以 ``_`` 开头的插件不会被导入！

    :参数:

      - ``file_path: str``: 指定 toml 文件路径
      - ``encoding: str``: 指定 toml 文件编码

    :返回:

      - ``Set[Plugin]``
    """
    with open(file_path, "r", encoding=encoding) as f:
        data = tomlkit.parse(f.read())  # type: ignore

    nonebot_data = data.get("nonebot", {}).get("plugins")
    if not nonebot_data:
        raise ValueError("Cannot find '[nonebot.plugins]' in given toml file!")
    plugins = nonebot_data.get("plugins", [])
    plugin_dirs = nonebot_data.get("plugin_dirs", [])
    assert isinstance(plugins, list), "plugins must be a list of plugin name"
    assert isinstance(plugin_dirs,
                      list), "plugin_dirs must be a list of directories"
    return load_all_plugins(set(plugins), set(plugin_dirs))


def load_builtin_plugins(name: str = "echo") -> Optional[Plugin]:
    """
    :说明:

      导入 NoneBot 内置插件

    :返回:

      - ``Plugin``
    """
    return load_plugin(f"nonebot.plugins.{name}")


def require(name: str) -> Optional[Export]:
    """
    :说明:

      获取一个插件的导出内容

    :参数:

      * ``name: str``: 插件名，与 ``load_plugin`` 参数一致。如果为 ``load_plugins`` 导入的插件，则为文件(夹)名。

    :返回:

      - ``Optional[Export]``
    """
    plugin = get_plugin(name) or load_plugin(name)
    if not plugin:
        raise RuntimeError(f"Cannot load plugin \"{name}\"!")
    return plugin.export
