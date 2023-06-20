import importlib

import nonebot
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="NoneBot 离线文档",
    description="在本地查看 NoneBot 文档",
    usage="启动机器人后访问 http://localhost:port/website/ 查看文档",
    type="application",
    homepage="https://github.com/nonebot/nonebot2/blob/master/packages/nonebot-plugin-docs",
    config=None,
    supported_adapters=None,
)


def init():
    driver = nonebot.get_driver()
    try:
        _module = importlib.import_module(
            f"nonebot_plugin_docs.drivers.{driver.type.split('+')[0]}"
        )
    except ImportError:
        logger.warning(f"Driver {driver.type} not supported")
        return
    register_route = getattr(_module, "register_route")
    register_route(driver)
    host = str(driver.config.host)
    port = driver.config.port
    if host in {"0.0.0.0", "127.0.0.1"}:
        host = "localhost"
    logger.opt(colors=True).info(
        f"Nonebot docs will be running at: "
        f"<b><u>http://{host}:{port}/website/</u></b>"
    )


init()
