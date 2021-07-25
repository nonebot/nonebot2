from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent

message_test = on_keyword({'reply'}, rule=to_me())


@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)


command_test = on_command('miecho')


@command_test.handle()
async def _echo(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)