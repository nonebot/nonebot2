from pathlib import Path

from nonebot import load_plugins

_sub_plugins = set()

_sub_plugins |= load_plugins(str(Path(__file__).parent))
