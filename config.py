config = {
    'fallback_command': 'natural_language.process',
    'fallback_command_after_nl_processors': 'core.tuling123',
    'command_start_flags': ('/', '／', '来，', '来,'),  # Add '' (empty string) here to allow commands without start flags
    'command_name_separators': ('->', '::', '/'),  # Regex
    'command_args_start_flags': ('，', '：', ',', ', ', ':', ': '),  # Regex
    'command_args_separators': ('，', ','),  # Regex
}
