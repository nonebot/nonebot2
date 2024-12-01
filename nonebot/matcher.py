"""本模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行对话。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 3
    description: nonebot.matcher 模块
"""

from nonebot.internal.matcher import DEFAULT_PROVIDER_CLASS as DEFAULT_PROVIDER_CLASS
from nonebot.internal.matcher import Matcher as Matcher
from nonebot.internal.matcher import MatcherManager as MatcherManager
from nonebot.internal.matcher import MatcherProvider as MatcherProvider
from nonebot.internal.matcher import MatcherSource as MatcherSource
from nonebot.internal.matcher import current_bot as current_bot
from nonebot.internal.matcher import current_event as current_event
from nonebot.internal.matcher import current_handler as current_handler
from nonebot.internal.matcher import current_matcher as current_matcher
from nonebot.internal.matcher import matchers as matchers

__autodoc__ = {
    "Matcher": True,
    "matchers": True,
    "MatcherManager": True,
    "MatcherProvider": True,
    "DEFAULT_PROVIDER_CLASS": True,
}
