import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_load_plugin_name(app: App):
    from nonebot.plugin import PluginManager

    m = PluginManager(plugins=["plugins.export"])
    module1 = m.load_plugin("export")
    module2 = m.load_plugin("plugins.export")
    assert module1 is module2
