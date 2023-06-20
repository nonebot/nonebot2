from pathlib import Path

from nonebot.plugin import PluginManager, _managers

manager = PluginManager(
    search_path=[str((Path(__file__).parent / "plugins").resolve())]
)
_managers.append(manager)

# test load nested plugin with require
manager.load_plugin("nested_subplugin")
manager.load_plugin("nested_subplugin2")
