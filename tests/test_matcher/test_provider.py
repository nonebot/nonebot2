import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_manager(app: App, load_plugin):
    from nonebot.matcher import DEFAULT_PROVIDER_CLASS, matchers

    default_provider = matchers.provider
    matchers.set_provider(DEFAULT_PROVIDER_CLASS)
    assert matchers.provider == default_provider
