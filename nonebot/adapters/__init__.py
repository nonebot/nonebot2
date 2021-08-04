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

from ._base import Bot, Event, Message, MessageSegment
