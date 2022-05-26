from pathlib import Path

import nonebot

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))
