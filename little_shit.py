import os
import random
from datetime import datetime

from config import config


class SkipException(Exception):
    pass


def _mkdir_if_not_exists_and_return_path(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_root_dir():
    return os.path.split(os.path.realpath(__file__))[0]


def get_filters_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'filters'))


def get_commands_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'commands'))


def get_nl_processors_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'nl_processors'))


def get_db_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'db'))


def get_default_db_path():
    return os.path.join(get_db_dir(), 'default.sqlite')


def get_tmp_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'tmp'))


def get_source(ctx_msg):
    """
    Source is used to distinguish the interactive sessions.
    Note: This value may change after restarting the bot.

    :return: an unique value representing a source, or a random value if something strange happened
    """
    if ctx_msg.get('via') == 'qq':
        if ctx_msg.get('type') == 'group_message' and ctx_msg.get('group_uid') and ctx_msg.get('sender_uid'):
            return 'g' + ctx_msg.get('group_uid') + 'p' + ctx_msg.get('sender_uid')
        elif ctx_msg.get('type') == 'discuss_message' and ctx_msg.get('discuss_id') and ctx_msg.get('sender_uid'):
            return 'd' + ctx_msg.get('discuss_id') + 'p' + ctx_msg.get('sender_uid')
        elif ctx_msg.get('type') == 'friend_message' and ctx_msg.get('sender_uid'):
            return 'p' + ctx_msg.get('sender_uid')
    elif ctx_msg.get('via') == 'wx':
        if ctx_msg.get('type') == 'group_message' and ctx_msg.get('group_id') and ctx_msg.get('sender_id'):
            return 'g' + ctx_msg.get('group_id') + 'p' + ctx_msg.get('sender_id')
        elif ctx_msg.get('type') == 'friend_message' and ctx_msg.get('sender_id'):
            return 'p' + ctx_msg.get('sender_id')
    return str(int(datetime.now().timestamp())) + str(random.randint(100, 999))


def get_target(ctx_msg):
    """
    Target is used to distinguish the records in database.
    Note: This value will not change after restarting the bot.

    :return: an unique value representing a target, or None if there is no persistent unique value
    """
    if ctx_msg.get('via') == 'qq':
        if ctx_msg.get('type') == 'group_message' and ctx_msg.get('group_uid'):
            return 'g' + ctx_msg.get('group_uid')
        elif ctx_msg.get('type') == 'friend_message' and ctx_msg.get('sender_uid'):
            return 'p' + ctx_msg.get('sender_uid')
    elif ctx_msg.get('via') == 'wx':
        if ctx_msg.get('type') == 'friend_message' and ctx_msg.get('sender_account'):
            return 'p' + ctx_msg.get('sender_account')
    return None


def get_command_start_flags():
    return tuple(sorted(config.get('command_start_flags', ('',)), reverse=True))


def get_command_name_separators():
    return tuple(sorted(('\.',) + config.get('command_name_separators', ()), reverse=True))


def get_command_args_start_flags():
    return tuple(sorted(('[ \t\n]',) + config.get('command_args_start_flags', ()), reverse=True))


def get_command_args_separators():
    return tuple(sorted(('[ \t\n]',) + config.get('command_args_separators', ()), reverse=True))


def get_fallback_command():
    return config.get('fallback_command')


def get_fallback_command_after_nl_processors():
    return config.get('fallback_command_after_nl_processors')
