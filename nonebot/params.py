"""本模块定义了依赖注入的各类参数。

FrontMatter:
    sidebar_position: 4
    description: nonebot.params 模块
"""

from typing import Any, List, Union, Optional

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.internal.params import Arg as Arg
from nonebot.internal.params import ArgStr as ArgStr
from nonebot.internal.params import depends as depends
from nonebot.internal.params import ArgParam as ArgParam
from nonebot.internal.params import BotParam as BotParam
from nonebot.adapters import Event, Message, MessageSegment
from nonebot.internal.params import EventParam as EventParam
from nonebot.internal.params import StateParam as StateParam
from nonebot.internal.params import DependParam as DependParam
from nonebot.internal.params import ArgPlainText as ArgPlainText
from nonebot.internal.params import DefaultParam as DefaultParam
from nonebot.internal.params import MatcherParam as MatcherParam
from nonebot.internal.params import ExceptionParam as ExceptionParam
from nonebot.consts import (
    CMD_KEY,
    PREFIX_KEY,
    REGEX_DICT,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    RAW_CMD_KEY,
    REGEX_GROUP,
    CMD_START_KEY,
    REGEX_MATCHED,
)


@depends
async def event_type(event: Event) -> str:
    """{ref}`nonebot.adapters.Event` 类型参数"""
    return event.get_type()


@depends
async def event_message(event: Event) -> Message:
    """{ref}`nonebot.adapters.Event` 消息参数"""
    return event.get_message()


@depends
async def event_plain_text(event: Event) -> str:
    """{ref}`nonebot.adapters.Event` 纯文本消息参数"""
    return event.get_plaintext()


@depends
async def event_to_me(event: Event) -> bool:
    """{ref}`nonebot.adapters.Event` `to_me` 参数"""
    return event.is_tome()


@depends
def command(state: T_State) -> Message:
    """消息命令元组"""
    return state[PREFIX_KEY][CMD_KEY]


@depends
def raw_command(state: T_State) -> Message:
    """消息命令文本"""
    return state[PREFIX_KEY][RAW_CMD_KEY]


@depends
def command_arg(state: T_State) -> Message:
    """消息命令参数"""
    return state[PREFIX_KEY][CMD_ARG_KEY]


@depends
def command_start(state: T_State) -> str:
    """消息命令开头"""
    return state[PREFIX_KEY][CMD_START_KEY]


@depends(use_cache=False)
def shell_command_args(state: T_State) -> Any:
    """shell 命令解析后的参数字典"""
    return state[SHELL_ARGS]  # Namespace or ParserExit


@depends(use_cache=False)
def shell_command_argv(state: T_State) -> List[Union[str, MessageSegment]]:
    """shell 命令原始参数列表"""
    return state[SHELL_ARGV]


@depends(use_cache=False)
def regex_matched(state: T_State) -> str:
    """正则匹配结果"""
    return state[REGEX_MATCHED]


@depends(use_cache=False)
def regex_group(state: T_State):
    """正则匹配结果 group 元组"""
    return state[REGEX_GROUP]


@depends(use_cache=False)
def regex_dict(state: T_State):
    """正则匹配结果 group 字典"""
    return state[REGEX_DICT]


def received(id: Optional[str] = None, default: Any = None) -> Any:
    """`receive` 事件参数"""

    @depends(use_cache=False)
    def _received(matcher: "Matcher"):
        return matcher.get_receive(id or "", default)

    return _received


def last_received(default: Any = None) -> Any:
    """`last_receive` 事件参数"""

    @depends(use_cache=False)
    def _last_received(matcher: "Matcher") -> Any:
        return matcher.get_last_receive(default)

    return _last_received


__autodoc__ = {
    "Arg": True,
    "ArgStr": True,
    "depends": True,
    "ArgParam": True,
    "BotParam": True,
    "EventParam": True,
    "StateParam": True,
    "DependParam": True,
    "ArgPlainText": True,
    "DefaultParam": True,
    "MatcherParam": True,
    "ExceptionParam": True,
}
