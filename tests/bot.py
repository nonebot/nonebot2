import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import nonebot
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.ding import Bot as DingBot
from nonebot.adapters.mirai import Bot as MiraiBot
from nonebot.log import logger, default_format

# test custom log
logger.add("error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

nonebot.init(custom_config2="config on init")
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot)
driver.register_adapter("ding", DingBot)
driver.register_adapter("mirai", MiraiBot)

# load builtin plugin
nonebot.load_builtin_plugins()
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_test")

# load local plugins
nonebot.load_plugins("test_plugins")

# modify some config / config depends on loaded configs
config = driver.config
config.custom_config3 = config.custom_config1
config.custom_config4 = "New custom config"

if __name__ == "__main__":
    nonebot.run(app="bot:app")
