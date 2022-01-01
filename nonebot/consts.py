from sys import intern

# used by Matcher
RECEIVE_KEY = intern("_receive_{id}")
LAST_RECEIVE_KEY = intern("_last_receive")
ARG_KEY = intern("{key}")
REJECT_TARGET = intern("_current_target")
REJECT_CACHE_TARGET = intern("_next_target")

# used by Rule
PREFIX_KEY = intern("_prefix")

CMD_KEY = intern("command")
RAW_CMD_KEY = intern("raw_command")
CMD_ARG_KEY = intern("command_arg")

SHELL_ARGS = intern("_args")
SHELL_ARGV = intern("_argv")

REGEX_MATCHED = intern("_matched")
REGEX_GROUP = intern("_matched_groups")
REGEX_DICT = intern("_matched_dict")
