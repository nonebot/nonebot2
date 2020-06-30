#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable, Awaitable

Handler = Callable[["Bot", "Event", dict], Awaitable[None]]
