from nonebot.rule import to_me
from nonebot import CommandGroup

test = CommandGroup("test", rule=to_me())

from . import commands
