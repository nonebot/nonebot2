"""本模块主要定义了 NoneBot 启动所需函数，供 bot 入口文件调用。

## 快捷导入

为方便使用，本模块从子模块导入了部分内容，以下内容可以直接通过本模块导入:

- `on` => {ref}``on` <nonebot.plugin.on.on>`
- `on_metaevent` => {ref}``on_metaevent` <nonebot.plugin.on.on_metaevent>`
- `on_message` => {ref}``on_message` <nonebot.plugin.on.on_message>`
- `on_notice` => {ref}``on_notice` <nonebot.plugin.on.on_notice>`
- `on_request` => {ref}``on_request` <nonebot.plugin.on.on_request>`
- `on_startswith` => {ref}``on_startswith` <nonebot.plugin.on.on_startswith>`
- `on_endswith` => {ref}``on_endswith` <nonebot.plugin.on.on_endswith>`
- `on_fullmatch` => {ref}``on_fullmatch` <nonebot.plugin.on.on_fullmatch>`
- `on_keyword` => {ref}``on_keyword` <nonebot.plugin.on.on_keyword>`
- `on_command` => {ref}``on_command` <nonebot.plugin.on.on_command>`
- `on_shell_command` => {ref}``on_shell_command` <nonebot.plugin.on.on_shell_command>`
- `on_regex` => {ref}``on_regex` <nonebot.plugin.on.on_regex>`
- `on_type` => {ref}``on_type` <nonebot.plugin.on.on_type>`
- `CommandGroup` => {ref}``CommandGroup` <nonebot.plugin.on.CommandGroup>`
- `Matchergroup` => {ref}``MatcherGroup` <nonebot.plugin.on.MatcherGroup>`
- `load_plugin` => {ref}``load_plugin` <nonebot.plugin.load.load_plugin>`
- `load_plugins` => {ref}``load_plugins` <nonebot.plugin.load.load_plugins>`
- `load_all_plugins` => {ref}``load_all_plugins` <nonebot.plugin.load.load_all_plugins>`
- `load_from_json` => {ref}``load_from_json` <nonebot.plugin.load.load_from_json>`
- `load_from_toml` => {ref}``load_from_toml` <nonebot.plugin.load.load_from_toml>`
- `load_builtin_plugin` =>
  {ref}``load_builtin_plugin` <nonebot.plugin.load.load_builtin_plugin>`
- `load_builtin_plugins` =>
  {ref}``load_builtin_plugins` <nonebot.plugin.load.load_builtin_plugins>`
- `get_plugin` => {ref}``get_plugin` <nonebot.plugin.get_plugin>`
- `get_plugin_by_module_name` =>
  {ref}``get_plugin_by_module_name` <nonebot.plugin.get_plugin_by_module_name>`
- `get_loaded_plugins` =>
  {ref}``get_loaded_plugins` <nonebot.plugin.get_loaded_plugins>`
- `get_available_plugin_names` =>
  {ref}``get_available_plugin_names` <nonebot.plugin.get_available_plugin_names>`
- `get_plugin_config` => {ref}``get_plugin_config` <nonebot.plugin.get_plugin_config>`
- `require` => {ref}``require` <nonebot.plugin.load.require>`

FrontMatter:
    mdx:
        format: md
    sidebar_position: 0
    description: nonebot 模块
"""

from importlib.metadata import version
import os
from typing import Any, Optional, TypeVar, Union, overload

import loguru

from nonebot.adapters import Adapter, Bot
from nonebot.compat import model_dump
from nonebot.config import DOTENV_TYPE, Config, Env
from nonebot.drivers import ASGIMixin, Driver, combine_driver
from nonebot.log import logger as logger
from nonebot.utils import escape_tag, resolve_dot_notation

try:
    __version__ = version("nonebot2")
except Exception:  # pragma: no cover
    __version__ = None

A = TypeVar("A", bound=Adapter)

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """获取全局 {ref}`nonebot.drivers.Driver` 实例。

    可用于在计划任务的回调等情形中获取当前 {ref}`nonebot.drivers.Driver` 实例。

    返回:
        全局 {ref}`nonebot.drivers.Driver` 对象

    异常:
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        driver = nonebot.get_driver()
        ```
    """
    if _driver is None:
        raise ValueError("NoneBot has not been initialized.")
    return _driver


