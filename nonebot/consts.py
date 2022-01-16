"""
FrontMatter:
    sidebar_position: 9
    description: nonebot.consts 模块
"""
from typing_extensions import Literal

# used by Matcher
RECEIVE_KEY: Literal["_receive_{id}"] = "_receive_{id}"
LAST_RECEIVE_KEY: Literal["_last_receive"] = "_last_receive"
ARG_KEY: Literal["{key}"] = "{key}"
REJECT_TARGET: Literal["_current_target"] = "_current_target"
REJECT_CACHE_TARGET: Literal["_next_target"] = "_next_target"

# used by Rule
PREFIX_KEY: Literal["_prefix"] = "_prefix"

CMD_KEY: Literal["command"] = "command"
RAW_CMD_KEY: Literal["raw_command"] = "raw_command"
CMD_ARG_KEY: Literal["command_arg"] = "command_arg"

SHELL_ARGS: Literal["_args"] = "_args"
SHELL_ARGV: Literal["_argv"] = "_argv"

REGEX_MATCHED: Literal["_matched"] = "_matched"
REGEX_GROUP: Literal["_matched_groups"] = "_matched_groups"
REGEX_DICT: Literal["_matched_dict"] = "_matched_dict"
