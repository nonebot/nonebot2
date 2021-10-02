from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageSegment, GroupMessageEvent

template = on_command("template")


@template.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    state["at"] = MessageSegment.at(event.get_user_id())
    state["test"] = "test"
    # message: /template {at} hello {test}!
    ft = event.message.template(event.message)
    await template.send(ft)
