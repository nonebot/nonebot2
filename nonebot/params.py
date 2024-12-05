"""本模块定义了依赖注入的各类参数。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 4
    description: nonebot.params 模块
"""

from re import Match
from typing import Any, Callable, Literal, Optional, Union, overload

from nonebot.adapters import Event, Message, MessageSegment
from nonebot.consts import (
    CMD_ARG_KEY,
    CMD_KEY,
    CMD_START_KEY,
    CMD_WHITESPACE_KEY,
    ENDSWITH_KEY,
    FULLMATCH_KEY,
    KEYWORD_KEY,
    PAUSE_PROMPT_RESULT_KEY,
    PREFIX_KEY,
    RAW_CMD_KEY,
    RECEIVE_KEY,
    REGEX_MATCHED,
    REJECT_PROMPT_RESULT_KEY,
    SHELL_ARGS,
    SHELL_ARGV,
    STARTSWITH_KEY,
)
from nonebot.internal.params import Arg as Arg
from nonebot.internal.params import ArgParam as ArgParam
from nonebot.internal.params import ArgPlainText as ArgPlainText
from nonebot.internal.params import ArgPromptResult as ArgPromptResult
from nonebot.internal.params import ArgStr as ArgStr
from nonebot.internal.params import BotParam as BotParam
from nonebot.internal.params import DefaultParam as DefaultParam
from nonebot.internal.params import DependParam as DependParam
from nonebot.internal.params import Depends as Depends
from nonebot.internal.params import EventParam as EventParam
from nonebot.internal.params import ExceptionParam as ExceptionParam
from nonebot.internal.params import MatcherParam as MatcherParam
from nonebot.internal.params import StateParam as StateParam
from nonebot.matcher import Matcher
from nonebot.typing import T_State


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


def Command() -> tuple[str, ...]:
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


def _command_whitespace(state: T_State) -> str:
    return state[PREFIX_KEY][CMD_WHITESPACE_KEY]


def CommandWhitespace() -> str:
    """消息命令与参数之间的空白"""
    return Depends(_command_whitespace)


def _shell_command_args(state: T_State) -> Any:
    return state[SHELL_ARGS]  # Namespace or ParserExit


def ShellCommandArgs() -> Any:
    """shell 命令解析后的参数字典"""
    return Depends(_shell_command_args, use_cache=False)


def _shell_command_argv(state: T_State) -> list[Union[str, MessageSegment]]:
    return state[SHELL_ARGV]


def ShellCommandArgv() -> Any:
    """shell 命令原始参数列表"""
    return Depends(_shell_command_argv, use_cache=False)


def _regex_matched(state: T_State) -> Match[str]:
    return state[REGEX_MATCHED]


def RegexMatched() -> Match[str]:
    """正则匹配结果"""
    return Depends(_regex_matched, use_cache=False)


def _regex_str(
    groups: tuple[Union[str, int], ...],
) -> Callable[[T_State], Union[str, tuple[Union[str, Any], ...], Any]]:
    def _regex_str_dependency(
        state: T_State,
    ) -> Union[str, tuple[Union[str, Any], ...], Any]:
        return _regex_matched(state).group(*groups)

    return _regex_str_dependency


@overload
def RegexStr(group: Literal[0] = 0, /) -> str: ...


@overload
def RegexStr(group: Union[str, int], /) -> Union[str, Any]: ...


@overload
def RegexStr(
    group1: Union[str, int], group2: Union[str, int], /, *groups: Union[str, int]
) -> tuple[Union[str, Any], ...]: ...


def RegexStr(*groups: Union[str, int]) -> Union[str, tuple[Union[str, Any], ...], Any]:
    """正则匹配结果文本"""
    return Depends(_regex_str(groups), use_cache=False)


def _regex_group(state: T_State) -> tuple[Any, ...]:
    return _regex_matched(state).groups()


def RegexGroup() -> tuple[Any, ...]:
    """正则匹配结果 group 元组"""
    return Depends(_regex_group, use_cache=False)


def _regex_dict(state: T_State) -> dict[str, Any]:
    return _regex_matched(state).groupdict()


def RegexDict() -> dict[str, Any]:
    """正则匹配结果 group 字典"""
    return Depends(_regex_dict, use_cache=False)


def _startswith(state: T_State) -> str:
    return state[STARTSWITH_KEY]


def Startswith() -> str:
    """响应触发前缀"""
    return Depends(_startswith, use_cache=False)


def _endswith(state: T_State) -> str:
    return state[ENDSWITH_KEY]


def Endswith() -> str:
    """响应触发后缀"""
    return Depends(_endswith, use_cache=False)


def _fullmatch(state: T_State) -> str:
    return state[FULLMATCH_KEY]


def Fullmatch() -> str:
    """响应触发完整消息"""
    return Depends(_fullmatch, use_cache=False)


def _keyword(state: T_State) -> str:
    return state[KEYWORD_KEY]


def Keyword() -> str:
    """响应触发关键字"""
    return Depends(_keyword, use_cache=False)


def Received(id: Optional[str] = None, default: Any = None) -> Any:
    """`receive` 事件参数"""

    def _received(matcher: "Matcher") -> Any:
        return matcher.get_receive(id or "", default)

    return Depends(_received, use_cache=False)


def LastReceived(default: Any = None) -> Any:
    """`last_receive` 事件参数"""

    def _last_received(matcher: "Matcher") -> Any:
        return matcher.get_last_receive(default)

    return Depends(_last_received, use_cache=False)


def ReceivePromptResult(id: Optional[str] = None) -> Any:
    """`receive` prompt 发送结果"""

    def _receive_prompt_result(matcher: "Matcher") -> Any:
        return matcher.state.get(
            REJECT_PROMPT_RESULT_KEY.format(key=RECEIVE_KEY.format(id=id))
        )

    return Depends(_receive_prompt_result, use_cache=False)


def PausePromptResult() -> Any:
    """`pause` prompt 发送结果"""

    def _pause_prompt_result(matcher: "Matcher") -> Any:
        return matcher.state.get(PAUSE_PROMPT_RESULT_KEY)

    return Depends(_pause_prompt_result, use_cache=False)


__autodoc__ = {
    "Arg": True,
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
    "ArgPromptResult": True,
}
