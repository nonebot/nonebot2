import os
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Set, Generator

import pytest
from nonebug import NONEBOT_INIT_KWARGS
from werkzeug.serving import BaseWSGIServer, make_server

import nonebot
from nonebot.config import Env
from fake_server import request_handler
from nonebot.drivers import URL, Driver
from nonebot import _resolve_combine_expr

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'
os.environ["CONFIG_OVERRIDE"] = "new"

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

collect_ignore = ["plugins/", "dynamic/", "bad_plugins/"]


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"config_from_init": "init"}


@pytest.fixture(name="driver")
def load_driver(request: pytest.FixtureRequest) -> Driver:
    driver_name = getattr(request, "param", None)
    global_driver = nonebot.get_driver()
    if driver_name is None:
        return global_driver

    DriverClass = _resolve_combine_expr(driver_name)
    return DriverClass(Env(environment=global_driver.env), global_driver.config)


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))


@pytest.fixture(scope="session", autouse=True)
def load_builtin_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload builtin plugins
    return nonebot.load_builtin_plugins("echo", "single_session")


@pytest.fixture(scope="session", autouse=True)
def server() -> Generator[BaseWSGIServer, None, None]:
    server = make_server("127.0.0.1", 0, app=request_handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join()


@pytest.fixture(scope="session")
def server_url(server: BaseWSGIServer) -> URL:
    return URL(f"http://{server.host}:{server.port}")
