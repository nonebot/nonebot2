"""本模块定义了依赖注入的各类参数。

FrontMatter:
    sidebar_position: 4
    description: nonebot.params 模块
"""

from typing import Any, Dict, List, Tuple, Optional

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Event, Message
from nonebot.internal.params import Arg as Arg
from nonebot.internal.params import State as State
from nonebot.internal.params import ArgStr as ArgStr
from nonebot.internal.params import Depends as Depends
from nonebot.internal.params import ArgParam as ArgParam
from nonebot.internal.params import BotParam as BotParam
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


async def _event_type(event: Event) -> str:
    return event.get_type()


def EventType() -> str:
    """{ref}`nonebot.adapters.Event` 类型参数"""
    return Depends(_event_type)


async def _event_message(event: Event) -> Message:
    return event.get_message()


def EventMessage() -> Any:
    """{ref}`nonebot.adapters.Event` 消息参数"""
    return Depends(_event_message)


async def _event_plain_text(event: Event) -> str:
    return event.get_plaintext()


def EventPlainText() -> str:
    """{ref}`nonebot.adapters.Event` 纯文本消息参数"""
    return Depends(_event_plain_text)


async def _event_to_me(event: Event) -> bool:
    return event.is_tome()


def EventToMe() -> bool:
    """{ref}`nonebot.adapters.Event` `to_me` 参数"""
    return Depends(_event_to_me)


def _command(state: T_State) -> Message:
    return state[PREFIX_KEY][CMD_KEY]


def Command() -> Tuple[str, ...]:
    """消息命令元组"""
    return Depends(_command)


def _raw_command(state: T_State) -> Message:
    return state[PREFIX_KEY][RAW_CMD_KEY]


def RawCommand() -> str:
    """消息命令文本"""
    return Depends(_raw_command)


def _command_arg(state: T_State) -> Message:
    return state[PREFIX_KEY][CMD_ARG_KEY]


def CommandArg() -> Any:
    """消息命令参数"""
    return Depends(_command_arg)


def _command_start(state: T_State) -> str:
    return state[PREFIX_KEY][CMD_START_KEY]


def CommandStart() -> str:
    """消息命令开头"""
    return Depends(_command_start)


def _shell_command_args(state: T_State) -> Any:
    return state[SHELL_ARGS]


def ShellCommandArgs():
    """shell 命令解析后的参数字典"""
    return Depends(_shell_command_args, use_cache=False)


def _shell_command_argv(state: T_State) -> List[str]:
    return state[SHELL_ARGV]


def ShellCommandArgv() -> Any:
    """shell 命令原始参数列表"""
    return Depends(_shell_command_argv, use_cache=False)


def _regex_matched(state: T_State) -> str:
    return state[REGEX_MATCHED]


def RegexMatched() -> str:
    """正则匹配结果"""
    return Depends(_regex_matched, use_cache=False)


def _regex_group(state: T_State):
    return state[REGEX_GROUP]


def RegexGroup() -> Tuple[Any, ...]:
    """正则匹配结果 group 元组"""
    return Depends(_regex_group, use_cache=False)


def _regex_dict(state: T_State):
    return state[REGEX_DICT]


def RegexDict() -> Dict[str, Any]:
    """正则匹配结果 group 字典"""
    return Depends(_regex_dict, use_cache=False)


def Received(id: Optional[str] = None, default: Any = None) -> Any:
    """`receive` 事件参数"""

    def _received(matcher: "Matcher"):
        return matcher.get_receive(id or "", default)

    return Depends(_received, use_cache=False)


def LastReceived(default: Any = None) -> Any:
    """`last_receive` 事件参数"""

    def _last_received(matcher: "Matcher") -> Any:
        return matcher.get_last_receive(default)

    return Depends(_last_received, use_cache=False)


__autodoc__ = {
    "Arg": True,
    "State": True,
    "ArgStr": True,
    "Depends": True,
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
