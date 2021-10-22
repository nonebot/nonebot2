import re
from enum import IntEnum, auto
from collections import defaultdict
from asyncio import get_running_loop
from typing import Set, List, Type, Union, Optional, DefaultDict

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event

from .message import Message
from .event import MessageEvent, GroupMessageEvent


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


class CommandDebounce:
    debounced: DefaultDict[Type[Matcher], Set[str]] = defaultdict(set)

    class IsolateLevel(IntEnum):
        GLOBAL = auto()
        GROUP = auto()
        USER = auto()
        GROUP_USER = auto()

    def __init__(
        self,
        matcher: Type[Matcher],
        isolate_level: IsolateLevel = IsolateLevel.USER,
        debounce_timeout: float = 5,
        cancel_message: Optional[str] = None,
    ):
        self.isolate_level = isolate_level
        self.debounce_timeout = debounce_timeout
        self.matcher = matcher
        self.cancel_message = cancel_message

    async def __call__(self, bot: Bot, event: Event, state: T_State) -> bool:
        if not isinstance(event, MessageEvent):
            return True

        loop = get_running_loop()
        debounce_set = CommandDebounce.debounced[self.matcher]

        if self.isolate_level is self.IsolateLevel.GROUP:
            key = str(
                event.group_id
                if isinstance(event, GroupMessageEvent) else event.user_id,)
        elif self.isolate_level is self.IsolateLevel.USER:
            key = str(event.user_id)
        elif self.isolate_level is self.IsolateLevel.GROUP_USER:
            key = f'{event.group_id}_{event.user_id}' if isinstance(
                event, GroupMessageEvent) else str(event.user_id)
        elif self.isolate_level is self.IsolateLevel.GLOBAL:
            key = self.IsolateLevel.GLOBAL.name
        else:
            raise ValueError(f'invalid isolate level: {self.isolate_level!r}, '
                             'isolate level must use provided enumerate value.')

        if key in debounce_set:
            await self.matcher.finish(message=self.cancel_message,
                                      at_sender=True)
            return False
        else:
            debounce_set.add(key)
            loop.call_later(self.debounce_timeout,
                            lambda: debounce_set.remove(key))
            return True

    def apply(self) -> Type[Matcher]:
        self.matcher.rule.checkers.add(self.__call__)
        return self.matcher
