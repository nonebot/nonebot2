from nonebot.adapters.feishu.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.feishu import Bot as FeishuBot, MessageSegment, MessageEvent

helper = on_command("ding_helper", to_me())


@helper.handle()
async def ding_helper(bot: FeishuBot, event: MessageEvent):
    message = MessageSegment.text("114514")
    await helper.finish(message)
