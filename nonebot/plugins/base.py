from functools import reduce

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, unescape, MessageEvent, Message, MessageSegment

say = on_command("say", to_me(), permission=SUPERUSER)


@say.handle()
async def say_unescape(bot: Bot, event: MessageEvent):

    def _unescape(message: Message, segment: MessageSegment):
        if segment.is_text():
            return message.append(unescape(str(segment)))
        return message.append(segment)

    message = reduce(_unescape, event.get_message(), Message())  # type: ignore
    await bot.send(message=message, event=event)


echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(bot: Bot, event: MessageEvent):
    await bot.send(message=event.get_message(), event=event)
