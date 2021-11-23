from nonebot.rule import to_me
from nonebot import CommandGroup, MatcherGroup

cmd = CommandGroup("test", rule=to_me())
match = MatcherGroup(priority=2)

from . import commands
