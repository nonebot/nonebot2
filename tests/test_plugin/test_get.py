from pydantic import BaseModel, Field
import pytest

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


def test_get_plugin_config_with_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PLUGIN_CONFIG_ONE", "no_dummy_val")
    monkeypatch.setenv("PLUGIN_SUB_CONFIG__TWO", "two")
    monkeypatch.setenv("PLUGIN_CFG_THREE", "33")
    monkeypatch.setenv("CONFIG_FROM_INIT", "impossible")

    class SubConfig(BaseModel):
        two: str = "dummy_val"

    class Config(BaseModel):
        plugin_config: int
        plugin_config_one: str = "dummy_val"
        plugin_sub_config: SubConfig = Field(default_factory=SubConfig)
        plugin_config_three: int = Field(default=3, alias="plugin_cfg_three")
        config_from_init: str = "dummy_val"

    config = nonebot.get_plugin_config(Config)
    assert config.plugin_config == 1
    assert config.plugin_config_one == "no_dummy_val"
    assert config.plugin_sub_config.two == "two"
    assert config.plugin_config_three == 33
    assert config.config_from_init == "init"
