import os

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


def get_db_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'db'))


def get_default_db_path():
    return os.path.join(get_db_dir(), 'default.sqlite')


def get_tmp_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'tmp'))


def get_source(ctx_msg):
    """
    Source is used to distinguish the interactive sessions.
    """
    if ctx_msg.get('type') == 'group_message':
        return 'g' + str(ctx_msg.get('gnumber')) + 'p' + str(ctx_msg.get('sender_qq'))
    else:
        return 'p' + str(ctx_msg.get('sender_qq'))


def get_target(ctx_msg):
    """
    Target is used to distinguish the records in database.
    """
    if ctx_msg.get('type') == 'group_message':
        return 'g' + str(ctx_msg.get('gnumber'))
    else:
        return 'p' + str(ctx_msg.get('sender_qq'))


def get_command_start_flags():
    return tuple(sorted(config['command_start_flags'], reverse=True))


def get_command_name_separators():
    return tuple(sorted(config['command_name_separators'], reverse=True))


def get_command_args_start_flags():
    return tuple(sorted(('[ \t\n]',) + config['command_args_start_flags'], reverse=True))
