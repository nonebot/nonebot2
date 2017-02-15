config = {
    'fallback_command': 'natural_language.process',
    'fallback_command_after_nl_processors': 'ai.tuling123',
    'command_start_flags': ('/', '／', '来，', '来,'),  # Add '' (empty string) here to allow commands without start flags
    'command_name_separators': ('->', '::', '/'),  # Regex
    'command_args_start_flags': ('，', '：', ',', ', ', ':', ': '),  # Regex
    'command_args_separators': ('，', ','),  # Regex

    'message_sources': [
        {
            'via': 'mojo_weixin',
            'login_id': 'rcdevtest',
            'superuser_id': 'richard_chien_0',
            'api_url': 'http://127.0.0.1:5001/openwx',
        },
        {
            'via': 'mojo_webqq',
            'login_id': '3281334718',
            'superuser_id': '1002647525',
            'api_url': 'http://127.0.0.1:5000/openqq',
        }
    ]
}
