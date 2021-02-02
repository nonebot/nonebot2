from nonebot.plugin import on_message
from nonebot.adapters.mirai import Bot, MessageEvent

message_test = on_message()


@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    if not text:
        return
    reversed_text = ''.join(reversed(text))
    await bot.send(event, reversed_text, at_sender=True)
