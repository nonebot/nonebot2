"""
协议适配基类
============

各协议请继承以下基类，并使用 ``driver.register_adapter`` 注册适配器
"""

from typing import Iterable

try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
    del pkg_resources
except ImportError:
    import pkgutil
    __path__: Iterable[str] = pkgutil.extend_path(
        __path__,  # type: ignore
        __name__)
    del pkgutil
except Exception:
    pass

from ._bot import Bot
from ._event import Event
from ._message import Message, MessageSegment
