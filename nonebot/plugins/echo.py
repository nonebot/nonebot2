from functools import reduce

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import (Message, MessageEvent, MessageSegment,
                                     unescape)

say = on_command("say", to_me(), permission=SUPERUSER)


@say.handle()
async def say_unescape(event: MessageEvent):

    def _unescape(message: Message, segment: MessageSegment):
        if segment.is_text():
            return message.append(unescape(str(segment)))
        return message.append(segment)

    message = reduce(_unescape, event.get_message(), Message())  # type: ignore
    await say.send(message=message)


echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape(event: MessageEvent):
    await say.send(message=event.get_message())
