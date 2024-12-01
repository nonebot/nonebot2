from nonebot import on_message
from nonebot.adapters import Event, Message
from nonebot.matcher import Matcher
from nonebot.params import ArgStr, EventMessage, LastReceived, Received

test_handle = on_message()


@test_handle.handle()
async def handle():
    await test_handle.finish("send", at_sender=True)


test_got = on_message()


@test_got.got("key1", "prompt key1")
@test_got.got("key2", "prompt key2")
async def got(key1: str = ArgStr(), key2: str = ArgStr()):
    if key2 == "text":
        await test_got.reject("reject", at_sender=True)

    assert key1 == "text"
    assert key2 == "text_next"


test_receive = on_message()


@test_receive.receive()
@test_receive.receive("receive")
async def receive(
    x: Event = Received("receive"), y: Event = LastReceived(), z: Event = Received()
):
    assert str(x.get_message()) == "text"
    assert str(z.get_message()) == "text"
    assert x is y
    await test_receive.pause("pause", at_sender=True)


test_combine = on_message()


@test_combine.got("a")
@test_combine.receive()
@test_combine.got("b")
async def combine(a: str = ArgStr(), b: str = ArgStr(), r: Event = Received()):
    if a == "text":
        await test_combine.reject_arg("a")
    elif b == "text":
        await test_combine.reject_arg("b")
    elif str(r.get_message()) == "text":
        await test_combine.reject_receive()

    assert a == "text_next"
    assert b == "text_next"
    assert str(r.get_message()) == "text_next"


test_preset = on_message()


@test_preset.handle()
async def preset(matcher: Matcher, message: Message = EventMessage()):
    matcher.set_arg("a", message)


@test_preset.got("a")
@test_preset.got("b")
async def reject_preset(a: str = ArgStr(), b: str = ArgStr()):
    if a == "text":
        await test_preset.reject_arg("a")

    assert a == "text_next"
    assert b == "text"


test_overload = on_message()


class FakeEvent(Event): ...


@test_overload.got("a")
async def overload(event: FakeEvent):
    await test_overload.reject_arg("a")


@test_overload.handle()
async def finish():
    await test_overload.finish()


test_destroy = on_message()
