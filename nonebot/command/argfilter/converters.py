from typing import Optional, List


def _simple_chinese_to_bool(text: str) -> Optional[bool]:
    """
    Convert a chinese text to boolean.

    Examples:

        是的 -> True
        好的呀 -> True
        不要 -> False
        不用了 -> False
        你好呀 -> None
    """
    text = text.strip().lower().replace(' ', '') \
        .rstrip(',.!?~，。！？～了的呢吧呀啊呗啦')
    if text in {'要', '用', '是', '好', '对', '嗯', '行',
                'ok', 'okay', 'yeah', 'yep',
                '当真', '当然', '必须', '可以', '肯定', '没错', '确定', '确认'}:
        return True
    if text in {'不', '不要', '不用', '不是', '否', '不好', '不对', '不行', '别',
                'no', 'nono', 'nonono', 'nope', '不ok', '不可以', '不能',
                '不可以'}:
        return False
    return None


def _split_nonempty_lines(text: str) -> List[str]:
    return list(filter(lambda x: x, text.splitlines()))


def _split_nonempty_stripped_lines(text: str) -> List[str]:
    return list(filter(lambda x: x,
                       map(lambda x: x.strip(), text.splitlines())))


simple_chinese_to_bool = _simple_chinese_to_bool
split_nonempty_lines = _split_nonempty_lines
split_nonempty_stripped_lines = _split_nonempty_stripped_lines
