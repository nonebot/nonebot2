import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_manager(app: App, load_plugin):
    from nonebot.matcher import DEFAULT_PROVIDER, matchers
    from nonebot.internal.matcher.provider import _DictProvider

    matchers.set_provider(_DictProvider)

    assert matchers.provider == DEFAULT_PROVIDER
