from nonebot import require

from plugins.export import test
from .export import test as test_related

test_require = require("export").test

assert test is test_related and test is test_require, "Export Require Error"
