from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.adapters.feishu import MessageEvent
from nonebot.adapters.feishu import Bot as FeishuBot

helper = on_command("say")


@helper.handle()
async def feishu_helper(bot: FeishuBot, event: MessageEvent, state: T_State):
    message = event.get_message()
    await helper.finish(message, at_sender=True)
