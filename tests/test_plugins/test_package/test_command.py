from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.adapters import Bot, Event

test_command = on_command("帮助", to_me())


@test_command.handle()
async def test_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    print("[!] Command:", state["_prefix"], "Args:", args)
    if args:
        state["help"] = args
    else:
        await bot.send(message="命令:\n1. test1\n2. test2", event=event)


@test_command.got("help", prompt="你要帮助的命令是？")
async def test_handler(bot: Bot, event: Event, state: T_State):
    print("[!] Command 帮助:", state["help"])
    if state["help"] not in ["test1", "test2"]:
        await test_command.reject(f"{state['help']} 不支持，请重新输入！")
    await bot.send(message=f"{state['help']} 帮助:\n...", event=event)
