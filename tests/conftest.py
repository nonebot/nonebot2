import os
import json
import base64
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Set, Dict, List, Union, TypeVar, Generator

import pytest
from werkzeug import Request, Response
from nonebug import NONEBOT_INIT_KWARGS
from werkzeug.datastructures import MultiDict
from werkzeug.serving import BaseWSGIServer, make_server

import nonebot
from nonebot.drivers import URL

os.environ["CONFIG_FROM_ENV"] = '{"test": "test"}'
os.environ["CONFIG_OVERRIDE"] = "new"

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


K = TypeVar("K")
V = TypeVar("V")


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"config_from_init": "init"}


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))


@pytest.fixture(scope="session", autouse=True)
def load_builtin_plugin(nonebug_init: None) -> Set["Plugin"]:
    # preload builtin plugins
    return nonebot.load_builtin_plugins("echo", "single_session")


def json_safe(string, content_type="application/octet-stream") -> str:
    try:
        string = string.decode("utf-8")
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b"".join(
            [
                b"data:",
                content_type.encode("utf-8"),
                b";base64,",
                base64.b64encode(string),
            ]
        ).decode("utf-8")


def flattern(d: MultiDict[K, V]) -> Dict[K, Union[V, List[V]]]:
    return {k: v[0] if len(v) == 1 else v for k, v in d.to_dict(flat=False).items()}


@Request.application
def request_handler(request: Request) -> Response:
    try:
        _json = json.loads(request.data.decode("utf-8"))
    except (ValueError, TypeError):
        _json = None

    return Response(
        json.dumps(
            {
                "url": request.url,
                "method": request.method,
                "origin": request.headers.get("X-Forwarded-For", request.remote_addr),
                "headers": flattern(
                    MultiDict((k, v) for k, v in request.headers.items())
                ),
                "args": flattern(request.args),
                "form": flattern(request.form),
                "data": json_safe(request.data),
                "json": _json,
                "files": flattern(
                    MultiDict(
                        (
                            k,
                            json_safe(
                                v.read(),
                                request.files[k].content_type
                                or "application/octet-stream",
                            ),
                        )
                        for k, v in request.files.items()
                    )
                ),
            }
        ),
        status=200,
        content_type="application/json",
    )


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
