import pytest
from nonebug import App

from utils import make_fake_event


@pytest.mark.asyncio
async def test_permission(app: App):
    from nonebot.permission import Permission
    from nonebot.exception import SkippedException

    async def falsy():
        return False

    async def truthy():
        return True

    async def skipped() -> bool:
        raise SkippedException

    def _is_eq(a: Permission, b: Permission) -> bool:
        return {d.call for d in a.checkers} == {d.call for d in b.checkers}

    assert _is_eq(Permission(truthy) | None, Permission(truthy))
    assert _is_eq(Permission(truthy) | falsy, Permission(truthy, falsy))
    assert _is_eq(Permission(truthy) | Permission(falsy), Permission(truthy, falsy))

    assert _is_eq(None | Permission(truthy), Permission(truthy))
    assert _is_eq(truthy | Permission(falsy), Permission(truthy, falsy))

    event = make_fake_event()()

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert await Permission(falsy)(bot, event) == False
        assert await Permission(truthy)(bot, event) == True
        assert await Permission(skipped)(bot, event) == False
        assert await Permission(truthy, falsy)(bot, event) == True
        assert await Permission(truthy, skipped)(bot, event) == True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type,expected",
    [
        ("message", True),
        ("notice", False),
    ],
)
async def test_message(
    app: App,
    type: str,
    expected: bool,
):
    from nonebot.permission import MESSAGE, Message

    dependent = list(MESSAGE.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, Message)

    event = make_fake_event(_type=type)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type,expected",
    [
        ("message", False),
        ("notice", True),
    ],
)
async def test_notice(
    app: App,
    type: str,
    expected: bool,
):
    from nonebot.permission import NOTICE, Notice

    dependent = list(NOTICE.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, Notice)

    event = make_fake_event(_type=type)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type,expected",
    [
        ("message", False),
        ("request", True),
    ],
)
async def test_request(
    app: App,
    type: str,
    expected: bool,
):
    from nonebot.permission import REQUEST, Request

    dependent = list(REQUEST.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, Request)

    event = make_fake_event(_type=type)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type,expected",
    [
        ("message", False),
        ("meta_event", True),
    ],
)
async def test_metaevent(
    app: App,
    type: str,
    expected: bool,
):
    from nonebot.permission import METAEVENT, MetaEvent

    dependent = list(METAEVENT.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, MetaEvent)

    event = make_fake_event(_type=type)()
    assert await dependent(event=event) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type,user_id,expected",
    [
        ("message", "test", True),
        ("message", "foo", False),
        ("message", "faketest", True),
        ("notice", "test", False),
    ],
)
async def test_startswith(
    app: App,
    type: str,
    user_id: str,
    expected: bool,
):
    from nonebot.permission import SUPERUSER, SuperUser

    dependent = list(SUPERUSER.checkers)[0]
    checker = dependent.call

    assert isinstance(checker, SuperUser)

    event = make_fake_event(_type=type, _user_id=user_id)()

    async with app.test_api() as ctx:
        bot = ctx.create_bot()
        assert await dependent(bot=bot, event=event) == expected
