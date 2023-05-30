import os
from pathlib import Path
from typing import TYPE_CHECKING, Set

import pytest
from nonebug import NONEBOT_INIT_KWARGS

import nonebot

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'
os.environ["CONFIG_OVERRIDE"] = "new"

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"config_from_init": "init"}


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))


@pytest.fixture(scope="session", autouse=True)
def load_builtin_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload builtin plugins
    return nonebot.load_builtin_plugins("echo", "single_session")
