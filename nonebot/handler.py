"""
事件处理函数
============

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""

import inspect
from typing import Optional

from pydantic.typing import evaluate_forwardref

from nonebot.utils import get_name
from nonebot.typing import T_Handler


class Handler:
    """事件处理函数类"""

    def __init__(self, func: T_Handler, *, name: Optional[str] = None):
        """装饰事件处理函数以便根据动态参数运行"""
        self.func: T_Handler = func
        """
        :类型: ``T_Handler``
        :说明: 事件处理函数
        """
        self.name = get_name(func) if name is None else name
