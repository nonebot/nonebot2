from re import Match

from nonebot.adapters import Message
from nonebot.params import (
    Command,
    CommandArg,
    CommandStart,
    CommandWhitespace,
    Endswith,
    Fullmatch,
    Keyword,
    RawCommand,
    RegexDict,
    RegexGroup,
    RegexMatched,
    RegexStr,
    ShellCommandArgs,
    ShellCommandArgv,
    Startswith,
)
from nonebot.typing import T_State


async def state(x: T_State) -> T_State:
    return x


async def postpone_state(x: "T_State") -> T_State:
    return x


async def legacy_state(state):
    return state


async def not_legacy_state(state: int): ...


async def command(cmd: tuple[str, ...] = Command()) -> tuple[str, ...]:
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
    shell_command_argv: list[str] = ShellCommandArgv(),
) -> list[str]:
    return shell_command_argv


async def regex_dict(regex_dict: dict = RegexDict()) -> dict:
    return regex_dict


async def regex_group(regex_group: tuple = RegexGroup()) -> tuple:
    return regex_group


async def regex_matched(regex_matched: Match[str] = RegexMatched()) -> Match[str]:
    return regex_matched


async def regex_str(
    entire: str = RegexStr(),
    type_: str = RegexStr("type"),
    second: str = RegexStr(2),
    groups: tuple[str, ...] = RegexStr(1, "arg"),
) -> tuple[str, str, str, tuple[str, ...]]:
    return entire, type_, second, groups


async def startswith(startswith: str = Startswith()) -> str:
    return startswith


async def endswith(endswith: str = Endswith()) -> str:
    return endswith


async def fullmatch(fullmatch: str = Fullmatch()) -> str:
    return fullmatch


async def keyword(keyword: str = Keyword()) -> str:
    return keyword
