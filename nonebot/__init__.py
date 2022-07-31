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
- `CommandGroup` => {ref}``CommandGroup` <nonebot.plugin.on.CommandGroup>`
- `Matchergroup` => {ref}``MatcherGroup` <nonebot.plugin.on.MatcherGroup>`
- `load_plugin` => {ref}``load_plugin` <nonebot.plugin.load.load_plugin>`
- `load_plugins` => {ref}``load_plugins` <nonebot.plugin.load.load_plugins>`
- `load_all_plugins` => {ref}``load_all_plugins` <nonebot.plugin.load.load_all_plugins>`
- `load_from_json` => {ref}``load_from_json` <nonebot.plugin.load.load_from_json>`
- `load_from_toml` => {ref}``load_from_toml` <nonebot.plugin.load.load_from_toml>`
- `load_builtin_plugin` => {ref}``load_builtin_plugin` <nonebot.plugin.load.load_builtin_plugin>`
- `load_builtin_plugins` => {ref}``load_builtin_plugins` <nonebot.plugin.load.load_builtin_plugins>`
- `get_plugin` => {ref}``get_plugin` <nonebot.plugin.get_plugin>`
- `get_plugin_by_module_name` => {ref}``get_plugin_by_module_name` <nonebot.plugin.get_plugin_by_module_name>`
- `get_loaded_plugins` => {ref}``get_loaded_plugins` <nonebot.plugin.get_loaded_plugins>`
- `get_available_plugin_names` => {ref}``get_available_plugin_names` <nonebot.plugin.get_available_plugin_names>`
- `export` => {ref}``export` <nonebot.plugin.export.export>`
- `require` => {ref}``require` <nonebot.plugin.load.require>`

FrontMatter:
    sidebar_position: 0
    description: nonebot 模块
