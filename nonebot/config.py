#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Set, Union
from ipaddress import IPv4Address

from pydantic import BaseSettings


class Env(BaseSettings):
    environment: str = "prod"

    class Config:
        env_file = ".env"


class Config(BaseSettings):
    driver: str = "nonebot.drivers.fastapi"
    host: IPv4Address = IPv4Address("127.0.0.1")
    port: int = 8080
    debug: bool = False

    superusers: Set[int] = set()
    nickname: Union[str, Set[str]] = ""

    custom_config: dict = {}

    class Config:
        env_file = ".env.prod"
