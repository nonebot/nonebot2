#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快捷导入
========

为方便使用，``nonebot`` 模块从子模块导入了部分内容

- ``on_message`` => ``nonebot.plugin.on_message``
- ``on_notice`` => ``nonebot.plugin.on_notice``
- ``on_request`` => ``nonebot.plugin.on_request``
- ``on_metaevent`` => ``nonebot.plugin.on_metaevent``
- ``on_startswith`` => ``nonebot.plugin.on_startswith``
- ``on_endswith`` => ``nonebot.plugin.on_endswith``
- ``on_command`` => ``nonebot.plugin.on_command``
- ``on_regex`` => ``nonebot.plugin.on_regex``
- ``on_regex`` => ``nonebot.plugin.on_regex``
- ``on_regex`` => ``nonebot.plugin.on_regex``
- ``CommandGroup`` => ``nonebot.plugin.CommandGroup``
- ``load_plugin`` => ``nonebot.plugin.load_plugin``
- ``load_plugins`` => ``nonebot.plugin.load_plugins``
- ``load_builtin_plugins`` => ``nonebot.plugin.load_builtin_plugins``
- ``get_loaded_plugins`` => ``nonebot.plugin.get_loaded_plugins``
"""

import importlib
from nonebot.typing import Bot, Dict, Type, Union, Driver, Optional, NoReturn

_driver: Optional[Driver] = None


def get_driver() -> Union[NoReturn, Driver]:
    """
    :说明:

      获取全局 Driver 对象。可用于在计划任务的回调中获取当前 Driver 对象。

    :返回:

      * ``Driver``: 全局 Driver 对象

    :异常:

      * ``ValueError``: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)

    :用法:

    .. code-block:: python

        driver = nonebot.get_driver()

    """
    if _driver is None:
        raise ValueError("NoneBot has not been initialized.")
    return _driver


def get_app():
    """
    :说明:

      获取全局 Driver 对应 Server App 对象。

    :返回:

      * ``Any``: Server App 对象

    :异常:

      * ``ValueError``: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)

    :用法:

    .. code-block:: python

        app = nonebot.get_app()

    """
    driver = get_driver()
    return driver.server_app


def get_asgi():
    """
    :说明:

      获取全局 Driver 对应 Asgi 对象。

    :返回:

      * ``Any``: Asgi 对象

    :异常:

      * ``ValueError``: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)

    :用法:

    .. code-block:: python

        asgi = nonebot.get_asgi()

    """
    driver = get_driver()
    return driver.asgi


def get_bots() -> Union[NoReturn, Dict[str, Bot]]:
    """
    :说明:

      获取所有通过 ws 连接 NoneBot 的 Bot 对象。

    :返回:

      * ``Dict[str, Bot]``: 一个以字符串 ID 为键，Bot 对象为值的字典

    :异常:

      * ``ValueError``: 全局 Driver 对象尚未初始化 (nonebot.init 尚未调用)

    :用法:

    .. code-block:: python

        bots = nonebot.get_bots()

    """
    driver = get_driver()
    return driver.bots


from nonebot.sched import scheduler
from nonebot.utils import escape_tag
from nonebot.config import Env, Config
from nonebot.log import logger, default_filter
from nonebot.adapters.cqhttp import Bot as CQBot

try:
    import nonebot_test
except ImportError:
    nonebot_test = None


def init(*, _env_file: Optional[str] = None, **kwargs):
    """
    :说明:

      初始化 NoneBot 以及 全局 Driver 对象。

      NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。

      你也可以传入自定义的 _env_file 来指定 NoneBot 从该文件读取配置。

    :参数:

      * ``_env_file: Optional[str]``: 配置文件名，默认从 .env.{env_name} 中读取配置
      * ``**kwargs``: 任意变量，将会存储到 Config 对象里

    :返回:

      - ``None``

    :用法:

    .. code-block:: python

        nonebot.init(database=Database(...))

    """
    global _driver
    if not _driver:
        logger.info("NoneBot is initializing...")
        env = Env()
        logger.opt(
            colors=True).info(f"Current <y><b>Env: {env.environment}</b></y>")
        config = Config(**kwargs,
                        _env_file=_env_file or f".env.{env.environment}")

        default_filter.level = "DEBUG" if config.debug else "INFO"
        logger.opt(colors=True).debug(
            f"Loaded <y><b>Config</b></y>: {escape_tag(str(config.dict()))}")

        DriverClass: Type[Driver] = getattr(
            importlib.import_module(config.driver), "Driver")
        _driver = DriverClass(env, config)

        # register build-in adapters
        _driver.register_adapter("cqhttp", CQBot)

        # load nonebot test frontend if debug
        if config.debug and nonebot_test:
            logger.debug("Loading nonebot test frontend...")
            nonebot_test.init()

    if scheduler:
        _driver.on_startup(_start_scheduler)


def run(host: Optional[str] = None,
        port: Optional[int] = None,
        *args,
        **kwargs):
    """
    :说明:

      启动 NoneBot，即运行全局 Driver 对象。

    :参数:

      * ``host: Optional[str]``: 主机名／IP，若不传入则使用配置文件中指定的值
      * ``port: Optional[int]``: 端口，若不传入则使用配置文件中指定的值
      * ``*args``: 传入 Driver.run 的位置参数
      * ``**kwargs``: 传入 Driver.run 的命名参数

    :返回:

      - ``None``

    :用法:

    .. code-block:: python

        nonebot.run(host="127.0.0.1", port=8080)

    """
    logger.info("Running NoneBot...")
    get_driver().run(host, port, *args, **kwargs)


async def _start_scheduler():
    if scheduler and not scheduler.running:
        scheduler.configure(_driver.config.apscheduler_config)
        scheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")


from nonebot.plugin import on_message, on_notice, on_request, on_metaevent
from nonebot.plugin import on_startswith, on_endswith, on_command, on_regex, CommandGroup
from nonebot.plugin import load_plugin, load_plugins, load_builtin_plugins, get_loaded_plugins
