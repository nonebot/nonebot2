#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import dataclasses

from nonebot.typing import overrides


class DataclassEncoder(json.JSONEncoder):

    @overrides(json.JSONEncoder)
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
