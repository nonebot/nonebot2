from collections.abc import Generator
from functools import wraps
import os
from pathlib import Path
import threading
from typing import TYPE_CHECKING, Callable, TypeVar
from typing_extensions import ParamSpec

from nonebug import NONEBOT_INIT_KWARGS
import pytest
from werkzeug.serving import BaseWSGIServer, make_server

from fake_server import request_handler
import nonebot
from nonebot import _resolve_combine_expr
from nonebot.config import Env
from nonebot.drivers import URL, Driver

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'
os.environ["CONFIG_OVERRIDE"] = "new"

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

P = ParamSpec("P")
R = TypeVar("R")

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


@pytest.fixture(scope="session", params=[pytest.param("asyncio"), pytest.param("trio")])
def anyio_backend(request: pytest.FixtureRequest):
    return request.param


def run_once(func: Callable[P, R]) -> Callable[P, R]:
    result = ...

    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        nonlocal result
        if result is not Ellipsis:
            return result

        result = func(*args, **kwargs)
        return result

    return _wrapper


@pytest.fixture(scope="session", autouse=True)
@run_once
def load_plugin(anyio_backend, nonebug_init: None) -> set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))


@pytest.fixture(scope="session", autouse=True)
@run_once
def load_builtin_plugin(anyio_backend, nonebug_init: None) -> set["Plugin"]:
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
