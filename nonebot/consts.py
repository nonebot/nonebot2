# used by Params
WRAPPER_ASSIGNMENTS = (
    "__module__",
    "__name__",
    "__qualname__",
    "__doc__",
    "__annotations__",
    "__globals__",
)

# used by Matcher
RECEIVE_KEY = "_receive_{id}"
ARG_KEY = "_arg_{key}"
ARG_STR_KEY = "{key}"
REJECT_TARGET = "_current_target"

# used by Rule
PREFIX_KEY = "_prefix"

CMD_KEY = "command"
RAW_CMD_KEY = "raw_command"
CMD_ARG_KEY = "command_arg"

SHELL_ARGS = "_args"
SHELL_ARGV = "_argv"

REGEX_MATCHED = "_matched"
REGEX_GROUP = "_matched_groups"
REGEX_DICT = "_matched_dict"
