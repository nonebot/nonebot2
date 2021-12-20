from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import ArgStr, Received, LastReceived

test_handle = on_message()


@test_handle.handle()
async def handle():
    await test_handle.finish("send", at_sender=True)


test_got = on_message()


@test_got.got("key1", "prompt key1")
@test_got.got("key2", "prompt key2")
async def got(key1: str = ArgStr(), key2: str = ArgStr()):
    assert key1 == "text"
    assert key2 == "text"
    await test_got.reject("reject", at_sender=True)


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
