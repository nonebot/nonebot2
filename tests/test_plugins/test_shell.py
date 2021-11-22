from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot import on_shell_command
from nonebot.rule import ArgumentParser, to_me

parser = ArgumentParser()
parser.add_argument("-a", action="store_true")

shell = on_shell_command("ls", to_me(), parser=parser)


@shell.handle()
async def _(bot: Bot, state: T_State):
    print(state["argv"])
    print(state["args"])
