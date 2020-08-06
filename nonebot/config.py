#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from ipaddress import IPv4Address
from typing import Set, Dict, Union, Optional

from pydantic import BaseSettings


class Env(BaseSettings):
    environment: str = "prod"

    class Config:
        env_file = ".env"


class Config(BaseSettings):
    # nonebot configs
    driver: str = "nonebot.drivers.fastapi"
    host: IPv4Address = IPv4Address("127.0.0.1")
    port: int = 8080
    secret: Optional[str] = None
    debug: bool = False

    # bot connection configs
    api_root: Dict[int, str] = {}
    access_token: Optional[str] = None

    # bot runtime configs
    superusers: Set[int] = set()
    nickname: Union[str, Set[str]] = ""
    session_expire_timeout: timedelta = timedelta(minutes=2)

    # custom configs
    custom_config: dict = {}

    class Config:
        env_file = ".env.prod"
