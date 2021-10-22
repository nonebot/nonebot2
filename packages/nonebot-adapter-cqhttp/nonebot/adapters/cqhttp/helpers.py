from typing import List, Optional, Union
from .message import Message
from .bot import Bot
from .event import MessageEvent
from nonebot.matcher import Matcher
import re


def extract_image_urls(message: Message) -> List[str]:
    return [
        segment.data['url']
        for segment in message
        if (segment.type == 'image') and ('url' in segment.data)
    ]


NUMBERS_REGEXP = re.compile(r'[+-]?(\d*\.?\d+|\d+\.?\d*)')


def extract_numbers(message: Message) -> List[float]:
    return [
        float(matched)
        for matched in NUMBERS_REGEXP.findall(message.extract_plain_text())
    ]


CHINESE_AGREE_WORD = {
    '要', '用', '是', '好', '对', '嗯', '行', 'ok', 'okay', 'yeah', 'yep', '当真', '当然',
    '必须', '可以', '肯定', '没错', '确定', '确认'
}
CHINESE_DECLINE_WORD = {
    '不', '不要', '不用', '不是', '否', '不好', '不对', '不行', '别', 'no', 'nono', 'nonono',
    'nope', '不ok', '不可以', '不能', '不可以'
}
CHINESE_TRAILING_WORD = ',.!?~，。！？～了的呢吧呀啊呗啦'


def convert_chinese_to_bool(message: Union[Message, str]) -> Optional[bool]:
    text = message.extract_plain_text() if isinstance(message,
                                                      Message) else message
    text = text.lower().strip().replace(' ', '').rstrip(CHINESE_TRAILING_WORD)

    if text in CHINESE_AGREE_WORD:
        return True
    if text in CHINESE_DECLINE_WORD:
        return False
    return None


def remove_empty_lines(message: Union[Message, str],
                       include_stripped: bool = False) -> str:
    text = message.extract_plain_text() if isinstance(message,
                                                      Message) else message
    return ''.join(line for line in text.splitlines(keepends=False)
                   if bool(line.strip() if include_stripped else line))


CHINESE_CANCELLATION_WORDS = {'算', '别', '不', '停', '取消'}
CHINESE_CANCELLATION_REGEX_1 = re.compile(r'^那?[算别不停]\w{0,3}了?吧?$')
CHINESE_CANCELLATION_REGEX_2 = re.compile(r'^那?(?:[给帮]我)?取消了?吧?$')


def is_cancellation(message: Union[Message, str]) -> bool:
    text = message.extract_plain_text() if isinstance(message,
                                                      Message) else message
    return any(kw in text for kw in CHINESE_CANCELLATION_WORDS) and bool(
        CHINESE_CANCELLATION_REGEX_1.match(text) or
        CHINESE_CANCELLATION_REGEX_2.match(text))


def handle_cancellation(reject_prompt: Optional[str] = None):

    async def cancellation_rule(matcher: Matcher, bot: Bot,
                                event: MessageEvent) -> bool:
        cancelled = is_cancellation(event.message)
        if cancelled and reject_prompt:
            await matcher.finish(reject_prompt)
        return not cancelled

    return cancellation_rule