@overload
def get_adapter(name: str) -> Adapter:
    """
    参数:
        name: 适配器名称

    返回:
        指定名称的 {ref}`nonebot.adapters.Adapter` 对象
    """


@overload
def get_adapter(name: type[A]) -> A:
    """
    参数:
        name: 适配器类型

    返回:
        指定类型的 {ref}`nonebot.adapters.Adapter` 对象
    """


def get_adapter(name: Union[str, type[Adapter]]) -> Adapter:
    """获取已注册的 {ref}`nonebot.adapters.Adapter` 实例。

    异常:
        ValueError: 指定的 {ref}`nonebot.adapters.Adapter` 未注册
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        from nonebot.adapters.console import Adapter
        adapter = nonebot.get_adapter(Adapter)
        ```
    """
    adapters = get_adapters()
    target = name if isinstance(name, str) else name.get_name()
    if target not in adapters:
        raise ValueError(f"Adapter {target} not registered.")
    return adapters[target]


def get_adapters() -> dict[str, Adapter]:
    """获取所有已注册的 {ref}`nonebot.adapters.Adapter` 实例。

    返回:
        所有 {ref}`nonebot.adapters.Adapter` 实例字典

    异常:
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        adapters = nonebot.get_adapters()
        ```
    """
    return get_driver()._adapters.copy()


def get_app() -> Any:
    """获取全局 {ref}`nonebot.drivers.ASGIMixin` 对应的 Server App 对象。

    返回:
        Server App 对象

    异常:
        AssertionError: 全局 Driver 对象不是 {ref}`nonebot.drivers.ASGIMixin` 类型
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        app = nonebot.get_app()
        ```
    """
    driver = get_driver()
    assert isinstance(driver, ASGIMixin), "app object is only available for asgi driver"
    return driver.server_app


def get_asgi() -> Any:
    """获取全局 {ref}`nonebot.drivers.ASGIMixin` 对应的
    [ASGI](https://asgi.readthedocs.io/) 对象。

    返回:
        ASGI 对象

    异常:
        AssertionError: 全局 Driver 对象不是 {ref}`nonebot.drivers.ASGIMixin` 类型
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        asgi = nonebot.get_asgi()
        ```
    """
    driver = get_driver()
    assert isinstance(driver, ASGIMixin), (
        "asgi object is only available for asgi driver"
    )
    return driver.asgi


def get_bot(self_id: Optional[str] = None) -> Bot:
    """获取一个连接到 NoneBot 的 {ref}`nonebot.adapters.Bot` 对象。

    当提供 `self_id` 时，此函数是 `get_bots()[self_id]` 的简写；
    当不提供时，返回一个 {ref}`nonebot.adapters.Bot`。

    参数:
        self_id: 用来识别 {ref}`nonebot.adapters.Bot` 的
            {ref}`nonebot.adapters.Bot.self_id` 属性

    返回:
        {ref}`nonebot.adapters.Bot` 对象

    异常:
        KeyError: 对应 self_id 的 Bot 不存在
        ValueError: 没有传入 self_id 且没有 Bot 可用
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        assert nonebot.get_bot("12345") == nonebot.get_bots()["12345"]

        another_unspecified_bot = nonebot.get_bot()
        ```
    """
    bots = get_bots()
    if self_id is not None:
        return bots[self_id]

    for bot in bots.values():
        return bot

    raise ValueError("There are no bots to get.")


def get_bots() -> dict[str, Bot]:
    """获取所有连接到 NoneBot 的 {ref}`nonebot.adapters.Bot` 对象。

    返回:
        一个以 {ref}`nonebot.adapters.Bot.self_id` 为键
        {ref}`nonebot.adapters.Bot` 对象为值的字典

    异常:
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化
            ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        bots = nonebot.get_bots()
        ```
    """
    return get_driver().bots


def _resolve_combine_expr(obj_str: str) -> type[Driver]:
    drivers = obj_str.split("+")
    DriverClass = resolve_dot_notation(
        drivers[0], "Driver", default_prefix="nonebot.drivers."
    )
    if len(drivers) == 1:
        logger.trace(f"Detected driver {DriverClass} with no mixins.")
        return DriverClass
    mixins = [
        resolve_dot_notation(mixin, "Mixin", default_prefix="nonebot.drivers.")
        for mixin in drivers[1:]
    ]
    logger.trace(f"Detected driver {DriverClass} with mixins {mixins}.")
    return combine_driver(DriverClass, *mixins)


