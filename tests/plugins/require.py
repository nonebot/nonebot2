from nonebot import require

require("export")

from plugins.export import test

assert test() == "export", "Require should work!"
