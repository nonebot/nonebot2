from contextlib import asynccontextmanager

import pytest

from utils import make_fake_event


@pytest.mark.asyncio
async def test_matcher_mutex():
    from nonebot.plugins.single_session import matcher_mutex, _running_matcher

    am = asynccontextmanager(matcher_mutex)
    event = make_fake_event()()
    event_1 = make_fake_event()()
    event_2 = make_fake_event(_session_id="test1")()
    event_3 = make_fake_event(_session_id=None)()

    async with am(event) as ctx:
        assert ctx is False
    assert not _running_matcher

    async with am(event) as ctx:
        async with am(event_1) as ctx_1:
            assert ctx is False
            assert ctx_1 is True
    assert not _running_matcher

    async with am(event) as ctx:
        async with am(event_2) as ctx_2:
            assert ctx is False
            assert ctx_2 is False
    assert not _running_matcher

    async with am(event_3) as ctx_3:
        assert ctx_3 is False
    assert not _running_matcher
