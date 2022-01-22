"""本模块定义了协议适配基类，各协议请继承以下基类。

使用 {ref}`nonebot.drivers.Driver.register_adapter` 注册适配器。

FrontMatter:
    sidebar_position: 0
    description: nonebot.adapters 模块
"""

from typing import Iterable

try:
    import pkg_resources

    pkg_resources.declare_namespace(__name__)
    del pkg_resources
except ImportError:
    import pkgutil

    __path__: Iterable[str] = pkgutil.extend_path(__path__, __name__)  # type: ignore
    del pkgutil
except Exception:
    pass

from ._bot import Bot as Bot
from ._event import Event as Event
from ._adapter import Adapter as Adapter
from ._message import Message as Message
from ._message import MessageSegment as MessageSegment
from ._template import MessageTemplate as MessageTemplate

__autodoc__ = {
    "_bot": True,
    "_event": True,
    "_adapter": True,
    "_message": True,
    "_template": True,
}
