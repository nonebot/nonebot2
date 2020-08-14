#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
import dataclasses
from functools import wraps, partial

from nonebot.typing import Any, Callable, Awaitable, overrides


def run_sync(func: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:

    @wraps(func)
    async def _wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


class DataclassEncoder(json.JSONEncoder):

    @overrides(json.JSONEncoder)
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
