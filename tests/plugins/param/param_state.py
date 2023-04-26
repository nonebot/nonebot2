from typing import List, Match, Tuple

from nonebot.typing import T_State
from nonebot.adapters import Message
from nonebot.params import (
    Command,
    Keyword,
    Endswith,
    RegexStr,
    Fullmatch,
    RegexDict,
    CommandArg,
    RawCommand,
    RegexGroup,
    Startswith,
    CommandStart,
    RegexMatched,
    ShellCommandArgs,
    ShellCommandArgv,
    CommandWhitespace,
)


async def state(x: T_State) -> T_State:
    return x


async def legacy_state(state):
    return state


async def not_legacy_state(state: int):
    ...


async def command(cmd: Tuple[str, ...] = Command()) -> Tuple[str, ...]:
    return cmd


async def raw_command(raw_cmd: str = RawCommand()) -> str:
    return raw_cmd


async def command_arg(cmd_arg: Message = CommandArg()) -> Message:
    return cmd_arg


async def command_start(start: str = CommandStart()) -> str:
    return start


async def command_whitespace(whitespace: str = CommandWhitespace()) -> str:
    return whitespace


async def shell_command_args(
    shell_command_args: dict = ShellCommandArgs(),
) -> dict:
    return shell_command_args


async def shell_command_argv(
    shell_command_argv: List[str] = ShellCommandArgv(),
) -> List[str]:
    return shell_command_argv


async def regex_dict(regex_dict: dict = RegexDict()) -> dict:
    return regex_dict


async def regex_group(regex_group: Tuple = RegexGroup()) -> Tuple:
    return regex_group


async def regex_matched(regex_matched: Match[str] = RegexMatched()) -> Match[str]:
    return regex_matched


async def regex_str(regex_str: str = RegexStr()) -> str:
    return regex_str


async def startswith(startswith: str = Startswith()) -> str:
    return startswith


async def endswith(endswith: str = Endswith()) -> str:
    return endswith


async def fullmatch(fullmatch: str = Fullmatch()) -> str:
    return fullmatch


async def keyword(keyword: str = Keyword()) -> str:
    return keyword
