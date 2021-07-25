from pathlib import Path

from nonebot.drivers.fastapi import Driver
from fastapi.staticfiles import StaticFiles


def register_route(driver: Driver):
    app = driver.server_app

    static_path = str((Path(__file__).parent / ".." / "dist").resolve())

    app.mount("/docs",
              StaticFiles(directory=static_path, html=True),
              name="docs")
