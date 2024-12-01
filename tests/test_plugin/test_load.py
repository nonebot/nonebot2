from dataclasses import asdict
from functools import wraps
from pathlib import Path
import sys
from typing import Callable, TypeVar
from typing_extensions import ParamSpec

import pytest

import nonebot
from nonebot.plugin import (
    Plugin,
    PluginManager,
    _managers,
    _plugins,
    inherit_supported_adapters,
)

P = ParamSpec("P")
R = TypeVar("R")


def _recover(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        origin_managers = _managers.copy()
        origin_plugins = _plugins.copy()
        try:
            return func(*args, **kwargs)
        finally:
            _managers.clear()
            _managers.extend(origin_managers)
            _plugins.clear()
            _plugins.update(origin_plugins)

    return _wrapper


@_recover
def test_load_plugin():
    # check regular
    assert nonebot.load_plugin("dynamic.simple")

    # check path
    assert nonebot.load_plugin(Path("dynamic/path.py"))

    # check not found
    assert nonebot.load_plugin("some_plugin_not_exist") is None


def test_load_plugins(load_plugin: set[Plugin], load_builtin_plugin: set[Plugin]):
    loaded_plugins = {
        plugin for plugin in nonebot.get_loaded_plugins() if not plugin.parent_plugin
    }
    assert loaded_plugins >= load_plugin | load_builtin_plugin

    # check simple plugin
    assert "plugins.export" in sys.modules
    assert "plugin._hidden" not in sys.modules

    # check sub plugin
    plugin = nonebot.get_plugin("nested:nested_subplugin")
    assert plugin
    assert "plugins.nested.plugins.nested_subplugin" in sys.modules
    assert plugin.parent_plugin is nonebot.get_plugin("nested")

    # check load again
    with pytest.raises(RuntimeError):
        PluginManager(plugins=["plugins.export"]).load_all_plugins()
    with pytest.raises(RuntimeError):
        PluginManager(search_path=["plugins"]).load_all_plugins()


def test_load_nested_plugin():
    parent_plugin = nonebot.get_plugin("nested")
    sub_plugin = nonebot.get_plugin("nested:nested_subplugin")
    sub_plugin2 = nonebot.get_plugin("nested:nested_subplugin2")
    assert parent_plugin
    assert sub_plugin
    assert sub_plugin2
    assert sub_plugin.parent_plugin is parent_plugin
    assert sub_plugin2.parent_plugin is parent_plugin
    assert parent_plugin.sub_plugins == {sub_plugin, sub_plugin2}


@_recover
def test_load_json():
    nonebot.load_from_json("./plugins.json")

    with pytest.raises(TypeError):
        nonebot.load_from_json("./plugins.invalid.json")


@_recover
def test_load_toml():
    nonebot.load_from_toml("./plugins.toml")

    with pytest.raises(ValueError, match="Cannot find"):
        nonebot.load_from_toml("./plugins.empty.toml")

    with pytest.raises(TypeError):
        nonebot.load_from_toml("./plugins.invalid.toml")


@_recover
def test_bad_plugin():
    nonebot.load_plugins("bad_plugins")

    assert nonebot.get_plugin("bad_plugin") is None


@_recover
def test_require_loaded(monkeypatch: pytest.MonkeyPatch):
    def _patched_find(name: str):
        pytest.fail("require existing plugin should not call find_manager_by_name")

    with monkeypatch.context() as m:
        m.setattr("nonebot.plugin.load._find_manager_by_name", _patched_find)

        # require use module name
        nonebot.require("plugins.export")
        # require use plugin id
        nonebot.require("export")
        nonebot.require("nested:nested_subplugin")


@_recover
def test_require_not_loaded(monkeypatch: pytest.MonkeyPatch):
    pm = PluginManager(["dynamic.require_not_loaded"], ["dynamic/require_not_loaded/"])
    _managers.append(pm)
    num_managers = len(_managers)

    origin_load = PluginManager.load_plugin

    def _patched_load(self: PluginManager, name: str):
        assert self is pm
        return origin_load(self, name)

    with monkeypatch.context() as m:
        m.setattr(PluginManager, "load_plugin", _patched_load)

        # require standalone plugin
        nonebot.require("dynamic.require_not_loaded")
        # require searched plugin
        nonebot.require("dynamic.require_not_loaded.subplugin1")
        nonebot.require("require_not_loaded:subplugin2")

    assert len(_managers) == num_managers


@_recover
def test_require_not_declared():
    num_managers = len(_managers)

    nonebot.require("dynamic.require_not_declared")

    assert len(_managers) == num_managers + 1
    assert _managers[-1].plugins == {"dynamic.require_not_declared"}


@_recover
def test_require_not_found():
    with pytest.raises(RuntimeError):
        nonebot.require("some_plugin_not_exist")


def test_plugin_metadata():
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


def test_inherit_supported_adapters_not_found():
    with pytest.raises(RuntimeError):
        inherit_supported_adapters("some_plugin_not_exist")

    with pytest.raises(ValueError, match="has no metadata!"):
        inherit_supported_adapters("export")


@pytest.mark.parametrize(
    ("inherit_plugins", "expected"),
    [
        (("echo",), None),
        (
            ("metadata",),
            {
                "nonebot.adapters.onebot.v11",
                "plugins.metadata:FakeAdapter",
            },
        ),
        (
            ("metadata_2",),
            {
                "nonebot.adapters.onebot.v11",
                "nonebot.adapters.onebot.v12",
            },
        ),
        (
            ("metadata_3",),
            {
                "nonebot.adapters.onebot.v11",
                "nonebot.adapters.onebot.v12",
                "nonebot.adapters.qq",
            },
        ),
        (
            ("metadata", "metadata_2"),
            {
                "nonebot.adapters.onebot.v11",
            },
        ),
        (
            ("metadata", "metadata_3"),
            {
                "nonebot.adapters.onebot.v11",
            },
        ),
        (
            ("metadata_2", "metadata_3"),
            {
                "nonebot.adapters.onebot.v11",
                "nonebot.adapters.onebot.v12",
            },
        ),
        (
            ("metadata", "metadata_2", "metadata_3"),
            {
                "nonebot.adapters.onebot.v11",
            },
        ),
        (
            ("metadata", "echo"),
            {
                "nonebot.adapters.onebot.v11",
                "plugins.metadata:FakeAdapter",
            },
        ),
        (
            ("metadata", "metadata_2", "echo"),
            {
                "nonebot.adapters.onebot.v11",
            },
        ),
    ],
)
def test_inherit_supported_adapters_combine(
    inherit_plugins: tuple[str], expected: set[str]
):
    assert inherit_supported_adapters(*inherit_plugins) == expected
