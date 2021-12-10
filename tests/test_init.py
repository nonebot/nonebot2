import os

import pytest

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
