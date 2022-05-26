from typing import TYPE_CHECKING, Set

import pytest
from nonebug import App

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


@pytest.mark.asyncio
async def test_get_plugin(app: App, load_plugin: Set["Plugin"]):
    import nonebot

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
async def test_get_available_plugin(app: App):
    import nonebot
    from nonebot.plugin import PluginManager, _managers

    _managers.append(PluginManager(["plugins.export", "plugin.require"]))

    # check get available plugins
    plugin_names = nonebot.get_available_plugin_names()
    assert plugin_names == {"export", "require"}
