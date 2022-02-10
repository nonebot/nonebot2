import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_weather(app: App):
    from examples.weather import weather
    from utils import make_fake_event, make_fake_message

    # 将此处的 make_fake_message() 替换为你要发送的平台消息 Message 类型
    Message = make_fake_message()

    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()

        msg = Message("/天气 上海")
        # 将此处的 make_fake_event() 替换为你要发送的平台事件 Event 类型
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "上海的天气是...", True)
        ctx.should_finished()

    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()

        msg = Message("/天气 南京")
        # 将此处的 make_fake_event() 替换为你要发送的平台事件 Event 类型
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            Message.template("你想查询的城市 {} 暂不支持，请重新输入！").format("南京"),
            True,
        )
        ctx.should_rejected()

        msg = Message("北京")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "北京的天气是...", True)
        ctx.should_finished()

    async with app.test_matcher(weather) as ctx:
        bot = ctx.create_bot()

        msg = Message("/天气")
        # 将此处的 make_fake_event() 替换为你要发送的平台事件 Event 类型
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "你想查询哪个城市的天气呢？", True)

        msg = Message("杭州")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            Message.template("你想查询的城市 {} 暂不支持，请重新输入！").format("杭州"),
            True,
        )
        ctx.should_rejected()

        msg = Message("北京")
        event = make_fake_event(_message=msg)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "北京的天气是...", True)
        ctx.should_finished()
