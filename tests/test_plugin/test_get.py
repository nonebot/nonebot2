from pydantic import BaseModel

import nonebot
from nonebot.plugin import PluginManager, _managers


def test_get_plugin():
    # check simple plugin
    plugin = nonebot.get_plugin("export")
    assert plugin
    assert plugin.id_ == "export"
    assert plugin.name == "export"
    assert plugin.module_name == "plugins.export"

    # check sub plugin
    plugin = nonebot.get_plugin("nested:nested_subplugin")
    assert plugin
    assert plugin.id_ == "nested:nested_subplugin"
    assert plugin.name == "nested_subplugin"
    assert plugin.module_name == "plugins.nested.plugins.nested_subplugin"


def test_get_plugin_by_module_name():
    # check get plugin by exact module name
    plugin = nonebot.get_plugin_by_module_name("plugins.nested")
    assert plugin
    assert plugin.id_ == "nested"
    assert plugin.name == "nested"
    assert plugin.module_name == "plugins.nested"

    # check get plugin by sub module name
    plugin = nonebot.get_plugin_by_module_name("plugins.nested.utils")
    assert plugin
    assert plugin.id_ == "nested"
    assert plugin.name == "nested"
    assert plugin.module_name == "plugins.nested"

    # check get plugin by sub plugin exact module name
    plugin = nonebot.get_plugin_by_module_name(
        "plugins.nested.plugins.nested_subplugin"
    )
    assert plugin
    assert plugin.id_ == "nested:nested_subplugin"
    assert plugin.name == "nested_subplugin"
    assert plugin.module_name == "plugins.nested.plugins.nested_subplugin"


def test_get_available_plugin():
    old_managers = _managers.copy()
    _managers.clear()
    try:
        _managers.append(PluginManager(["plugins.export", "plugin.require"]))

        # check get available plugins
        plugin_ids = nonebot.get_available_plugin_names()
        assert plugin_ids == {"export", "require"}
    finally:
        _managers.clear()
        _managers.extend(old_managers)


def test_get_plugin_config():
    class Config(BaseModel):
        plugin_config: int

    # check get plugin config
    config = nonebot.get_plugin_config(Config)
    assert isinstance(config, Config)
    assert config.plugin_config == 1
