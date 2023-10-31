import sys
from typing import Set
from pathlib import Path
from dataclasses import asdict

import pytest

import nonebot
from nonebot.plugin import Plugin, PluginManager, _managers, inherit_supported_adapters


@pytest.mark.asyncio
async def test_load_plugin():
    # check regular
    assert nonebot.load_plugin("dynamic.simple")

    # check path
    assert nonebot.load_plugin(Path("dynamic/path.py"))

    # check not found
    assert nonebot.load_plugin("some_plugin_not_exist") is None


@pytest.mark.asyncio
async def test_load_plugins(load_plugin: Set[Plugin], load_builtin_plugin: Set[Plugin]):
    loaded_plugins = {
        plugin for plugin in nonebot.get_loaded_plugins() if not plugin.parent_plugin
    }
    assert loaded_plugins >= load_plugin | load_builtin_plugin

    # check simple plugin
    assert "plugins.export" in sys.modules

    # check sub plugin
    plugin = nonebot.get_plugin("nested_subplugin")
    assert plugin
    assert "plugins.nested.plugins.nested_subplugin" in sys.modules
    assert plugin.parent_plugin == nonebot.get_plugin("nested")

    # check load again
    with pytest.raises(RuntimeError):
        PluginManager(plugins=["plugins.export"]).load_all_plugins()
    with pytest.raises(RuntimeError):
        PluginManager(search_path=["plugins"]).load_all_plugins()


@pytest.mark.asyncio
async def test_load_nested_plugin():
    parent_plugin = nonebot.get_plugin("nested")
    sub_plugin = nonebot.get_plugin("nested_subplugin")
    sub_plugin2 = nonebot.get_plugin("nested_subplugin2")
    assert parent_plugin
    assert sub_plugin
    assert sub_plugin2
    assert sub_plugin.parent_plugin is parent_plugin
    assert sub_plugin2.parent_plugin is parent_plugin
    assert parent_plugin.sub_plugins == {sub_plugin, sub_plugin2}


@pytest.mark.asyncio
async def test_load_json():
    nonebot.load_from_json("./plugins.json")

    with pytest.raises(TypeError):
        nonebot.load_from_json("./plugins.invalid.json")


@pytest.mark.asyncio
async def test_load_toml():
    nonebot.load_from_toml("./plugins.toml")

    with pytest.raises(ValueError, match="Cannot find"):
        nonebot.load_from_toml("./plugins.empty.toml")

    with pytest.raises(TypeError):
        nonebot.load_from_toml("./plugins.invalid.toml")


@pytest.mark.asyncio
async def test_bad_plugin():
    nonebot.load_plugins("bad_plugins")

    assert nonebot.get_plugin("bad_plugin") is None


@pytest.mark.asyncio
async def test_require_loaded(monkeypatch: pytest.MonkeyPatch):
    def _patched_find(name: str):
        pytest.fail("require existing plugin should not call find_manager_by_name")

    monkeypatch.setattr("nonebot.plugin.load._find_manager_by_name", _patched_find)

    nonebot.require("plugins.export")


@pytest.mark.asyncio
async def test_require_not_loaded(monkeypatch: pytest.MonkeyPatch):
    m = PluginManager(["dynamic.require_not_loaded"])
    _managers.append(m)
    num_managers = len(_managers)

    origin_load = PluginManager.load_plugin

    def _patched_load(self: PluginManager, name: str):
        assert self is m
        return origin_load(self, name)

    monkeypatch.setattr(PluginManager, "load_plugin", _patched_load)

    nonebot.require("dynamic.require_not_loaded")

    assert len(_managers) == num_managers


@pytest.mark.asyncio
async def test_require_not_declared():
    num_managers = len(_managers)

    nonebot.require("dynamic.require_not_declared")

    assert len(_managers) == num_managers + 1
    assert _managers[-1].plugins == {"dynamic.require_not_declared"}


@pytest.mark.asyncio
async def test_require_not_found():
    with pytest.raises(RuntimeError):
        nonebot.require("some_plugin_not_exist")


@pytest.mark.asyncio
async def test_plugin_metadata():
    from plugins.metadata import Config, FakeAdapter

    plugin = nonebot.get_plugin("metadata")
    assert plugin
    assert plugin.metadata
    assert asdict(plugin.metadata) == {
        "name": "测试插件",
        "description": "测试插件元信息",
        "usage": "无法使用",
        "type": "application",
        "homepage": "https://nonebot.dev",
        "config": Config,
        "supported_adapters": {"~onebot.v11", "plugins.metadata:FakeAdapter"},
        "extra": {"author": "NoneBot"},
    }

    assert plugin.metadata.get_supported_adapters() == {FakeAdapter}


@pytest.mark.asyncio
async def test_inherit_supported_adapters():
    with pytest.raises(RuntimeError):
        inherit_supported_adapters("some_plugin_not_exist")

    with pytest.raises(ValueError, match="has no metadata!"):
        inherit_supported_adapters("export")

    echo = nonebot.get_plugin("echo")
    assert echo
    assert echo.metadata
    assert inherit_supported_adapters("echo") is None

    plugin_1 = nonebot.get_plugin("metadata")
    assert plugin_1
    assert plugin_1.metadata
    assert inherit_supported_adapters("metadata") == {
        "nonebot.adapters.onebot.v11",
        "plugins.metadata:FakeAdapter",
    }

    plugin_2 = nonebot.get_plugin("metadata_2")
    assert plugin_2
    assert plugin_2.metadata
    assert inherit_supported_adapters("metadata", "metadata_2") == {
        "nonebot.adapters.onebot.v11"
    }
    assert inherit_supported_adapters("metadata", "echo", "metadata_2") == {
        "nonebot.adapters.onebot.v11"
    }