def _log_patcher(record: "loguru.Record"):
    """使用插件标识优化日志展示"""
    record["name"] = (
        plugin.id_
        if (module_name := record["name"])
        and (plugin := get_plugin_by_module_name(module_name))
        else (module_name and module_name.split(".", maxsplit=1)[0])
    )


def init(*, _env_file: Optional[DOTENV_TYPE] = None, **kwargs: Any) -> None:
    """初始化 NoneBot 以及 全局 {ref}`nonebot.drivers.Driver` 对象。

    NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。

    也可以传入自定义的 `_env_file` 来指定 NoneBot 从该文件读取配置。

    参数:
        _env_file: 配置文件名，默认从 `.env.{env_name}` 中读取配置
        kwargs: 任意变量，将会存储到 {ref}`nonebot.drivers.Driver.config` 对象里

    用法:
        ```python
        nonebot.init(database=Database(...))
        ```
    """
    global _driver
    if not _driver:
        logger.success("NoneBot is initializing...")
        env = Env()
        _env_file = _env_file or f".env.{env.environment}"
        config = Config(
            **kwargs,
            _env_file=(
                (".env", _env_file)
                if isinstance(_env_file, (str, os.PathLike))
                else _env_file
            ),
        )

        logger.configure(
            extra={"nonebot_log_level": config.log_level}, patcher=_log_patcher
        )
        logger.opt(colors=True).info(
            f"Current <y><b>Env: {escape_tag(env.environment)}</b></y>"
        )
        logger.opt(colors=True).debug(
            f"Loaded <y><b>Config</b></y>: {escape_tag(str(model_dump(config)))}"
        )

        DriverClass = _resolve_combine_expr(config.driver)
        _driver = DriverClass(env, config)


def run(*args: Any, **kwargs: Any) -> None:
    """启动 NoneBot，即运行全局 {ref}`nonebot.drivers.Driver` 对象。

    参数:
        args: 传入 {ref}`nonebot.drivers.Driver.run` 的位置参数
        kwargs: 传入 {ref}`nonebot.drivers.Driver.run` 的命名参数

    用法:
        ```python
        nonebot.run(host="127.0.0.1", port=8080)
        ```
    """
    logger.success("Running NoneBot...")
    get_driver().run(*args, **kwargs)


from nonebot.plugin import CommandGroup as CommandGroup
from nonebot.plugin import MatcherGroup as MatcherGroup
from nonebot.plugin import get_available_plugin_names as get_available_plugin_names
from nonebot.plugin import get_loaded_plugins as get_loaded_plugins
from nonebot.plugin import get_plugin as get_plugin
from nonebot.plugin import get_plugin_by_module_name as get_plugin_by_module_name
from nonebot.plugin import get_plugin_config as get_plugin_config
from nonebot.plugin import load_all_plugins as load_all_plugins
from nonebot.plugin import load_builtin_plugin as load_builtin_plugin
from nonebot.plugin import load_builtin_plugins as load_builtin_plugins
from nonebot.plugin import load_from_json as load_from_json
from nonebot.plugin import load_from_toml as load_from_toml
from nonebot.plugin import load_plugin as load_plugin
from nonebot.plugin import load_plugins as load_plugins
from nonebot.plugin import on as on
from nonebot.plugin import on_command as on_command
from nonebot.plugin import on_endswith as on_endswith
from nonebot.plugin import on_fullmatch as on_fullmatch
from nonebot.plugin import on_keyword as on_keyword
from nonebot.plugin import on_message as on_message
from nonebot.plugin import on_metaevent as on_metaevent
from nonebot.plugin import on_notice as on_notice
from nonebot.plugin import on_regex as on_regex
from nonebot.plugin import on_request as on_request
from nonebot.plugin import on_shell_command as on_shell_command
from nonebot.plugin import on_startswith as on_startswith
from nonebot.plugin import on_type as on_type
from nonebot.plugin import require as require
