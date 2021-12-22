import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonebug_init",
    [{"driver": "nonebot.drivers.fastapi"}],
    indirect=True,
)
async def test_driver(nonebug_init):
    ...