"""

import importlib
from typing import Any, Dict, Type, Optional

from nonebot.adapters import Bot
from nonebot.utils import escape_tag
from nonebot.config import Env, Config
from nonebot.log import logger, default_filter
from nonebot.drivers import Driver, ReverseDriver, combine_driver

try:
    import pkg_resources

    _dist: pkg_resources.Distribution = pkg_resources.get_distribution("nonebot2")
    __version__ = _dist.version
    VERSION = _dist.parsed_version
except Exception:  # pragma: no cover
    __version__ = None
    VERSION = None

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """获取全局 {ref}`nonebot.drivers.Driver` 实例。

    可用于在计划任务的回调等情形中获取当前 {ref}`nonebot.drivers.Driver` 实例。

    返回:
        全局 {ref}`nonebot.drivers.Driver` 对象

    异常:
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化 ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        driver = nonebot.get_driver()
        ```
    """
    if _driver is None:
        raise ValueError("NoneBot has not been initialized.")
    return _driver


def get_app() -> Any:
    """获取全局 {ref}`nonebot.drivers.ReverseDriver` 对应的 Server App 对象。

    返回:
        Server App 对象

    异常:
        AssertionError: 全局 Driver 对象不是 {ref}`nonebot.drivers.ReverseDriver` 类型
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化 ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        app = nonebot.get_app()
        ```
    """
    driver = get_driver()
    assert isinstance(
        driver, ReverseDriver
    ), "app object is only available for reverse driver"
    return driver.server_app


def get_asgi() -> Any:
    """获取全局 {ref}`nonebot.drivers.ReverseDriver` 对应 [ASGI](https://asgi.readthedocs.io/) 对象。

    返回:
        ASGI 对象

    异常:
        AssertionError: 全局 Driver 对象不是 {ref}`nonebot.drivers.ReverseDriver` 类型
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化 ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        asgi = nonebot.get_asgi()
        ```
    """
    driver = get_driver()
    assert isinstance(
        driver, ReverseDriver
    ), "asgi object is only available for reverse driver"
    return driver.asgi


def get_bot(self_id: Optional[str] = None) -> Bot:
    """获取一个连接到 NoneBot 的 {ref}`nonebot.adapters.Bot` 对象。

    当提供 `self_id` 时，此函数是 `get_bots()[self_id]` 的简写；
    当不提供时，返回一个 {ref}`nonebot.adapters.Bot`。

    参数:
        self_id: 用来识别 {ref}`nonebot.adapters.Bot` 的 {ref}`nonebot.adapters.Bot.self_id` 属性

    返回:
        {ref}`nonebot.adapters.Bot` 对象

    异常:
        KeyError: 对应 self_id 的 Bot 不存在
        ValueError: 没有传入 self_id 且没有 Bot 可用
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化 ({ref}`nonebot.init <nonebot.init>` 尚未调用)

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


def get_bots() -> Dict[str, Bot]:
    """获取所有连接到 NoneBot 的 {ref}`nonebot.adapters.Bot` 对象。

    返回:
        一个以 {ref}`nonebot.adapters.Bot.self_id` 为键，{ref}`nonebot.adapters.Bot` 对象为值的字典

    异常:
        ValueError: 全局 {ref}`nonebot.drivers.Driver` 对象尚未初始化 ({ref}`nonebot.init <nonebot.init>` 尚未调用)

    用法:
        ```python
        bots = nonebot.get_bots()
        ```
    """
    driver = get_driver()
    return driver.bots


def _resolve_dot_notation(
    obj_str: str, default_attr: str, default_prefix: Optional[str] = None
) -> Any:
    modulename, _, cls = obj_str.partition(":")
    if default_prefix is not None and modulename.startswith("~"):
        modulename = default_prefix + modulename[1:]
    module = importlib.import_module(modulename)
    if not cls:
        return getattr(module, default_attr)
    instance = module
    for attr_str in cls.split("."):
        instance = getattr(instance, attr_str)
    return instance


def _resolve_combine_expr(obj_str: str) -> Type[Driver]:
    drivers = obj_str.split("+")
    DriverClass = _resolve_dot_notation(
        drivers[0], "Driver", default_prefix="nonebot.drivers."
    )
    if len(drivers) == 1:
        logger.trace(f"Detected driver {DriverClass} with no mixins.")
        return DriverClass
    mixins = [
        _resolve_dot_notation(mixin, "Mixin", default_prefix="nonebot.drivers.")
        for mixin in drivers[1:]
    ]
    logger.trace(f"Detected driver {DriverClass} with mixins {mixins}.")
    return combine_driver(DriverClass, *mixins)


def init(*, _env_file: Optional[str] = None, **kwargs: Any) -> None:
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
        config = Config(
            **kwargs,
            _common_config=env.dict(),
            _env_file=_env_file or f".env.{env.environment}",
        )

        default_filter.level = config.log_level
        logger.opt(colors=True).info(
            f"Current <y><b>Env: {escape_tag(env.environment)}</b></y>"
        )
        logger.opt(colors=True).debug(
            f"Loaded <y><b>Config</b></y>: {escape_tag(str(config.dict()))}"
        )

        DriverClass: Type[Driver] = _resolve_combine_expr(config.driver)
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


from nonebot.plugin import on as on
from nonebot.plugin import export as export
from nonebot.plugin import require as require
from nonebot.plugin import on_regex as on_regex
from nonebot.plugin import on_notice as on_notice
from nonebot.plugin import get_plugin as get_plugin
from nonebot.plugin import on_command as on_command
from nonebot.plugin import on_keyword as on_keyword
from nonebot.plugin import on_message as on_message
from nonebot.plugin import on_request as on_request
from nonebot.plugin import load_plugin as load_plugin
from nonebot.plugin import on_endswith as on_endswith
from nonebot.plugin import CommandGroup as CommandGroup
from nonebot.plugin import MatcherGroup as MatcherGroup
from nonebot.plugin import load_plugins as load_plugins
from nonebot.plugin import on_fullmatch as on_fullmatch
from nonebot.plugin import on_metaevent as on_metaevent
from nonebot.plugin import on_startswith as on_startswith
from nonebot.plugin import load_from_json as load_from_json
from nonebot.plugin import load_from_toml as load_from_toml
from nonebot.plugin import load_all_plugins as load_all_plugins
from nonebot.plugin import on_shell_command as on_shell_command
from nonebot.plugin import get_loaded_plugins as get_loaded_plugins
from nonebot.plugin import load_builtin_plugin as load_builtin_plugin
from nonebot.plugin import load_builtin_plugins as load_builtin_plugins
from nonebot.plugin import get_plugin_by_module_name as get_plugin_by_module_name
from nonebot.plugin import get_available_plugin_names as get_available_plugin_names

__autodoc__ = {"internal": False}
