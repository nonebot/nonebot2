from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent

overload = on_command("overload")


@overload.handle()
async def handle_first_receive(bot: Bot):
    return


@overload.got("message", prompt="群？")
async def handle_group(bot: Bot, event: GroupMessageEvent):
    return


@overload.got("message", prompt="私？")
async def handle_private(bot: Bot, event: PrivateMessageEvent):
    return
