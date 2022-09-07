from typing import List, Tuple

from nonebot.typing import T_State
from nonebot.adapters import Message
from nonebot.params import (
    command,
    regex_dict,
    command_arg,
    raw_command,
    regex_group,
    command_start,
    regex_matched,
    shell_command_args,
    shell_command_argv,
)


async def state(x: T_State) -> T_State:
    return x


async def legacy_state(state):
    return state


async def not_legacy_state(state: int):
    ...


async def command_test(cmd: Tuple[str, ...] = command()) -> Tuple[str, ...]:
    return cmd


async def raw_command_test(raw_cmd: str = raw_command()) -> str:
    return raw_cmd


async def command_arg_test(cmd_arg: Message = command_arg()) -> Message:
    return cmd_arg


async def command_start_test(start: str = command_start()) -> str:
    return start


async def shell_command_args_test(
    shell_command_args: dict = shell_command_args(),
) -> dict:
    return shell_command_args


async def shell_command_argv_test(
    shell_command_argv: List[str] = shell_command_argv(),
) -> List[str]:
    return shell_command_argv


async def regex_dict_test(regex_dict: dict = regex_dict()) -> dict:
    return regex_dict


async def regex_group_test(regex_group: Tuple = regex_group()) -> Tuple:
    return regex_group


async def regex_matched_test(regex_matched: str = regex_matched()) -> str:
    return regex_matched
