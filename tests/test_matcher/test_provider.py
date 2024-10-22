from nonebug import App

from nonebot.matcher import DEFAULT_PROVIDER_CLASS, matchers


def test_manager(app: App):
    try:
        default_provider = matchers.provider
        matchers.set_provider(DEFAULT_PROVIDER_CLASS)
        assert default_provider == matchers.provider
    finally:
        matchers.provider = app.provider
