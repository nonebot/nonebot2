from functools import reduce

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import Bot, Event, MessageSegment

say = on_command("say", to_me(), permission=SUPERUSER)


@say.handle()
async def say_unescape(bot: Bot, event: Event, state: dict):
    Message = event.message.__class__

    def _unescape(message: Message, segment: MessageSegment):
        if segment.type == "text":
            return message.append(segment.data["text"])
        return message.append(segment)

    message = reduce(_unescape, event.message, Message())  # type: ignore
    await bot.send(message=message, event=event)


echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(bot: Bot, event: Event, state: dict):
    Message = event.message.__class__
    MessageSegment = event.message[0].__class__

    message = Message().append(  # type: ignore
        MessageSegment.text(str(event.message)))
    await bot.send(message=message, event=event)
