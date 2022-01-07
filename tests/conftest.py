from pathlib import Path
from typing import TYPE_CHECKING, Set

import pytest

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


@pytest.fixture
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    import nonebot

    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))


@pytest.fixture
def load_example(nonebug_init: None) -> Set["Plugin"]:
    import nonebot

    return nonebot.load_plugins(str(Path(__file__).parent / "examples"))
