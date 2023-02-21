import pytest

from nonebot.plugin import PluginManager


@pytest.mark.asyncio
async def test_load_plugin_name():
    m = PluginManager(plugins=["dynamic.manager"])
    module1 = m.load_plugin("manager")
    module2 = m.load_plugin("dynamic.manager")
    assert module1 is module2
