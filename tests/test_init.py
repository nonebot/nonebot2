import os
import sys
from typing import TYPE_CHECKING, Set

import pytest
from utils import load_plugin

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

os.environ["CONFIG_FROM_ENV"] = "env"


@pytest.mark.asyncio
@pytest.mark.parametrize("nonebug_init", [{"config_from_init": "init"}], indirect=True)
async def test_init(nonebug_init):
    from nonebot import get_driver

    env = get_driver().env
    assert env == "test"

    config = get_driver().config
    assert config.config_from_env == "env"
    assert config.config_from_init == "init"
    assert config.common_config == "common"


@pytest.mark.asyncio
async def test_load_plugin(load_plugin: Set["Plugin"]):
    import nonebot

    assert nonebot.get_loaded_plugins() == load_plugin
    plugin = nonebot.get_plugin("depends")
    assert plugin
    assert plugin.module_name == "plugins.depends"
    assert "plugins.depends" in sys.modules
