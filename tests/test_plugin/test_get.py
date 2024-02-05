import pytest
from pydantic import BaseModel

import nonebot
from nonebot.plugin import PluginManager, _managers


@pytest.mark.asyncio
async def test_get_plugin():
    # check simple plugin
    plugin = nonebot.get_plugin("export")
    assert plugin
    assert plugin.module_name == "plugins.export"

    # check sub plugin
    plugin = nonebot.get_plugin("nested_subplugin")
    assert plugin
    assert plugin.module_name == "plugins.nested.plugins.nested_subplugin"

    # check get plugin by module name
    plugin = nonebot.get_plugin_by_module_name("plugins.nested.utils")
    assert plugin
    assert plugin.module_name == "plugins.nested"


@pytest.mark.asyncio
async def test_get_available_plugin():
    old_managers = _managers.copy()
    _managers.clear()
    try:
        _managers.append(PluginManager(["plugins.export", "plugin.require"]))

        # check get available plugins
        plugin_names = nonebot.get_available_plugin_names()
        assert plugin_names == {"export", "require"}
    finally:
        _managers.clear()
        _managers.extend(old_managers)


@pytest.mark.asyncio
async def test_get_plugin_config():
    class Config(BaseModel):
        plugin_config: int

    # check get plugin config
    config = nonebot.get_plugin_config(Config)
    assert isinstance(config, Config)
    assert config.plugin_config == 1
