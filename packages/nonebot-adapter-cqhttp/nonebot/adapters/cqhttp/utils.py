from typing import Optional

from nonebot.utils import logger_wrapper

log = logger_wrapper("CQHTTP")


def escape(s: str, *, escape_comma: bool = True) -> str:
    """
    :说明:

      对字符串进行 CQ 码转义。

    :参数:

      * ``s: str``: 需要转义的字符串
      * ``escape_comma: bool``: 是否转义逗号（``,``）。
    """
    s = s.replace("&", "&amp;") \
        .replace("[", "&#91;") \
        .replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


def unescape(s: str) -> str:
    """
    :说明:

      对字符串进行 CQ 码去转义。

    :参数:

      * ``s: str``: 需要转义的字符串
    """
    return s.replace("&#44;", ",") \
        .replace("&#91;", "[") \
        .replace("&#93;", "]") \
        .replace("&amp;", "&")


def _b2s(b: Optional[bool]) -> Optional[str]:
    """转换布尔值为字符串。"""
    return b if b is None else str(b).lower()
