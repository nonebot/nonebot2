from nonebot import require

test_require = require("export").test

from plugins.export import test

assert test is test_require, "Export Require Error"
assert test() == "export", "Export Require Error"
