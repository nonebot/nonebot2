import re
from typing import List

from nonebot.message import Message
from nonebot.typing import Message_T


def _extract_text(arg: Message_T) -> str:
    """Extract all plain text segments from a message-like object."""
    arg_as_msg = Message(arg)
    return arg_as_msg.extract_plain_text()


def _extract_image_urls(arg: Message_T) -> List[str]:
    """Extract all image urls from a message-like object."""
    arg_as_msg = Message(arg)
    return [s.data['url'] for s in arg_as_msg
            if s.type == 'image' and 'url' in s.data]


def _extract_numbers(arg: Message_T) -> List[float]:
    """Extract all numbers (integers and floats) from a message-like object."""
    s = str(arg)
    return list(map(float, re.findall(r'[+-]?(\d*\.?\d+|\d+\.?\d*)', s)))


extract_text = _extract_text
extract_image_urls = _extract_image_urls
extract_numbers = _extract_numbers
