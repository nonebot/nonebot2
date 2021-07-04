from nonebot.adapters.feishu.event import MessageEvent
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.feishu import Bot as FeishuBot, MessageSegment, MessageEvent

helper = on_command("114514")


@helper.handle()
async def feishu_helper(bot: FeishuBot, event: MessageEvent):
    message = MessageSegment.text("1919810")
    await helper.finish(message)
