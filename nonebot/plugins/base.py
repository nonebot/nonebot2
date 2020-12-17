from functools import reduce

from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot, Event, Message, MessageSegment

say = on_command("say", to_me(), permission=SUPERUSER)


@say.handle()
async def say_unescape(bot: Bot, event: Event, state: T_State):
    MessageImpl = event.get_message().__class__

    def _unescape(message: Message, segment: MessageSegment):
        if segment.is_text():
            return message.append(str(segment))
        return message.append(segment)

    message = reduce(_unescape, event.get_message(), MessageImpl())
    await bot.send(message=message, event=event)


echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(bot: Bot, event: Event, state: T_State):
    await bot.send(message=event.get_message(), event=event)
