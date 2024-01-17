import pytest

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
async def test_get_plugin_by_id():
    # check simple plugin
    plugin = nonebot.get_plugin(("export",))
    assert plugin
    assert plugin.module_name == "plugins.export"

    # check sub plugin
    plugin = nonebot.get_plugin(("nested",))
    assert plugin
    assert plugin.module_name == "plugins.nested"

    plugin = nonebot.get_plugin(("nested", "nested_subplugin"))
    assert plugin
    assert plugin.module_name == "plugins.nested.plugins.nested_subplugin"

    plugin = nonebot.get_plugin(("nested", "nested_subplugin2"))
    assert plugin
    assert plugin.module_name == "plugins.nested.plugins.nested_subplugin2"


@pytest.mark.asyncio
async def test_get_available_plugin():
    old_managers = _managers.copy()
    _managers.clear()
    try:
        _managers.append(PluginManager(["plugins.export", "plugin.require"]))

        # check get available plugins
        plugin_names = nonebot.get_available_plugin_names()
        assert plugin_names == {"export", "require"}
        # check get available plugins' id
        plugin_fullpaths = nonebot.get_available_plugin_fullpaths()
        assert plugin_fullpaths == {("export",), ("require",)}
    finally:
        _managers.clear()
        _managers.extend(old_managers)
