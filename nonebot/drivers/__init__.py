#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
from ipaddress import IPv4Address


class BaseDriver(object):

    @property
    def server_app(self):
        raise NotImplementedError

    @property
    def asgi(self):
        raise NotImplementedError

    @property
    def logger(self):
        raise NotImplementedError

    def run(self,
            host: Optional[IPv4Address] = None,
            port: Optional[int] = None,
            *args,
            **kwargs):
        raise NotImplementedError
